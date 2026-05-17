from pydantic import BaseModel, Field
from typing import Literal, List, Optional, Dict, Any


class WorkforceInput(BaseModel):
    hiring_target: int = Field(..., ge=1, le=100000)
    company_type: Literal["product", "consulting", "gcc", "startup", "enterprise"]
    dropout_ratio: float = Field(..., ge=0, le=80)
    complexity_factor: Literal["low", "medium", "high", "hyper"]
    recruiter_productivity: int = Field(..., ge=1, le=200)
    geography: Literal["domestic", "multi-region", "global"] = "domestic"
    ai_niche_percent: float = Field(default=0, ge=0, le=80)


class TAStructureResult(BaseModel):
    adjusted_hiring: int
    total_ta: int
    junior_recruiters: int
    recruiters: int
    senior_recruiters: int
    sourcers: int
    coordinators: int
    leads: int
    managers: int
    ta_head: int
    hiring_capacity: int
    timeline: str
    utilization: float
    estimated_cost: str
    cost_per_hire: str
    model_used: str


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    context: Optional[Dict[str, Any]] = None


class ExportRequest(BaseModel):
    inputs: WorkforceInput
    result: TAStructureResult
