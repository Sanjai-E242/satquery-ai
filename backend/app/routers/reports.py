import os
import json
import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.config import settings
from app.routers.query import RESULTS_DATABASE
from app.services.report_generator import generate_pdf_report, generate_json_report

router = APIRouter(prefix="/reports", tags=["Reports"])
logger = logging.getLogger("satquery.reports")

def find_result_data(execution_id: str) -> dict:
    """Finds result data from in-memory cache or on-disk JSON report."""
    candidates = [
        execution_id,
        f"exec_{execution_id}" if not execution_id.startswith("exec_") else execution_id[5:]
    ]
    for cid in candidates:
        if cid in RESULTS_DATABASE:
            return RESULTS_DATABASE[cid]
        json_path = settings.OUTPUTS_DIR / f"satquery_report_{cid}.json"
        if json_path.exists():
            try:
                with open(json_path, "r") as f:
                    data = json.load(f)
                    RESULTS_DATABASE[cid] = data
                    return data
            except Exception as e:
                logger.warning(f"Error reading report from {json_path}: {e}")
    return None

@router.post("/generate/{execution_id}")
async def generate_report(execution_id: str, format: str = "pdf"):
    res_data = find_result_data(execution_id)
    if res_data is None:
        raise HTTPException(status_code=404, detail=f"Execution ID '{execution_id}' not found.")

    clean_id = res_data.get("execution_id", execution_id)
    if format.lower() == "json":
        filename = f"satquery_report_{clean_id}.json"
        out_path = settings.OUTPUTS_DIR / filename
        generate_json_report(res_data, str(out_path))
        return {"report_id": clean_id, "format": "json", "download_url": f"/api/reports/{clean_id}/download?format=json"}
    else:
        filename = f"satquery_report_{clean_id}.pdf"
        out_path = settings.OUTPUTS_DIR / filename
        generate_pdf_report(res_data, str(out_path))
        return {"report_id": clean_id, "format": "pdf", "download_url": f"/api/reports/{clean_id}/download?format=pdf"}

@router.api_route("/{execution_id}/download", methods=["GET", "HEAD"])
async def download_report(execution_id: str, format: str = "pdf"):
    ext = "json" if format.lower() == "json" else "pdf"
    clean_id = execution_id if execution_id.startswith("exec_") else f"exec_{execution_id}"
    
    # Check candidates for existing file on disk
    candidate_paths = [
        settings.OUTPUTS_DIR / f"satquery_report_{execution_id}.{ext}",
        settings.OUTPUTS_DIR / f"satquery_report_{clean_id}.{ext}",
    ]
    
    out_path = None
    for p in candidate_paths:
        if p.exists():
            out_path = p
            break
            
    if out_path is None or not out_path.exists():
        res_data = find_result_data(execution_id)
        if res_data:
            target_id = res_data.get("execution_id", clean_id)
            out_path = settings.OUTPUTS_DIR / f"satquery_report_{target_id}.{ext}"
            if ext == "json":
                generate_json_report(res_data, str(out_path))
            else:
                generate_pdf_report(res_data, str(out_path))
        else:
            raise HTTPException(status_code=404, detail=f"Report for execution ID '{execution_id}' not found.")

    media_type = "application/json" if ext == "json" else "application/pdf"
    return FileResponse(path=out_path, media_type=media_type, filename=out_path.name)
