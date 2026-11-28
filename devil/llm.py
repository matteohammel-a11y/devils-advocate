"""Thin LLM client. Talks to Ollama (or any OpenAI-compatible server) via the OpenAI SDK."""
from __future__ import annotations

import json
import os
import re

import httpx
import time

from openai import (APIConnectionError, BadRequestError, InternalServerError, OpenAI, RateLimitError,
                    UnprocessableEntityError)

DEFAULT_BASE_URL = os.getenv("DA_BASE_URL", "http://localhost:11434/v1")
DEFAULT_API_KEY = os.getenv("DA_API_KEY", "ollama")
DEFAULT_MODEL = os.getenv("DA_MODEL", "qwen3:8b")
FALLBACK_MODEL = os.getenv("DA_FALLBACK_MODEL", "")  # used if the main model is overloaded

# Other companies' models, written as "<provider>:<model>", e.g. "openai:chat-latest" or
# "claude:claude-sonnet-5-5". Both providers offer an OpenAI-compatible endpoint, so the same client works.
PROVIDERS = {
    "openai": ("https://api.openai.com/v1", "OPENAI_API_KEY"),
    "claude": ("https://api.anthropic.com/v1/", "ANTHROPIC_API_KEY"),
}


def resolve(model: str, base_url: str, api_key: str) -> tuple[str, str, str]:
    """Turn "openai:gpt-x" into (model, base_url, key); anything else uses the app's own connection.
    (Ollama names like "deepseek-v3.1:671b-cloud" also contain ":", but their prefix isn't a provider.)"""
    prefix, sep, name = model.partition(":")
    if sep and prefix.strip().lower() in PROVIDERS:
        url, env = PROVIDERS[prefix.strip().lower()]
        return name.strip(), url, os.getenv(env, "")
    return model, base_url, api_key


def provider_ready(model: str) -> bool:
    prefix, sep, _ = model.partition(":")
    p = prefix.strip().lower()
    return not (sep and p in PROVIDERS) or bool(os.getenv(PROVIDERS[p][1]))


_THINK = re.compile(r"<think>.*?</think>", re.DOTALL)


def list_ollama_models(base_url: str = DEFAULT_BASE_URL, api_key: str = "") -> list[str]:
    """Models available at base_url: Ollama's /api/tags, else the OpenAI-style /models list
    (works for Gemini, Groq, OpenRouter…). Returns [] if nothing answers."""
    root = base_url.rstrip("/").removesuffix("/v1")
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    try:
        r = httpx.get(f"{root}/api/tags", timeout=3, headers=headers)
        r.raise_for_status()
        return sorted(m["name"] for m in r.json().get("models", []))
    except Exception:
        pass
    try:
        r = httpx.get(base_url.rstrip("/") + "/models", timeout=5, headers=headers)
        r.raise_for_status()
        ids = [m.get("id", "").removeprefix("models/") for m in r.json().get("data", [])]
        chat = [i for i in ids if i and not any(x in i for x in ("embed", "tts", "image", "whisper", "guard",
                                                                    "audio", "veo", "imagen", "aqa"))]
        return sorted(chat)
    except Exception:
        return []


def parse_json(text: str) -> dict:
    """Parse a model reply as JSON, tolerating code fences, <think> blocks and chatter."""
    text = _THINK.sub("", text).strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            return json.loads(text[start : end + 1])
        raise


class LLM:
    def __init__(self, model: str = DEFAULT_MODEL, base_url: str = DEFAULT_BASE_URL,
                 api_key: str = DEFAULT_API_KEY, temperature: float = 0.4,
                 think: bool = False, max_tokens: int | None = 1500):
        self.model = model
        self.temperature = temperature
        self.think = think            # False = skip the hidden "thinking" phase (much faster)
        self.max_tokens = max_tokens  # cap answer length so no call runs away
        self.client = OpenAI(base_url=base_url, api_key=api_key or "none", timeout=300)

    # Which request variant works, per (server, model). Remembered so only the first call probes.
    _variant_cache: dict = {}

    def _variants(self, json_mode: bool) -> list[dict]:
        """Request variants from fastest to most compatible. Providers differ: Ollama accepts
        reasoning_effort="none", Gemini 3 can't switch thinking off (and then needs more tokens)."""
        rf = {"response_format": {"type": "json_object"}} if json_mode else {}
        cap = {"max_tokens": self.max_tokens} if self.max_tokens else {}
        if self.think:
            return [{**rf}, {}]
        # "_no_temp": OpenAI reasoning models only accept the default temperature and want
        # max_completion_tokens instead of max_tokens.
        newcap = {"max_completion_tokens": self.max_tokens} if self.max_tokens else {}
        return [{**rf, "reasoning_effort": "none", **cap},
                {**rf, "reasoning_effort": "minimal"},
                {**rf, "reasoning_effort": "low"},
                {**rf, **cap},
                {**rf},
                {},
                {**rf, "reasoning_effort": "none", **newcap, "_no_temp": True},
                {**rf, "reasoning_effort": "low", "_no_temp": True},
                {**rf, "_no_temp": True},
                {"_no_temp": True}]

    def chat(self, system: str, user: str, json_mode: bool = False,
             history: list[dict] | None = None) -> str:
        messages = [{"role": "system", "content": system}, *(history or []),
                    {"role": "user", "content": user}]
        key = (str(self.client.base_url), self.model, json_mode, self.think)
        variants = self._variants(json_mode)
        start = self._variant_cache.get(key, 0)
        last_exc = None
        for round_ in range(3):  # if everything fails (e.g. server really overloaded), wait and retry
            for i in range(start, len(variants)):
                try:
                    resp = self._create(messages, variants[i])
                    self._variant_cache[key] = i
                    return _THINK.sub("", resp.choices[0].message.content or "").strip()
                except (BadRequestError, InternalServerError, UnprocessableEntityError) as exc:
                    last_exc = exc  # this variant isn't accepted: try the next, more compatible one
            start = 0
            time.sleep(5 * (round_ + 1))
        same_server = str(self.client.base_url).rstrip("/") == DEFAULT_BASE_URL.rstrip("/")
        if FALLBACK_MODEL and FALLBACK_MODEL != self.model and same_server:
            backup = LLM(FALLBACK_MODEL, str(self.client.base_url), self.client.api_key,
                         self.temperature, self.think, self.max_tokens)
            return backup.chat(system, user, json_mode, history)
        raise last_exc

    def _create(self, messages, kwargs):
        """One API call; on a rate limit (429) or a dropped connection, wait and retry."""
        kwargs = dict(kwargs)
        if not kwargs.pop("_no_temp", False):
            kwargs["temperature"] = self.temperature
        for attempt in range(6):
            try:
                return self.client.chat.completions.create(model=self.model, messages=messages, **kwargs)
            except (RateLimitError, APIConnectionError):
                if attempt == 5:
                    raise
                time.sleep(8 * (attempt + 1))

    def json(self, system: str, user: str, history: list[dict] | None = None) -> dict:
        """Ask for JSON; retry once with a reminder if the model returns invalid JSON."""
        reply = self.chat(system, user, json_mode=True, history=history)
        try:
            return parse_json(reply)
        except (json.JSONDecodeError, ValueError):
            reply = self.chat(system, user + "\n\nReturn ONLY valid JSON, nothing else.",
                              json_mode=True, history=history)
            return parse_json(reply)
