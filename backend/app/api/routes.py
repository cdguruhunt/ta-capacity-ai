from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.calculation import (
    WorkforceInput, ChatRequest, ExportRequest
)
from app.services.calculator import calculate_ta_structure
from app.services.chatbot import get_ai_response
from app.services.export_excel import generate_excel_report
from app.services.export_pdf import generate_pdf_report
from app.services.benchmark_engine import get_benchmarks
import io

router = APIRouter()


@router.post("/calculate")
def calculate(inputs: WorkforceInput):
    """Calculate the TA team structure based on workforce inputs."""
    try:
        result = calculate_ta_structure(inputs)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def chat(request: ChatRequest):
    """AI chatbot endpoint for workforce planning queries."""
    try:
        response = await get_ai_response(request)
        return {"success": True, "message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/excel")
def export_excel(request: ExportRequest):
    """Generate and download an Excel workforce planning report."""
    try:
        buffer = generate_excel_report(request.inputs, request.result)
        return StreamingResponse(
            io.BytesIO(buffer),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=TalentScale_Report.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/pdf")
def export_pdf(request: ExportRequest):
    """Generate and download a PDF workforce planning report."""
    try:
        buffer = generate_pdf_report(request.inputs, request.result)
        return StreamingResponse(
            io.BytesIO(buffer),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=TalentScale_Report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/benchmarks/{company_type}")
def benchmarks(company_type: str):
    """Get industry benchmark data for a given company type."""
    try:
        data = get_benchmarks(company_type)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
