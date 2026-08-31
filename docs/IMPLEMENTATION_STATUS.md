# Technical Implementation Audit — SATQUERY AI

**Date**: August 27, 2026  
**System Classification**: **C. Mostly deterministic demo / algorithmic heuristic adapter platform**  
*(Architecture features real FastAPI/Next.js foundation, real BigEarthNet parquet dataset inspection, real image differencing, real PDF/JSON report generation, and real observable trace logging, but all AI vision-language, grounding, change description, and fusion models currently run on heuristic rule-based demo fallback adapters.)*

---

## Technical Audit Findings

### 1. BigEarthNet.txt.parquet
- **Exact File Path**: `/Users/sanjai/.gemini/antigravity-ide/scratch/satquery-ai/data/BigEarthNet/BigEarthNet.txt.parquet` (symlinked from `/Users/sanjai/Downloads/BigEarthNet.txt.parquet`).
- **File Read Verification**: The 445.19 MB Parquet file is actively read by PyArrow in `training/datasets/inspect_bigearthnet.py` and `backend/app/routers/system.py`.
- **Actual Row Count**: `9,553,962` rows.
- **Actual Columns**: 13 columns (`ID`, `s1_name`, `patch_id`, `input`, `output`, `type`, `category`, `split`, `latitude`, `longitude`, `country`, `season`, `climate_zone`).
- **Dataset Fields Used**: `s1_name` (Sentinel-1 reference), `patch_id` (Sentinel-2 reference), `input` (query prompt), `output` (target label/answer), `type`, `category`, `split`.
- **Image Resolution Status**: The Parquet file contains metadata and patch ID strings only. Actual raw Sentinel image patches are not stored inside the Parquet file.
- **Usage Level**: Displayed as dataset metadata, reported in system health API, and validated for data pipeline schema inspection.

### 2. Remote-Sensing VLM
- **Model Name & Class**: `RemoteSensingVQAModel` in `backend/app/models/vqa/vqa_model.py`.
- **Model Source & Checkpoint**: Custom Python wrapper; `checkpoint_path` is `None`.
- **Loaded Status**: `load()` sets `self.mode = "DEMO_MODE"`.
- **Inference Reality**: No deep learning VLM (e.g., LLaVA, Qwen-VL, PaliGemma) is loaded. `predict()` calculates basic RGB pixel averages (`greenness`, `blueness`, `brightness`) and evaluates `if` statements to return formatted text strings.
- **Fine-Tuning / LoRA**: PEFT/LoRA libraries are installed, but no training script (`train.py`) has been run, and no weight checkpoint exists.
- **Result Origin**: **Demo Fallback (Algorithmic rule-based heuristic)**.

### 3. Grounding
- **Model Name & Class**: `RemoteSensingGroundingModel` in `backend/app/models/grounding/grounding_model.py`.
- **Loaded Status**: `load()` returns `True` without loading model weights (no SAM or Grounding DINO).
- **Bounding Box / Mask Origin**: **Deterministic / Mock**. For `"water"`, it assigns a hardcoded relative bounding box `[0.15*w, 0.40*h, 0.75*w, 0.85*h]` and draws a translucent rectangle using PIL `ImageDraw`.
- **Source File**: `backend/app/models/grounding/grounding_model.py` (lines 37–56 & 63–75).

### 4. Agentic Controller
- **Query Parser**: Keyword rule matching (`QueryParser.parse_query` in `backend/app/agent/query_parser.py`).
- **Task Router & Executor**: Real routing dispatch in `AgentController.process_query` in `backend/app/agent/controller.py`.
- **Model Registry**: Static dictionary `ModelRegistry.MODELS` in `backend/app/agent/model_registry.py`.
- **Execution Trace**: Real structured log recorder producing observable step objects with execution durations and status.

