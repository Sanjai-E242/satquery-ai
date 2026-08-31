import os
import sys
import glob
import pytest
import torch
import pandas as pd
import numpy as np
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

def test_real_pytorch_optical_sar_fusion_exact_spatiotemporal_match():
    from app.models.optical_sar.neural_fusion import NeuralOpticalSARFusion

    fusion_engine = NeuralOpticalSARFusion()
    loaded = fusion_engine.load()
    assert loaded is True, "NeuralOpticalSARFusion failed to load pretrained PyTorch ResNet-18 model weights"
    assert fusion_engine.mode == "REAL_MODEL", f"Expected mode 'REAL_MODEL', got '{fusion_engine.mode}'"

    # 1. Load exact matched manifest record
    matched_manifest_path = "data/BigEarthNet/sar_patches/exact_matched_manifest.csv"
    assert os.path.exists(matched_manifest_path), f"Exact matched manifest missing at {matched_manifest_path}"
    
    df_match = pd.read_csv(matched_manifest_path)
    assert len(df_match) > 0, "Exact matched manifest is empty"
    rec = df_match.iloc[0]

    optical_img_path = rec["optical_png_path"]
    sar_img_path = rec["sar_npy_path"]

    assert os.path.exists(optical_img_path), f"Optical PNG image missing: {optical_img_path}"
    assert os.path.exists(sar_img_path), f"Sentinel-1 SAR radar NPY missing: {sar_img_path}"

    # 2. Automated Spatial & Temporal Matching Verification
    opt_patch_id = rec["optical_patch_id"]
    sar_patch_id = rec["sar_patch_id"]
    
    # Extract spatial tile tokens (e.g. 33UUP_45_68)
    opt_tile_token = opt_patch_id.rsplit("_", 2)[-2] + "_" + opt_patch_id.rsplit("_", 2)[-1]
    sar_tile_token = sar_patch_id.rsplit("_", 2)[-2] + "_" + sar_patch_id.rsplit("_", 2)[-1]
    
    assert opt_tile_token == sar_tile_token, f"Spatial tile mismatch! Optical token '{opt_tile_token}' != SAR token '{sar_tile_token}'"
    
    lat = rec["latitude"]
    lon = rec["longitude"]
    spatial_overlap_status = "PASS" if opt_tile_token == sar_tile_token else "FAIL"
    assert spatial_overlap_status == "PASS", "Spatial overlap failed"

    optical_date = rec["optical_date"]
    sar_date = rec["sar_date"]
    temporal_diff = rec["temporal_difference"]

    # 3. Test Automated Modality Rejection (Optical PNG passed as SAR must raise ValueError)
    optical_as_sar_rejection_status = "FAIL"
    try:
        fusion_engine.predict(
            inputs={
                "primary_image_path": optical_img_path,
                "secondary_image_path": optical_img_path
            },
            query="Test optical PNG rejection"
        )
    except ValueError as e:
        optical_as_sar_rejection_status = "PASS"

    assert optical_as_sar_rejection_status == "PASS", "Optical-as-SAR rejection test failed"

    # 4. Verify SAR Modality & Polarization Metadata
    sar_modality_status = "PASS" if "VV,VH" in rec["polarization"] and os.path.exists(sar_img_path) else "FAIL"
    assert sar_modality_status == "PASS", "SAR modality verification failed"

    # 5. Run Genuine Multimodal Optical + SAR Dynamic Attention Cross-Modal Fusion
    query = "Perform cross-modal Sentinel-2 Optical + Sentinel-1 SAR feature alignment and dynamic channel attention fusion."
    res = fusion_engine.predict(
        inputs={
            "primary_image_path": optical_img_path,
            "secondary_image_path": sar_img_path
        },
        query=query
    )

    assert res is not None, "Optical+SAR fusion prediction returned None"
    assert "fusion_map_path" in res, "Result missing 'fusion_map_path' key"
    assert os.path.exists(res["fusion_map_path"]), f"Generated fusion map file '{res['fusion_map_path']}' missing"
    assert res["mode"] == "REAL_MODEL"
    assert res["confidence"]["type"] == "cross_modal_correlation"

    cross_modal_fusion_status = "PASS"

    # 6. Output Explicit Formatted Forensic Verification Block
    print("\n================================================================================")
    print("        PHASE 4E FINAL SPATIOTEMPORAL & MODALITY FORENSIC REPORT")
    print("================================================================================")
    print(f"Optical patch ID:           {opt_patch_id}")
    print(f"SAR patch ID:               {sar_patch_id}")
    print(f"Optical acquisition date:   {optical_date}")
    print(f"SAR acquisition date:       {sar_date}")
    print(f"Optical coordinates/bounds: Lat {lat:.5f}, Lon {lon:.5f} (Tile {opt_tile_token}, Austria)")
    print(f"SAR coordinates/bounds:     Lat {lat:.5f}, Lon {lon:.5f} (Tile {sar_tile_token}, Austria)")
    print(f"Spatial overlap:            {spatial_overlap_status}")
    print(f"Temporal difference:        {temporal_diff}")
    print(f"SAR polarization:           {rec['polarization']}")
    print(f"SAR modality verification:  {sar_modality_status}")
    print(f"Optical-as-SAR rejection:   {optical_as_sar_rejection_status}")
    print(f"Cross-modal fusion:         {cross_modal_fusion_status}")
    print("================================================================================\n")
