import json
import logging
from fastapi import APIRouter, HTTPException
from app.config import settings
from app.agent.controller import AgentController
from app.routers.upload import IMAGE_DATABASE
from app.schemas.schemas import QueryRequest, AnalysisResultResponse

router = APIRouter(prefix="/query", tags=["Query & Execution"])

logger = logging.getLogger("satquery.query")
_agent_controller = None
RESULTS_DATABASE = {}

def get_agent_controller() -> AgentController:
    global _agent_controller
    if _agent_controller is None:
        _agent_controller = AgentController()
    return _agent_controller

@router.post("", response_model=AnalysisResultResponse)
async def process_natural_language_query(req: QueryRequest):
    if req.primary_image_id not in IMAGE_DATABASE:
        logger.error(f"Image ID '{req.primary_image_id}' not found in IMAGE_DATABASE")
        raise HTTPException(
            status_code=404, 
            detail=f"Primary image ID '{req.primary_image_id}' not found in database. Please re-upload or reload sample dataset."
        )

    primary_meta = IMAGE_DATABASE[req.primary_image_id]
    secondary_meta = IMAGE_DATABASE.get(req.secondary_image_id) if req.secondary_image_id else None

    controller = get_agent_controller()
    try:
        result = controller.process_query(
            query=req.query,
            mode=req.analysis_mode,
            primary_image=primary_meta,
            secondary_image=secondary_meta
        )
        result_dump = result.model_dump()
        RESULTS_DATABASE[result.execution_id] = result_dump
        
        # Persist report JSON to outputs directory so it survives server reloads
        try:
            out_json = settings.OUTPUTS_DIR / f"satquery_report_{result.execution_id}.json"
            with open(out_json, "w") as f:
                json.dump(result_dump, f, indent=2)
        except Exception as save_err:
            logger.warning(f"Could not persist result to disk: {save_err}")

        return result
    except ValueError as val_err:
        logger.warning(f"Validation error in query processing: {val_err}")
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        logger.error(f"Model execution error: {err}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Model execution error: {str(err)}")

@router.get("/results/{execution_id}", response_model=AnalysisResultResponse)
async def get_execution_result(execution_id: str):
    if execution_id in RESULTS_DATABASE:
        return AnalysisResultResponse(**RESULTS_DATABASE[execution_id])
    
    # Check disk fallback
    candidates = [execution_id, f"exec_{execution_id}"]
    for cid in candidates:
        disk_path = settings.OUTPUTS_DIR / f"satquery_report_{cid}.json"
        if disk_path.exists():
            try:
                with open(disk_path, "r") as f:
                    data = json.load(f)
                    RESULTS_DATABASE[cid] = data
                    return AnalysisResultResponse(**data)
            except Exception:
                pass

    raise HTTPException(status_code=404, detail=f"Execution ID '{execution_id}' not found.")
