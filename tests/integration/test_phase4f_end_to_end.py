import os
import sys
import glob
import pytest
import pandas as pd
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

from app.agent.controller import AgentController
from app.services.confidence import ConfidenceEngine
from app.services.report_generator import generate_pdf_report, generate_json_report

@pytest.mark.integration
def test_phase4f_end_to_end_system_verification(tmp_path):
    """
    Phase 4F — Full System-Wide End-to-End Integration & Forensic Verification Test Suite.
    Verifies AgentController routing, real model inference across all 4 tasks (VQA, Grounding, Change Analysis, Optical+SAR Fusion),
    dynamic confidence calibration, evidence generation, and PDF/JSON report generation.
    """
    controller = AgentController()

    # 1. Prepare genuine satellite image fixtures
    png_patches = glob.glob("data/BigEarthNet/patches/*.png")
    assert len(png_patches) >= 2, "At least 2 BigEarthNet optical PNG patches required"
    
    primary_png = png_patches[0]
    secondary_png = png_patches[1]

    # Load exact matched SAR asset
    matched_manifest_path = "data/BigEarthNet/sar_patches/exact_matched_manifest.csv"
    assert os.path.exists(matched_manifest_path), "Exact matched manifest missing"
    df_matched = pd.read_csv(matched_manifest_path)
    matched_rec = df_matched.iloc[0]

    primary_meta = {
        "filename": os.path.basename(primary_png),
        "filepath": primary_png,
        "width": 120,
        "height": 120,
        "format": "PNG",
        "modality": "Optical RGB",
        "has_geospatial": True
    }

    secondary_meta = {
        "filename": os.path.basename(secondary_png),
        "filepath": secondary_png,
        "width": 120,
        "height": 120,
        "format": "PNG",
        "modality": "Optical RGB",
        "has_geospatial": True
    }

    sar_meta = {
        "filename": os.path.basename(matched_rec["sar_npy_path"]),
        "filepath": matched_rec["sar_npy_path"],
        "width": 120,
        "height": 120,
        "format": "NPY",
        "modality": "Sentinel-1 SAR Radar (VV/VH)",
        "has_geospatial": True
    }

    # =========================================================================
    # Task 1: Single-Image VQA (Pretrained / LoRA Florence-2)
    # =========================================================================
    vqa_query = "What is the dominant land cover class in this satellite image?"
    vqa_res = controller.process_query(
        query=vqa_query,
        mode="single_image",
        primary_image=primary_meta
    )

    assert vqa_res is not None, "VQA execution returned None"
    assert vqa_res.task == "vqa", f"Expected task 'vqa', got '{vqa_res.task}'"
    assert len(vqa_res.answer.strip()) > 0, "VQA answer is empty"
    assert vqa_res.confidence.type in ["model_derived", "estimated"], f"Unexpected confidence type: {vqa_res.confidence.type}"
    assert len(vqa_res.execution_steps) >= 4, "Execution steps missing"

    # =========================================================================
    # Task 2: Text-Guided Grounding & Segmentation (Florence-2 Grounding)
    # =========================================================================
    grounding_query = "Locate water bodies and forested areas in this image."
    grounding_res = controller.process_query(
        query=grounding_query,
        mode="single_image",
        primary_image=primary_meta
    )

    assert grounding_res is not None, "Grounding execution returned None"
    assert grounding_res.task == "grounding", f"Expected task 'grounding', got '{grounding_res.task}'"
    assert len(grounding_res.evidence) >= 2, "Grounding evidence items missing"
    assert grounding_res.confidence.type == "model_derived"

    # =========================================================================
    # Task 3: Bi-Temporal Change Analysis (PyTorch ResNet-18 Siamese Dual-Stream)
    # =========================================================================
    change_query = "Identify land cover changes between T1 and T2 images."
    change_res = controller.process_query(
        query=change_query,
        mode="bi_temporal",
        primary_image=primary_meta,
        secondary_image=secondary_meta
    )

    assert change_res is not None, "Change analysis execution returned None"
    assert change_res.task == "change_analysis", f"Expected task 'change_analysis', got '{change_res.task}'"
    assert len(change_res.evidence) >= 3, "Change analysis evidence items missing"
    assert change_res.confidence.type == "model_derived"

    # =========================================================================
    # Task 4: Optical + SAR Dynamic Attention Fusion (PyTorch ResNet-18 Dual-Stream)
    # =========================================================================
    fusion_query = "Perform cross-modal Sentinel-2 Optical + Sentinel-1 SAR feature alignment and dynamic channel attention fusion."
    fusion_res = controller.process_query(
        query=fusion_query,
        mode="optical_sar",
        primary_image={
            "filename": os.path.basename(matched_rec["optical_png_path"]),
            "filepath": matched_rec["optical_png_path"],
            "width": 120,
            "height": 120,
            "format": "PNG",
            "modality": "Optical RGB",
            "has_geospatial": True
        },
        secondary_image=sar_meta
    )

    assert fusion_res is not None, "Optical+SAR fusion execution returned None"
    assert fusion_res.task == "optical_sar_fusion", f"Expected task 'optical_sar_fusion', got '{fusion_res.task}'"
    assert len(fusion_res.evidence) >= 3, "Optical+SAR evidence items missing"

    # =========================================================================
    # Task 5: PDF & JSON Report Generation Engine
    # =========================================================================
    pdf_out_path = str(tmp_path / "satquery_analysis_report.pdf")
    json_out_path = str(tmp_path / "satquery_analysis_report.json")

    pdf_res = generate_pdf_report(fusion_res.dict(), pdf_out_path)
    json_res = generate_json_report(fusion_res.dict(), json_out_path)

    assert os.path.exists(pdf_res) and os.path.getsize(pdf_res) > 500, "Generated PDF report is invalid"
    assert os.path.exists(json_res) and os.path.getsize(json_res) > 200, "Generated JSON report is invalid"

    print("\n================================================================================")
    print("        PHASE 4F FULL SYSTEM-WIDE END-TO-END VERIFICATION PASSED")
    print("================================================================================")
    print("  Task 1 (VQA Model):            ", vqa_res.models_used[0])
    print("  Task 2 (Grounding Model):      ", grounding_res.models_used[0])
    print("  Task 3 (Change Model):         ", change_res.models_used[0])
    print("  Task 4 (Optical+SAR Model):    ", fusion_res.models_used[0])
    print("  PDF Report Generated:          ", pdf_res, f"({os.path.getsize(pdf_res)} bytes)")
    print("  JSON Report Generated:         ", json_res, f"({os.path.getsize(json_res)} bytes)")
    print("================================================================================\n")