### 5. Bi-Temporal Change Analysis
- **Model Reality**: No neural change detection network (e.g., BIT-CD) is loaded.
- **Image Differencing**: **REAL**. Reads both uploaded images, resizes, computes absolute pixel difference array (`np.mean(np.abs(arr1 - arr2), axis=2)`), applies a threshold (`30.0`), calculates exact changed pixel percentage (`change_pct`), and overlays a red alpha change mask.
- **Change Description**: Template formatted string using `change_pct` and query target keywords.

### 6. Optical + SAR
- **Model Reality**: No neural cross-modal transformer fusion network is loaded.
- **Image Processing**: **REAL**. Reads Optical image into RGB array, SAR image into Grayscale array, computes green index and backscatter intensity.
- **Fusion Map**: Algorithmic heuristic matrix composite `[1.5*sar, opt_feat, 0.8*(1-sar)]` rendered as a PNG overlay. Text answer is template-generated.

### 7. Confidence
- **Origin**: **HARDCODED**. Floats (`0.92`, `0.94`, `0.91`, `0.89`) embedded in python return dicts and labeled as `type: "estimated"`.

### 8. Reports
- **Reality**: **REAL**. ReportLab PDF generator (`backend/app/services/report_generator.py`) formats real session query strings, answers, confidence scores, execution step timings, and visual evidence URLs into styled PDF and JSON files.

### 9. Tests
- **Test Suite**: `tests/test_satquery.py` (8 test cases passing).
- **Tested**: API metadata, image validation, query parser, adapter fallback prediction, change map creation, fusion map creation, PDF report building.
- **Untested / Missing**: Real PyTorch VLM inference, real LoRA training loop, real SAM/Grounding DINO model inference, PostGIS database connection, benchmark evaluation (RSVQA/CDVQA).

---

## Requirement Compliance Matrix

| Requirement | Real | Demo/Mock | Partial | Missing | Evidence / Source File |
| --- | :-: | :-: | :-: | :-: | --- |
| **BigEarthNet Parquet Inspection** | ✅ | | | | `training/datasets/inspect_bigearthnet.py` (Reads 9.55M rows) |
| **BigEarthNet Model Training / LoRA** | | | | ❌ | No `train.py` executed; no LoRA checkpoint in `checkpoints/` |
| **Single-Image VQA (Remote Sensing VLM)** | | ✅ | | | `backend/app/models/vqa/vqa_model.py` (RGB mean heuristics) |
| **Text-Guided Region Grounding** | | ✅ | | | `backend/app/models/grounding/grounding_model.py` (Hardcoded bbox `[0.15w, 0.40h, ...]`) |
| **Bi-Temporal Pixel Differencing & Change Map** | ✅ | | | | `backend/app/models/change_detection/change_model.py` (Real `ImageChops.difference` & `%`) |
| **Bi-Temporal Natural Language Description** | | ✅ | | | `backend/app/models/change_detection/change_model.py` (Template text formatting) |
| **Optical + SAR Feature Processing & Composite** | | | ✅ | | `backend/app/models/optical_sar/fusion_model.py` (Real NumPy arrays, heuristic RGB composite) |
| **Optical + SAR Neural Fusion Model** | | | | ❌ | No pretrained optical-SAR neural model loaded |
| **Agent Controller Query Routing** | ✅ | | | | `backend/app/agent/query_parser.py` & `controller.py` (Keyword intent parser + router) |
| **Observable Execution Trace** | ✅ | | | | `backend/app/agent/controller.py` & `ExecutionTrace.tsx` |
| **Confidence Scoring** | | ✅ | | | Hardcoded floats (`0.91`, `0.94`, `0.89`) |
| **PDF & JSON Report Generation** | ✅ | | | | `backend/app/services/report_generator.py` (ReportLab PDF builder) |
| **Geospatial & Format Metadata Inspection** | ✅ | | | | `backend/app/geospatial/metadata.py` & `validation.py` |
| **Interactive Next.js Frontend & Viewer** | ✅ | | | | `frontend/` (Next.js 14, Tailwind CSS, Swipe Slider, Chat UI) |
