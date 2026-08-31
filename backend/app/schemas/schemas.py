from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

class ImageMetadataResponse(BaseModel):
    id: str
    filename: str
    filepath: str
    url: Optional[str] = None
    file_size_bytes: int
    format: str
    width: int
    height: int
    bands: int
    dtype: str
    crs: Optional[str] = None
    bounds: Optional[List[float]] = None
    resolution: Optional[List[float]] = None
    modality: str  # optical, sar, multispectral, unknown
    has_geospatial: bool

class ValidationCheck(BaseModel):
    format: str
    dimensions: str
    crs: str
    alignment: str

class ImageValidationResponse(BaseModel):
    valid: bool
    warnings: List[str] = []
    errors: List[str] = []
    checks: ValidationCheck
    metadata: Optional[Dict[str, Any]] = None

class QueryRequest(BaseModel):
    query: str
    analysis_mode: str = Field("single", description="single, bi_temporal, optical_sar")
    primary_image_id: str
    secondary_image_id: Optional[str] = None

class ExecutionStep(BaseModel):
    name: str
    status: str  # pending, running, completed, failed
    duration_ms: Optional[int] = 0
    detail: Optional[str] = None

class ConfidenceInfo(BaseModel):
    value: float
    type: str  # model_derived, estimated, demo

class EvidenceItem(BaseModel):
    id: str
    title: str
    type: str  # image, mask, bounding_box, change_map, optical_sar_overlay
    url: str
    metadata: Optional[Dict[str, Any]] = {}

class AnalysisResultResponse(BaseModel):
    execution_id: str
    query: str
    answer: str
    confidence: ConfidenceInfo
    task: str
    input_type: str
    models_used: List[str]
    tools_used: List[str]
    execution_steps: List[ExecutionStep]
    evidence: List[EvidenceItem]
    duration_ms: int
    timestamp: str

class SystemStatusResponse(BaseModel):
    status: str
    version: str
    demo_mode: bool
    components: Dict[str, str]
    dataset: Dict[str, Any]
    hardware: Dict[str, Any]
