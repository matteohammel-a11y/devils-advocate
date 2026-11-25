# Put Devil's Advocate online (public link + shared database)

You will create 5 free accounts, then connect them. It takes about 30–40 minutes the first time.

| What | Service | Why |
|---|---|---|
| The code | **GitHub** | Streamlit Cloud reads the app from here |
| The link | **Streamlit Community Cloud** | Hosts the app for free → `https://your-name.streamlit.app` |
| The AI | **Ollama Cloud** | Runs the model online, so your Mac doesn't have to be on |
| Web search | **Tavily** | Same key as on your laptop |
| The memory | **Supabase** | A database that stores every debate permanently |

---

## Part A: the database (Supabase)
1. Go to **supabase.com**, click **Start your project**, and sign in with GitHub (create a GitHub account first if you need one).
2. Click **New project**. Name it `devils-advocate`, choose any database password, pick region **Central EU (Frankfurt)**, then click **Create**. Wait about 2 minutes.
3. In the left menu, open **SQL Editor** and click **New query**.
4. Open the file `supabase_schema.sql` from this folder (double-click, then open with TextEdit). Copy everything, paste it into Supabase, and click **Run**. You should see "Success".
5. In the left menu, go to **Project Settings → API** (or **Data API / API Keys**). Copy two things into a note:
   - **Project URL** (looks like `https://abcd.supabase.co`)
   - the **anon / public** key (a long code)

## Part B: the AI key (Ollama Cloud)
1. Go to **ollama.com** and sign in (the same account as the Ollama app works).
2. Go to **ollama.com/settings/keys**, click **Add API key**, and copy the key into your note.

## Part C: the code (GitHub)
1. Download **GitHub Desktop** (desktop.github.com), install it, and sign in.
2. Click **File → Add Local Repository** and choose the `devils-advocate` folder on your Desktop.
   It says it isn't a repository yet. Click **create a repository**, then **Create Repository**.
3. Click **Publish repository**. You can leave **Keep this code private** ticked. Then click **Publish**.

The `.gitignore` file makes sure your keys, `.venv` and local data are **not** uploaded.

## Part D: the link (Streamlit Community Cloud)
1. Go to **share.streamlit.io** and sign in with GitHub.
2. Click **Create app**, then **Deploy a public app from GitHub**.
3. Repository: `your-name/devils-advocate`. Branch: `main`. Main file: `app.py`.
4. App URL: choose something like `devils-advocate-luiss`.
5. Click **Advanced settings → Secrets**. Open `.streamlit/secrets.example.toml`, copy everything, paste it in, and replace each placeholder with your real values from the note.
   (In Finder, press `Cmd + Shift + .` to see hidden folders like `.streamlit`.)
6. Click **Deploy**. After 2–3 minutes your link is live, and you can send it to anyone.

## Updating the app later
Change files on your Mac → in GitHub Desktop, write a short summary and click **Commit to main** → **Push origin**.
Streamlit Cloud updates the live app automatically within a minute.

## How "getting better" works
- Every debate is saved in Supabase: belief, both cases, the Judge's map, answers, confidence before and after, and pushback.
- Users rate each challenge 👍/👎. The best-rated challenges are shown to the Devil as **examples of good
  challenges** for new beliefs, so quality improves as people use it.
- **Community** page: live stats (number of debates, % rated useful, average confidence shift, languages).
- **Team export**: download every debate as CSV (protected by `ADMIN_PASSWORD`) to find weak spots and
  improve the prompts. That is your iteration log.

The model itself is not retrained; the system improves through examples and through your prompt changes.

## Good to know
- Streamlit Cloud apps go to sleep after a few days without visitors. The first visitor then clicks "wake up" and waits about 30 seconds.
- The free Ollama Cloud and Tavily plans have usage limits. For a class demo and a small user study they are normally enough; check your usage on their websites.
- The app tells users that debates are stored anonymously and asks them not to enter personal data.
