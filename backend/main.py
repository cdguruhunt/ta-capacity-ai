from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import math, os

app = FastAPI(title="TA Capacity AI", version="1.0.0", description="Talent Acquisition Workforce Planning API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── Serve frontend ──
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/", include_in_schema=False)
def serve_frontend():
    idx = os.path.join(frontend_path, "index.html")
    if os.path.exists(idx):
        return FileResponse(idx)
    return {"message": "TA Capacity AI Backend v1.0", "docs": "/docs"}

# ── Models ──
class CalculateRequest(BaseModel):
    total_hires: int       = Field(..., ge=1,   le=10000, description="Total headcount hires needed")
    dropout_ratio: float   = Field(..., ge=0.0, le=0.49,  description="Candidate dropout/falloff rate (0–0.49)")
    complexity_factor: float = Field(..., ge=1.0, le=5.0, description="Role complexity multiplier")
    productivity: float    = Field(..., ge=1.0,  le=500,   description="Hires per recruiter per year")

class CalculateResponse(BaseModel):
    inputs: dict
    adjusted_hiring: int
    recruiters: int
    leads: int
    managers: int
    ta_head: int
    total_team: int
    ratios: dict
    formula_trace: dict

class HealthResponse(BaseModel):
    status: str
    version: str

# ── Core calculator (matches Python calculator.py logic) ──
def calculate_ta_structure(total_hires: int, dropout_ratio: float,
                           complexity_factor: float, productivity: float) -> dict:
    adjusted_hiring = math.ceil(total_hires / (1 - dropout_ratio))
    recruiters      = math.ceil((adjusted_hiring * complexity_factor) / productivity)
    leads           = math.ceil(recruiters / 5)
    managers        = math.ceil(leads / 3)
    ta_head         = 1
    total_team      = recruiters + leads + managers + ta_head

    return {
        "inputs": {
            "total_hires": total_hires,
            "dropout_ratio": dropout_ratio,
            "complexity_factor": complexity_factor,
            "productivity": productivity,
        },
        "adjusted_hiring": adjusted_hiring,
        "recruiters": recruiters,
        "leads": leads,
        "managers": managers,
        "ta_head": ta_head,
        "total_team": total_team,
        "ratios": {
            "hires_per_recruiter": round(adjusted_hiring / recruiters, 2) if recruiters else 0,
            "span_of_control_lead": round(recruiters / leads, 1) if leads else 0,
            "span_of_control_mgr": round(leads / managers, 1) if managers else 0,
            "team_overhead_pct": round((total_team - recruiters) / total_team * 100, 1) if total_team else 0,
        },
        "formula_trace": {
            "step1": f"adjusted = ceil({total_hires} / (1 - {dropout_ratio})) = {adjusted_hiring}",
            "step2": f"recruiters = ceil({adjusted_hiring} × {complexity_factor} / {productivity}) = {recruiters}",
            "step3": f"leads = ceil({recruiters} / 5) = {leads}",
            "step4": f"managers = ceil({leads} / 3) = {managers}",
            "step5": f"ta_head = 1 (fixed)",
            "step6": f"total = {recruiters} + {leads} + {managers} + 1 = {total_team}",
        }
    }

# ── Routes ──
@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/api/calculate", response_model=CalculateResponse)
def calculate(req: CalculateRequest):
    try:
        result = calculate_ta_structure(
            req.total_hires, req.dropout_ratio,
            req.complexity_factor, req.productivity
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/presets")
def get_presets():
    """Return sample presets for common org sizes."""
    presets = [
        {"name": "Startup",    "total_hires": 50,   "dropout_ratio": 0.10, "complexity_factor": 1.0, "productivity": 35},
        {"name": "Scale-up",   "total_hires": 200,  "dropout_ratio": 0.15, "complexity_factor": 1.2, "productivity": 40},
        {"name": "Enterprise", "total_hires": 500,  "dropout_ratio": 0.20, "complexity_factor": 1.5, "productivity": 45},
        {"name": "Corp+",      "total_hires": 1000, "dropout_ratio": 0.25, "complexity_factor": 2.0, "productivity": 50},
    ]
    return {"presets": [{"label": p["name"], "inputs": p,
                         "result": calculate_ta_structure(**{k:v for k,v in p.items() if k!="name"})}
                        for p in presets]}

@app.get("/api/benchmark")
def get_benchmarks():
    """Industry benchmarks for TA capacity planning."""
    return {
        "benchmarks": {
            "recruiter_productivity": {
                "low_complexity": {"min": 40, "max": 60, "unit": "hires/year"},
                "mid_complexity": {"min": 25, "max": 40, "unit": "hires/year"},
                "high_complexity": {"min": 10, "max": 25, "unit": "hires/year"},
                "source": "LinkedIn Talent Trends 2024"
            },
            "dropout_rates": {
                "tech": 0.18, "finance": 0.12, "retail": 0.25,
                "healthcare": 0.15, "manufacturing": 0.20
            },
            "span_of_control": {
                "recommended_lead_to_recruiter": 5,
                "recommended_mgr_to_lead": 3
            }
        }
    }
