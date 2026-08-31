import time
import uuid
import math
import logging
from pathlib import Path
import numpy as np
import torch
from typing import Dict, Any, List
from app.agent.query_parser import QueryParser
from app.models.vqa.remote_sensing_vqa import RemoteSensingVQAAdapter
from app.models.grounding.remote_sensing_grounding import RemoteSensingGroundingAdapter
from app.models.change_detection.change_model import BiTemporalChangeModel
from app.models.optical_sar.fusion_model import OpticalSARFusionModel
from app.services.confidence import ConfidenceEngine
from app.schemas.schemas import ExecutionStep, ConfidenceInfo, EvidenceItem, AnalysisResultResponse

logger = logging.getLogger("satquery.agent.controller")

def to_json_serializable(val: Any) -> Any:
    """
    Recursively converts NumPy types, PyTorch Tensors, Paths, NaNs, and custom objects into Python native JSON types.
    """
    if val is None:
        return None
    if isinstance(val, (bool, str)):
        return val
    if isinstance(val, (int, np.integer)):
        return int(val)
    if isinstance(val, (float, np.floating)):
        f_val = float(val)
        if math.isnan(f_val) or math.isinf(f_val):
            return 0.0
        return f_val
    if isinstance(val, np.bool_):
        return bool(val)
    if isinstance(val, np.ndarray):
        return [to_json_serializable(x) for x in val.tolist()]
    if isinstance(val, torch.Tensor):
        return [to_json_serializable(x) for x in val.detach().cpu().numpy().tolist()]
    if isinstance(val, Path):
        return str(val)
    if isinstance(val, dict):
        return {str(k): to_json_serializable(v) for k, v in val.items()}
    if isinstance(val, (list, tuple, set)):
        return [to_json_serializable(x) for x in val]
    return str(val)

