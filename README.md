# TalentScale AI — Workforce Planning Platform

AI-powered Talent Acquisition team structure calculator for HR leaders.

---

## Project Structure

```
TalentScaleAI/
├── frontend/          # Next.js 15 + TypeScript + Tailwind + Recharts
└── backend/           # FastAPI + Python + Anthropic/OpenAI + ChromaDB
```

---

## Quick Start (Local Development)

### Frontend

```bash
cd frontend
cp .env.local.example .env.local
# Edit .env.local: add your ANTHROPIC_API_KEY
npm install
npm run dev
# → http://localhost:3000
```

### Backend

```bash
cd backend
cp .env.example .env
# Edit .env: add ANTHROPIC_API_KEY or OPENAI_API_KEY
pip install -r requirements.txt
uvicorn app.main:app --reload
# → http://localhost:8000
```

---

## Environment Variables

### Frontend (`frontend/.env.local`)

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_BACKEND_URL` | Backend URL (default: http://localhost:8000) |
| `ANTHROPIC_API_KEY` | Anthropic API key for AI chat |

### Backend (`backend/.env`)

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic Claude API key (primary) |
| `OPENAI_API_KEY` | OpenAI API key (fallback) |
| `DATABASE_URL` | SQLite (default) or PostgreSQL URL |
| `CHROMA_PERSIST_DIR` | ChromaDB storage path |

---

## Deployment

### Frontend → Vercel

1. Push the `frontend/` folder to a GitHub repository
2. Go to [vercel.com](https://vercel.com) → **New Project** → import repo
3. Set **Root Directory** to `frontend`
4. Add environment variables:
   - `ANTHROPIC_API_KEY` = your key
5. Click **Deploy**

Or via CLI:
```bash
cd frontend
npx vercel --prod
```

### Backend → Render

1. Push the `backend/` folder to a GitHub repository
2. Go to [render.com](https://render.com) → **New Web Service** → connect repo
3. Set:
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render dashboard
5. Click **Deploy**

Or via Docker:
```bash
cd backend
docker build -t talentscale-backend .
docker run -p 8000:8000 --env-file .env talentscale-backend
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/calculate` | Calculate TA team structure |
| POST | `/api/chat` | AI chatbot response |
| POST | `/api/export/excel` | Download Excel report |
| POST | `/api/export/pdf` | Download PDF report |
| GET | `/api/benchmarks/{type}` | Get industry benchmarks |
| GET | `/health` | Health check |

---

## Features

- **3-panel dashboard**: Inputs → TA Structure → AI Chat
- **Business logic**: Product vs Consulting models with dropout adjustment
- **AI chatbot**: Powered by Claude (Anthropic) with TA expertise
- **Export**: PDF and Excel reports
- **RAG**: ChromaDB vector store with benchmark documents
- **Charts**: Pie + Bar charts via Recharts
- **Responsive**: Works on desktop and tablet

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS, Recharts, Framer Motion |
| Backend | FastAPI, Python 3.11, SQLAlchemy |
| AI | Anthropic Claude (claude-sonnet-4-20250514) |
| RAG | ChromaDB |
| Export | ReportLab (PDF), OpenPyXL (Excel) |
| Deploy | Vercel (frontend), Render (backend) |
