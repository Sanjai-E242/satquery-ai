# BigEarthNet.txt Parquet Dataset Inspection Report

## Overview
- **Dataset File:** `/Users/sanjai/.gemini/antigravity-ide/scratch/satquery-ai/data/BigEarthNet/BigEarthNet.txt.parquet`
- **File Size:** 445.19 MB
- **Total Rows:** 9,553,962
- **Total Columns:** 13

## Columns & Data Types
| Column Name | Data Type | Detected Purpose |
| --- | --- | --- |
| `ID` | `int64` | Image/Patch Ref |
| `s1_name` | `string` | Image/Patch Ref, Sentinel-1 SAR |
| `patch_id` | `string` | Image/Patch Ref, Sentinel-2 Optical |
| `input` | `string` | Metadata/Attribute |
| `output` | `string` | Answer/Label |
| `type` | `string` | Metadata/Attribute |
| `category` | `string` | Metadata/Attribute |
| `split` | `string` | Data Split |
| `latitude` | `double` | Metadata/Attribute |
| `longitude` | `double` | Metadata/Attribute |
| `country` | `string` | Metadata/Attribute |
| `season` | `string` | Metadata/Attribute |
| `climate_zone` | `string` | Metadata/Attribute |

## Detected Field Categories
- **Sentinel-1 (SAR) References:** `s1_name`
- **Sentinel-2 (Optical) References:** `patch_id`
- **Question/Instruction Fields:** None detected
- **Answer/Label Fields:** `output`
- **Split Information:** `split`

## Sample Records (First 3)
```json
[
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
  },
  {
    "ID": 2,
    "s1_name": "S1B_IW_GRDH_1SDV_20170612T165809_33UUP_26_57",
    "patch_id": "S2A_MSIL2A_20170613T101031_N9999_R022_T33UUP_26_57",
    "input": "Would you confirm that any broad-leaved forest borders upon pastures?",
    "output": "no",
    "type": "binary",
    "category": "adjacency",
    "split": "test",
    "latitude": 48.11003471465957,
    "longitude": 12.740300299577253,
    "country": "Austria",
    "season": "Summer",
    "climate_zone": "Cold, no dry season, warm summer"
  },
  {
    "ID": 3,
    "s1_name": "S1B_IW_GRDH_1SDV_20170612T165809_33UUP_26_57",
    "patch_id": "S2A_MSIL2A_20170613T101031_N9999_R022_T33UUP_26_57",
    "input": "Do pastures cover between 864000 square meters and 1008000 square meters of the image?",
    "output": "no",
    "type": "binary",
    "category": "area",
    "split": "test",
    "latitude": 48.11003471465957,
    "longitude": 12.740300299577253,
    "country": "Austria",
    "season": "Summer",
    "climate_zone": "Cold, no dry season, warm summer"
  }
]
```

## Adaptation Pipeline Status
- Dataset format validated.
- Schema verified for vision-language instruction tuning.
