# TA Capacity AI — Workforce Intelligence Platform

A full-stack AI-powered Talent Acquisition capacity planning tool.

---

## What It Does

- **Formula Engine** — calculates your exact TA team structure from 4 inputs
- **Org Chart Visualizer** — live SVG hierarchy diagram
- **AI Chat Assistant** — context-aware Q&A via OpenRouter (any LLM)
- **Industry Benchmarks** — dropout rates, productivity norms by sector

---

## Formula (from backend/calculator logic)

```
adjusted_hires  = ceil(total_hires / (1 - dropout_ratio))
recruiters      = ceil(adjusted_hires × complexity_factor / productivity)
leads           = ceil(recruiters / 5)
managers        = ceil(leads / 3)
ta_head         = 1  (fixed)
total_team      = recruiters + leads + managers + 1
```

---

## Quick Start — Frontend Only (no backend needed)

```bash
# Just open the file in your browser
open frontend/index.html
```

Add your OpenRouter key, set the sliders, click Calculate, then chat.

---

## Full Stack Setup

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### Key API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/calculate` | Run TA formula engine |
| GET | `/api/presets` | Startup/Enterprise presets |
| GET | `/api/benchmark` | Industry benchmarks |

### Example API Call

```bash
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "total_hires": 200,
    "dropout_ratio": 0.15,
    "complexity_factor": 1.2,
    "productivity": 40
  }'
```

Response:
```json
{
  "adjusted_hiring": 236,
  "recruiters": 8,
  "leads": 2,
  "managers": 1,
  "ta_head": 1,
  "total_team": 12
}
```

---

## Environment Variables

```env
OPENAI_API_KEY=sk-...         # Optional: for server-side AI calls
OPENROUTER_API_KEY=sk-or-...  # Optional: for server-side OpenRouter
```

---

## Project Structure

```
ta_capacity/
├── frontend/
│   └── index.html          # Complete UI (zero build step)
├── backend/
│   ├── main.py             # FastAPI app + all routes
│   └── requirements.txt
└── README.md
```

---

## AI Chat Context

The AI assistant receives your full calculation context as a system prompt:

- Hiring targets, dropout rate, complexity, productivity
- Full team structure output
- Benchmarking data

Ask it anything: strategy advice, timeline planning, sourcing channels, risk analysis, budget estimates, or what-if scenarios.

---

## OpenRouter Models Supported

- Claude Sonnet 4.5 / Opus 4 / Haiku
- GPT-4o / GPT-4o Mini
- Gemini 2.0 Flash
- Llama 3.3 70B
- DeepSeek V3

Get a free key at https://openrouter.ai
