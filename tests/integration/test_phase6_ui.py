import os
import sys
import glob
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

from app.main import app

client = TestClient(app)

@pytest.mark.integration
def test_phase6_identity_config_verification():
    """
    Test Phase 6 — Centralized identity configuration file contains exact 5-member team metadata.
    """
    identity_file = "frontend/lib/identityConfig.ts"
    assert os.path.exists(identity_file), "frontend/lib/identityConfig.ts missing"
    
    with open(identity_file, "r") as f:
      content = f.read()
    
    assert "SATQUERY AI" in content
    assert "Agentic Multimodal Intelligence for Satellite Imagery" in content
    assert "SIH26167" in content
    assert "Sanjai" in content
    assert "Rajalakshmi Engineering College" in content
    assert "Artificial Intelligence and Data Science" in content
    assert "404 Coders" in content
    assert "Sanjay" in content
    assert "Saqlain" in content
    assert "Prathesha" in content
    assert "Sujit" in content
    assert "Saravana" in content
    assert "Computer Vision & Geospatial Analysis Engineer" in content
    assert "sanjai.e.2024.aids@rajalakshmi.edu.in" in content

@pytest.mark.integration
def test_phase6_frontend_components_exist():
    """
    Test Phase 6 — All UI components exist and are intact.
    """
    required_files = [
        "frontend/app/page.tsx",
        "frontend/app/globals.css",
        "frontend/components/layout/Header.tsx",
        "frontend/components/dashboard/ProcessingPipeline.tsx",
        "frontend/components/satellite-viewer/SatelliteViewer.tsx",
        "frontend/components/chat/AIChat.tsx",
        "frontend/components/execution-trace/ExecutionTrace.tsx",
        "frontend/components/image-upload/InputPanel.tsx",
        "frontend/components/dashboard/StatusPanels.tsx",
        "frontend/lib/api.ts"
    ]
    for file_path in required_files:
        assert os.path.exists(file_path), f"Missing frontend component: {file_path}"

@pytest.mark.integration
def test_phase6_backend_api_and_report_contracts():
    """
    Test Phase 6 — FastAPI backend system status, image upload, sample dataset loader, query execution, and report endpoints.
    """
    # 1. System status
    res = client.get("/api/system/status")
    assert res.status_code == 200
    assert res.json()["status"] == "READY"

    # 2. Sample dataset loader
    sample_res = client.get("/api/system/sample-dataset")
    assert sample_res.status_code == 200
    sample_data = sample_res.json()
    assert sample_data["status"] in ["ready", "success"]
    opt_id = sample_data["primary_image"]["id"]
    sar_id = sample_data["secondary_image"]["id"]

    # 3. Query execution
    q_res = client.post("/api/query", json={
        "query": "What is the dominant land cover class?",
        "analysis_mode": "single",
        "primary_image_id": opt_id
    })
    assert q_res.status_code == 200
    exec_id = q_res.json()["execution_id"]

    # 4. Report PDF/JSON download URLs
    pdf_gen = client.post(f"/api/reports/generate/{exec_id}?format=pdf")
    assert pdf_gen.status_code == 200
    pdf_dl = client.get(f"/api/reports/{exec_id}/download?format=pdf")
    assert pdf_dl.status_code == 200
    assert pdf_dl.headers["content-type"] == "application/pdf"