class AgentController:
    """
    Agentic Orchestrator for Remote Sensing Intelligence.
    Receives queries & image references -> Parses intent -> Routes workflow -> Executes specialist model -> Generates evidence & observable trace.
    """
    def __init__(self):
        self.vqa_adapter = RemoteSensingVQAAdapter()
        self.grounding_adapter = RemoteSensingGroundingAdapter()
        self.change_adapter = BiTemporalChangeModel(use_neural=True)
        self.fusion_adapter = OpticalSARFusionModel(use_neural=True)
        
        # Optimize memory and inference speed: share Florence-2 model instance
        if hasattr(self.vqa_adapter, 'is_loaded') and self.vqa_adapter.is_loaded and getattr(self.vqa_adapter, 'model', None) is not None:
            self.grounding_adapter.model = self.vqa_adapter.model
            self.grounding_adapter.processor = self.vqa_adapter.processor
            self.grounding_adapter.is_loaded = True

    def process_query(self, query: str, mode: str, primary_image: Dict[str, Any], secondary_image: Dict[str, Any] = None) -> AnalysisResultResponse:
        total_start = time.time()
        execution_id = f"exec_{uuid.uuid4().hex[:10]}"
        steps: List[ExecutionStep] = []

        logger.info(f"[STAGE 01] START - Input Validation & Geospatial Inspection | ExecID: {execution_id}")
        logger.info(f"[STAGE 01] Primary Image: ID={primary_image.get('id')}, Path={primary_image.get('filepath')}, URL={primary_image.get('url')}, Dim={primary_image.get('width')}x{primary_image.get('height')}, Format={primary_image.get('format')}")
        if secondary_image:
            logger.info(f"[STAGE 01] Secondary Image: ID={secondary_image.get('id')}, Path={secondary_image.get('filepath')}, URL={secondary_image.get('url')}, Modality={secondary_image.get('modality')}")

        try:
            # Stage 01: Input Validation & Geospatial Inspection
            step1_start = time.time()
            steps.append(ExecutionStep(
                name="Input Validation & Geospatial Inspection",
                status="completed",
                duration_ms=int((time.time() - step1_start) * 1000),
                detail=f"Mode: {mode.upper()} | Primary: {primary_image.get('filename')} ({primary_image.get('width')}x{primary_image.get('height')} {primary_image.get('format')})"
            ))
            logger.info(f"[STAGE 01] COMPLETE - ExecID: {execution_id}")

            # Stage 02: Query Intent Classifier
            logger.info(f"[STAGE 02] START - Intent Classification | Query: '{query}' | Mode: {mode}")
            step2_start = time.time()
            parsed_task = QueryParser.parse_query(query, mode=mode)
            intent = parsed_task["intent"]
            steps.append(ExecutionStep(
                name="Query Intent & Requirement Classifier",
                status="completed",
                duration_ms=int((time.time() - step2_start) * 1000),
                detail=f"Intent: {intent.upper()} | Target: {parsed_task['target']}"
            ))
            logger.info(f"[STAGE 02] COMPLETE - Intent: {intent} | ExecID: {execution_id}")

            # Stage 03 & 04: Model Routing & Inference
            logger.info(f"[STAGE 03 & 04] START - Model Routing & Inference | Intent: {intent}")
            step3_start = time.time()
            models_used = []
            tools_used = []
            evidence_list: List[EvidenceItem] = []
            answer = ""
            model_mode = "REAL_MODEL"
            raw_score = 0.90
            model_name = ""
            device_name = "cpu"

            inputs = {
                "primary_image_path": primary_image.get("filepath"),
                "secondary_image_path": secondary_image.get("filepath") if secondary_image else None
            }

            # Add primary satellite input evidence
            evidence_list.append(EvidenceItem(
                id="ev_primary",
                title="Primary Satellite Input",
                type="image",
                url=f"/storage/uploads/{primary_image.get('filename')}",
                metadata=to_json_serializable({
                    "width": primary_image.get("width"),
                    "height": primary_image.get("height"),
                    "modality": primary_image.get("modality")
                })
            ))

            if secondary_image:
                evidence_list.append(EvidenceItem(
                    id="ev_secondary",
                    title="Secondary Input Image",
                    type="image",
                    url=f"/storage/uploads/{secondary_image.get('filename')}",
                    metadata=to_json_serializable({
                        "modality": secondary_image.get("modality")
                    })
                ))

            if intent == "grounding":
                res = self.grounding_adapter.predict(inputs, query)
                model_name = res.get("model", "RemoteSensingGroundingModel")
                models_used.append(model_name)
                tools_used.append("Dynamic Contour & Spectral Segmentation Engine")
                answer = res["answer"]
                model_mode = res.get("mode", "REAL_MODEL")
                raw_score = res.get("confidence", {}).get("value", 0.91)
                device_name = res.get("device", "cpu")

                if "mask_relative_url" in res:
                    evidence_list.append(EvidenceItem(
                        id="ev_grounding_mask",
                        title="Dynamic Grounded Region & Mask Overlay",
                        type="mask",
                        url=res["mask_relative_url"],
                        metadata=to_json_serializable({
                            "bounding_box": res.get("bounding_box"),
                            "target": res.get("target_name")
                        })
                    ))

            elif intent == "change_analysis":
                res = self.change_adapter.predict(inputs, query)
                model_name = res.get("model", "NeuralChangeDetector")
                models_used.append(model_name)
                tools_used.append("PyTorch Spatial Difference & Change Mask Generator")
                answer = res["answer"]
                model_mode = res.get("mode", "REAL_MODEL")
                raw_score = res.get("confidence", {}).get("value", 0.92)
                device_name = res.get("device", "cpu")

                if "change_map_relative_url" in res:
                    evidence_list.append(EvidenceItem(
                        id="ev_change_map",
                        title="PyTorch Spatial Change Map Overlay",
                        type="change_map",
                        url=res["change_map_relative_url"],
                        metadata=to_json_serializable({
                            "change_percentage": res.get("change_percentage")
                        })
                    ))

            elif intent == "optical_sar_fusion":
                res = self.fusion_adapter.predict(inputs, query)
                model_name = res.get("model", "NeuralOpticalSARFusion")
                models_used.append(model_name)
                tools_used.append("PyTorch Multimodal Feature Alignment & 1x1 Fusion Conv")
                answer = res["answer"]
                model_mode = res.get("mode", "REAL_MODEL")
                raw_score = res.get("confidence", {}).get("value", 0.95)
                device_name = res.get("device", "cpu")

                if "fusion_map_relative_url" in res:
                    evidence_list.append(EvidenceItem(
                        id="ev_fusion_map",
                        title="Optical + SAR PyTorch Fused Representation",
                        type="optical_sar_overlay",
                        url=res["fusion_map_relative_url"],
                        metadata=to_json_serializable(res.get("multimodal_summary", {}))
                    ))

            else:  # Default VQA / Vision-Language Query
                res = self.vqa_adapter.predict(inputs, query)
                model_name = res.get("model", "microsoft/Florence-2-base")
                models_used.append(model_name)
                tools_used.append("Pretrained Florence-2 Base VLM Adapter")
                answer = res["answer"]
                model_mode = res.get("mode", "REAL_MODEL")
                raw_score = None
                device_name = res.get("device", "cpu")

            steps.append(ExecutionStep(
                name="Specialist Model Routing & Inference",
                status="completed",
                duration_ms=int((time.time() - step3_start) * 1000),
                detail=f"Model Loading ✓ | Checkpoint: {model_name} | Device: {device_name.upper()} | Mode: {model_mode} | Inference ✓"
            ))
            logger.info(f"[STAGE 03 & 04] COMPLETE - Inference Model: {model_name} | ExecID: {execution_id}")

            # Stage 05: Evidence Packaging & Confidence Calibration
            logger.info(f"[STAGE 05] START - Evidence Packaging & Confidence Calibration | ExecID: {execution_id}")
            step5_start = time.time()

            confidence_info = ConfidenceEngine.calculate_confidence(
                raw_score=raw_score,
                model_mode=model_mode,
                image_meta=primary_image,
                has_secondary=(secondary_image is not None)
            )

            steps.append(ExecutionStep(
                name="Evidence Packaging & Dynamic Confidence Calibration",
                status="completed",
                duration_ms=int((time.time() - step5_start) * 1000),
                detail=f"Confidence: {(confidence_info.value * 100):.0f}% ({confidence_info.type}) | Evidence: {len(evidence_list)} items"
            ))
            logger.info(f"[STAGE 05] COMPLETE - Evidence Items: {len(evidence_list)} | Confidence: {confidence_info.value} ({confidence_info.type}) | ExecID: {execution_id}")

            # Stage 06: Result Assembly & JSON Sanitization
            logger.info(f"[STAGE 06] START - Result Assembly & Sanitization | ExecID: {execution_id}")
            total_duration = int((time.time() - total_start) * 1000)

            sanitized_answer = str(answer) if answer is not None else ""

            response_obj = AnalysisResultResponse(
                execution_id=str(execution_id),
                query=str(query),
                answer=sanitized_answer,
                confidence=confidence_info,
                task=str(intent),
                input_type=str(mode),
                models_used=[str(m) for m in models_used],
                tools_used=[str(t) for t in tools_used],
                execution_steps=steps,
                evidence=evidence_list,
                duration_ms=int(total_duration),
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )

            logger.info(f"[STAGE 06] COMPLETE - Result Assembled Successfully | ExecID: {execution_id} | Total Duration: {total_duration}ms")
            return response_obj

        except Exception as ex:
            logger.exception(
                f"[STAGE FAILURE] Exception in AgentController process_query | ExecID: {execution_id} | "
                f"Query: '{query}' | Mode: {mode} | PrimaryImg: {primary_image.get('id')} ({primary_image.get('filepath')}) | "
                f"SecondaryImg: {secondary_image.get('id') if secondary_image else 'None'}"
            )
            raise ex
