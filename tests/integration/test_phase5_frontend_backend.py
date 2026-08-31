import os
import sys
import glob
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

from app.main import app

client = TestClient(app)

@pytest.mark.integration
def test_phase5_system_health_endpoint():
    """
    Test Phase 5 — System health and status endpoint contracts.
    """
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"

    status_res = client.get("/api/system/status")
    assert status_res.status_code == 200
    status_data = status_res.json()
    assert status_data["status"] == "READY"
    assert "components" in status_data

@pytest.mark.integration
def test_phase5_sample_dataset_endpoint():
    """
    Test Phase 5 — Sample satellite dataset loader endpoint.
    """
    res = client.get("/api/system/sample-dataset")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] in ["ready", "success"]
    assert "primary_image" in data
    assert "secondary_image" in data
    assert data["primary_image"]["id"].startswith("img_")

@pytest.mark.integration
def test_phase5_image_upload_and_validation():
    """
    Test Phase 5 — Real image upload & pair validation endpoint contracts.
    """
    png_patches = glob.glob("data/BigEarthNet/patches/*.png")
    assert len(png_patches) >= 2, "Real BigEarthNet optical PNG patches required"

    with open(png_patches[0], "rb") as f:
        up_res1 = client.post("/api/images/upload", files={"file": ("test_p1.png", f, "image/png")})
    assert up_res1.status_code == 200
    img1_meta = up_res1.json()

    with open(png_patches[1], "rb") as f:
        up_res2 = client.post("/api/images/upload", files={"file": ("test_p2.png", f, "image/png")})
    assert up_res2.status_code == 200
    img2_meta = up_res2.json()

    val_res = client.post(f"/api/images/validate?primary_id={img1_meta['id']}&secondary_id={img2_meta['id']}")
    assert val_res.status_code == 200
    val_data = val_res.json()
    assert val_data["valid"] is True

@pytest.mark.integration
def test_phase5_workflows_and_reports():
    """
    Test Phase 5 — End-to-end user workflows (VQA, Grounding, Change Analysis, Optical+SAR) & PDF/JSON Report Downloads via FastAPI.
    """
    # 1. Load sample dataset
    sample_res = client.get("/api/system/sample-dataset")
    assert sample_res.status_code == 200
    sample_data = sample_res.json()
    opt_id = sample_data["primary_image"]["id"]
    sar_id = sample_data["secondary_image"]["id"]

    # Workflow A — VQA
    vqa_res = client.post("/api/query", json={
        "query": "What is the dominant land cover class in this satellite image?",
        "analysis_mode": "single",
        "primary_image_id": opt_id
    })
    assert vqa_res.status_code == 200
    vqa_data = vqa_res.json()
    assert vqa_data["task"] == "vqa"
    assert len(vqa_data["answer"]) > 0

    # Workflow B — Grounding
    g_res = client.post("/api/query", json={
        "query": "Locate water bodies and forested areas.",
        "analysis_mode": "single",
        "primary_image_id": opt_id
    })
    assert g_res.status_code == 200
    g_data = g_res.json()
    assert g_data["task"] == "grounding"

    # Workflow C — Change Detection
    cd_res = client.post("/api/query", json={
        "query": "Identify land cover changes between T1 and T2.",
        "analysis_mode": "bi_temporal",
        "primary_image_id": opt_id,
        "secondary_image_id": opt_id
    })
    assert cd_res.status_code == 200
    cd_data = cd_res.json()
    assert cd_data["task"] == "change_analysis"

    # Workflow D — Optical + SAR Fusion
    fus_res = client.post("/api/query", json={
        "query": "Perform cross-modal optical and SAR fusion.",
        "analysis_mode": "optical_sar",
        "primary_image_id": opt_id,
        "secondary_image_id": sar_id
    })
    assert fus_res.status_code == 200
    fus_data = fus_res.json()
    exec_id = fus_data["execution_id"]

    # Report Generation PDF & JSON
    pdf_gen = client.post(f"/api/reports/generate/{exec_id}?format=pdf")
    assert pdf_gen.status_code == 200

    json_gen = client.post(f"/api/reports/generate/{exec_id}?format=json")
    assert json_gen.status_code == 200

    # Download Reports
    pdf_dl = client.get(f"/api/reports/{exec_id}/download?format=pdf")
    assert pdf_dl.status_code == 200
    assert pdf_dl.headers["content-type"] == "application/pdf"
    assert len(pdf_dl.content) > 500

    json_dl = client.get(f"/api/reports/{exec_id}/download?format=json")
    assert json_dl.status_code == 200
    assert json_dl.headers["content-type"] == "application/json"
    assert len(json_dl.content) > 200

@pytest.mark.integration
def test_phase5_optical_as_sar_rejection():
    """
    Test Phase 5 — Modality validation rejecting optical RGB image passed into SAR path.
    """
    sample_res = client.get("/api/system/sample-dataset")
    opt_id = sample_res.json()["primary_image"]["id"]

    # Submit query passing optical RGB image as secondary SAR image
    fus_res = client.post("/api/query", json={
        "query": "Perform cross-modal optical and SAR fusion.",
        "analysis_mode": "optical_sar",
        "primary_image_id": opt_id,
        "secondary_image_id": opt_id
    })

    # Must fail cleanly or raise ValueError modality exception
    assert fus_res.status_code in [400, 500] or "Invalid Modality" in fus_res.text or "ValueError" in fus_res.text
