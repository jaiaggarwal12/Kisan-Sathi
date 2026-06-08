# Deploying Kisan Sathi (free tiers)

Three pieces to deploy:
- **Backend** (FastAPI + ML) → **Hugging Face Spaces** (free, 16GB RAM — fits PyTorch)
- **Farmer app** (static) → **Vercel**
- **Officer portal** (static) → **Vercel**

> Why not Render free for the backend? Render's free tier is 512MB RAM and the
> PyTorch + Transformers pest model needs more than that. Hugging Face Spaces
> free CPU gives 16GB. (A Render "lite" option without the model is noted below.)

---

## 1) Backend → Hugging Face Spaces (Docker)

1. Create account at https://huggingface.co → **New Space**.
2. Owner: you · Space name: `kisan-sathi-api` · **SDK: Docker** · **Blank** · Public.
3. In the Space → **Files** → create a `README.md` with this header at the top:
   ```
   ---
   title: Kisan Sathi API
   sdk: docker
   app_port: 7860
   ---
   ```
4. Upload the **contents of the `backend/` folder** into the Space repo
   (the `Dockerfile`, `app/`, `data/`, `requirements.txt`). Easiest:
   ```bat
   git clone https://huggingface.co/spaces/<you>/kisan-sathi-api
   xcopy /E /I "e:\kisan sathi\backend\app"  kisan-sathi-api\app
   xcopy /E /I "e:\kisan sathi\backend\data" kisan-sathi-api\data
   copy "e:\kisan sathi\backend\Dockerfile" kisan-sathi-api\
   copy "e:\kisan sathi\backend\requirements.txt" kisan-sathi-api\
   cd kisan-sathi-api & git add . & git commit -m "deploy" & git push
   ```
5. Space → **Settings → Variables and secrets** → add your keys as **Secrets**:
   `OPENWEATHER_KEY`, `AGRO_API_KEY`, `DATA_GOV_API_KEY`,
   `DATA_GOV_RESOURCE_ID`, `DEFAULT_FIELD_ID`, and `CORS_ORIGINS=*`.
6. The Space builds and goes live at:
   `https://<you>-kisan-sathi-api.hf.space`
   Test: open `https://<you>-kisan-sathi-api.hf.space/docs`

---

## 2) Farmer app → Vercel

1. Push this repo to GitHub (see below).
2. https://vercel.com → **Add New Project** → import the GitHub repo.
3. Set **Root Directory** = `farmer-app`.
4. Framework preset = **Vite** (auto). Build = `npm run build`, Output = `dist`.
5. **Environment Variables** → add
   `VITE_API_BASE = https://<you>-kisan-sathi-api.hf.space`
6. Deploy → you get `https://kisan-sathi-farmer.vercel.app`.

## 3) Officer portal → Vercel

Repeat step 2, but **Root Directory** = `officer-portal` (new Vercel project,
same repo). Same `VITE_API_BASE` env var.

---

## Alternative: backend on Render (lite, no real pest AI)

Render free works if you skip PyTorch (pest detection falls back to a stub;
weather, mandi, soil, chatbot, proximity, schemes all work):

1. https://render.com → **New → Web Service** → connect the repo.
2. Root Directory = `backend`.
3. Build: `pip install -r requirements.txt` (PyTorch is not installed here, so
   it stays light).
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add the same env vars as above.

---

## Notes
- `.env` is git-ignored — never commit keys. Set them in the host's dashboard.
- The SQLite DB resets on redeploy (fine for a demo). Use a managed Postgres
  (set `DATABASE_URL`) for persistence.
- `CORS_ORIGINS=*` is set for demo simplicity; lock it to your Vercel domains
  for production.
