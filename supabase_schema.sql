-- Run this once in Supabase → SQL Editor → New query → Run.
create table if not exists public.debates (
  id               uuid primary key,
  created_at       timestamptz default now(),
  language         text,
  model            text,
  belief           text,
  restatement      text,
  claim_type       text,
  confidence_before int,
  confidence_after  int,
  advocate         jsonb,
  challenge        jsonb,
  steelman         text,
  questions        jsonb,
  judge            jsonb,
  answers          jsonb,
  reassess         jsonb,
  pushback         jsonb,
  sources          jsonb,
  rating           int,      -- 1 = 👍, 0 = 👎, null = not rated
  feedback         text,
  change_mind      text
);

-- The app uses the anon key server-side (it is never sent to the browser).
alter table public.debates enable row level security;
create policy "app can insert" on public.debates for insert to anon with check (true);
create policy "app can read"   on public.debates for select to anon using (true);
create policy "app can update" on public.debates for update to anon using (true) with check (true);
