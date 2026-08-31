import os
import sys
import pytest
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.geospatial.metadata import extract_image_metadata
from app.geospatial.validation import validate_image_file, validate_image_pair
from app.agent.query_parser import QueryParser
from app.agent.controller import AgentController
from app.services.report_generator import generate_pdf_report, generate_json_report

@pytest.fixture
def mock_images(tmp_path):
    from PIL import Image
    
    # Create optical image
    opt_path = tmp_path / "test_optical.png"
    img1 = Image.new("RGB", (256, 256), color=(40, 140, 60))
    img1.save(opt_path)
    
    # Create SAR image / T2 image
    sar_path = tmp_path / "test_sar.png"
    img2 = Image.new("RGB", (256, 256), color=(20, 40, 180))
    img2.save(sar_path)
    
    return str(opt_path), str(sar_path)

def test_geospatial_metadata(mock_images):
    opt_path, _ = mock_images
    meta = extract_image_metadata(opt_path)
    assert meta["width"] == 256
    assert meta["height"] == 256
    assert meta["format"] == "PNG"

def test_image_validation(mock_images):
    opt_path, sar_path = mock_images
    val_single = validate_image_file(opt_path)
    assert val_single["valid"] is True
    
    val_pair = validate_image_pair(opt_path, sar_path)
    assert val_pair["valid"] is True

def test_query_parser():
    p1 = QueryParser.parse_query("What is the dominant land cover?", mode="single")
    assert p1["intent"] == "vqa"
    
    p2 = QueryParser.parse_query("Highlight the water body.", mode="single")
    assert p2["intent"] == "grounding"
    
    p3 = QueryParser.parse_query("What changed between these two dates?", mode="bi_temporal")
    assert p3["intent"] == "change_analysis"
    
    p4 = QueryParser.parse_query("Use optical and SAR together", mode="optical_sar")
    assert p4["intent"] == "optical_sar_fusion"

def test_workflow_1_vqa(mock_images):
    opt_path, _ = mock_images
    controller = AgentController()
    meta = extract_image_metadata(opt_path)
    meta["id"] = "img_vqa"
    
    res = controller.process_query("What is the dominant land cover?", mode="single", primary_image=meta)
    assert res.task == "vqa"
    assert len(res.answer) > 0
    assert res.confidence.value > 0.5
    assert len(res.execution_steps) >= 4

def test_workflow_2_grounding(mock_images):
    opt_path, _ = mock_images
    controller = AgentController()
    meta = extract_image_metadata(opt_path)
    meta["id"] = "img_grounding"
    
    res = controller.process_query("Highlight the water body.", mode="single", primary_image=meta)
    assert res.task == "grounding"
    assert "Localized" in res.answer or "Water Body" in res.answer
    assert any(e.type == "mask" for e in res.evidence)

def test_workflow_3_bitemporal_change(mock_images):
    opt_path, sar_path = mock_images
    controller = AgentController()
    meta1 = extract_image_metadata(opt_path)
    meta1["id"] = "img_t1"
    meta2 = extract_image_metadata(sar_path)
    meta2["id"] = "img_t2"
    
    res = controller.process_query("What changed between these two dates?", mode="bi_temporal", primary_image=meta1, secondary_image=meta2)
    assert res.task == "change_analysis"
    assert any(e.type == "change_map" for e in res.evidence)

def test_workflow_4_optical_sar(mock_images):
    opt_path, sar_path = mock_images
    controller = AgentController()
    meta1 = extract_image_metadata(opt_path)
    meta1["id"] = "img_opt"
    meta2 = extract_image_metadata(sar_path)
    meta2["id"] = "img_sar"
    
    res = controller.process_query("Use optical and SAR together", mode="optical_sar", primary_image=meta1, secondary_image=meta2)
    assert res.task == "optical_sar_fusion"
    assert any(e.type == "optical_sar_overlay" for e in res.evidence)

def test_report_generation(mock_images, tmp_path):
    opt_path, _ = mock_images
    controller = AgentController()
    meta = extract_image_metadata(opt_path)
    meta["id"] = "img_report"
    
    res = controller.process_query("What is the dominant land cover?", mode="single", primary_image=meta)
    pdf_out = str(tmp_path / "test_report.pdf")
    json_out = str(tmp_path / "test_report.json")
    
    generate_pdf_report(res.model_dump(), pdf_out)
    generate_json_report(res.model_dump(), json_out)
    
    assert os.path.exists(pdf_out) and os.path.getsize(pdf_out) > 0
    assert os.path.exists(json_out) and os.path.getsize(json_out) > 0
