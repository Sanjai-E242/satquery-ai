# BigEarthNet Image Asset Availability & Forensic Inspection Report

**Status:** STOPPED AT ASSET VERIFICATION (MISSING REAL IMAGE ASSET FILES)  
**Inspection Date:** 2026-08-27  
**Dataset Metadata File:** `data/BigEarthNet/BigEarthNet.txt.parquet`  

---

## 1. Parquet Metadata Inspection

- **File Path:** [`data/BigEarthNet/BigEarthNet.txt.parquet`](file:///Users/sanjai/.gemini/antigravity-ide/scratch/satquery-ai/data/BigEarthNet/BigEarthNet.txt.parquet)
- **File Size:** 445.19 MB
- **Total Parquet Rows:** 9,553,962 question-answer pairs
- **Total Unique Sentinel-2 Patches:** 590,326 distinct `patch_id` entries
- **Metadata Fields:** `ID`, `s1_name`, `patch_id`, `input`, `output`, `type`, `category`, `split`, `latitude`, `longitude`, `country`, `season`, `climate_zone`

### Sample Parquet Record:
```json
{
  "ID": 1,
  "s1_name": "S1B_IW_GRDH_1SDV_20170612T165809_33UUP_26_57",
  "patch_id": "S2A_MSIL2A_20170613T101031_N9999_R022_T33UUP_26_57",
  "input": "Would you say that any arable land lies next to pastures in the image?",
  "output": "yes",
  "type": "binary",
  "category": "adjacency",
  "split": "test",
  "latitude": 48.11003471465957,
  "longitude": 12.740300299577253,
  "country": "Austria",
  "season": "Summer",
  "climate_zone": "Cold, no dry season, warm summer"
}
```

---

## 2. Asset Availability Summary

| Asset Component | Local File / Path | Status | Count | Details |
| :--- | :--- | :--- | :--- | :--- |
| **Parquet Text Dataset** | `data/BigEarthNet/BigEarthNet.txt.parquet` | **AVAILABLE** | 9,553,962 rows | Complete VQA question-answer pair metadata |
| **Sentinel-2 Optical Images** | `data/BigEarthNet/BigEarthNet-S2/` | **MISSING** | 0 files | Patch directories & GeoTIFF/PNG files absent |
| **Sentinel-1 SAR Images** | `data/BigEarthNet/BigEarthNet-S1/` | **MISSING** | 0 files | Patch directories & GeoTIFF/PNG files absent |

---

## 3. Exact Expected Directory & File Naming Structure

To enable PyTorch training without synthetic fallbacks, real BigEarthNet satellite image assets must be placed under `data/BigEarthNet/` using one of the following standard layouts:

### Option A: Standard Multi-Band GeoTIFF Layout (Raw BigEarthNet-S2 Archive)
```text
data/BigEarthNet/
├── BigEarthNet.txt.parquet
└── BigEarthNet-S2/
    └── <patch_id>/
        ├── <patch_id>_B01.tif  (Coastal Aerosol)
        ├── <patch_id>_B02.tif  (Blue 10m)
        ├── <patch_id>_B03.tif  (Green 10m)
        ├── <patch_id>_B04.tif  (Red 10m)
        ├── <patch_id>_B05.tif  (Red Edge 1)
        ├── <patch_id>_B06.tif  (Red Edge 2)
        ├── <patch_id>_B07.tif  (Red Edge 3)
        ├── <patch_id>_B08.tif  (NIR 10m)
        ├── <patch_id>_B8A.tif  (Narrow NIR)
        ├── <patch_id>_B09.tif  (Water Vapour)
        ├── <patch_id>_B11.tif  (SWIR 1)
        ├── <patch_id>_B12.tif  (SWIR 2)
        └── <patch_id>_labels_metadata.json
```

### Option B: RGB Composite Image Layout (Preprocessed PNG / JPG)
```text
data/BigEarthNet/patches/
├── <patch_id>.png             (e.g., S2A_MSIL2A_20170613T101031_N9999_R022_T33UUP_26_57.png)
└── <s1_name>.png              (e.g., S1B_IW_GRDH_1SDV_20170612T165809_33UUP_26_57.png)
```

---

## 4. Estimated Download & Storage Requirements

- **Full BigEarthNet Archive (590,326 patches):**
  - Sentinel-2 (12-band GeoTIFFs): ~66 GB archive (~120 GB unpacked)
  - Sentinel-1 (2-band SAR GeoTIFFs): ~30 GB archive (~50 GB unpacked)
  - **Total Full Storage Required:** ~170 GB
- **Minimum Development Subset Required (for MacBook Air MPS/CPU LoRA Fine-Tuning):**
  - Sample Count: 100 to 1,000 unique Sentinel-2 RGB PNG / GeoTIFF image patches matching `patch_id` entries in `BigEarthNet.txt.parquet`.
  - **Total Development Storage Required:** **~50 MB to 500 MB**.

---

## 5. Next Steps / Actions Required

In accordance with Phase 4B Mandatory Development Rules:
1. **NO synthetic images (PIL `Image.new()`) or hardcoded dummy loss values have been created.**
2. **Execution is STOPPED until real BigEarthNet image patches are downloaded or extracted into `data/BigEarthNet/patches/` or `data/BigEarthNet/BigEarthNet-S2/`.**
3. Once a minimum subset of real image patches (100–1,000 samples) is provided, the PyTorch dataset reader (`training/finetuning/florence2_lora.py`) can be executed for real gradient-based LoRA training.
