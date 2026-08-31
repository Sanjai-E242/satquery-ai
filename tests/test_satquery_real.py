import os
import sys
import pytest
from pathlib import Path

# Add project root and backend to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "backend"))

from app.geospatial.metadata import extract_image_metadata
from app.geospatial.validation import validate_image_file, validate_image_pair
from app.models.vqa.remote_sensing_vqa import RemoteSensingVQAAdapter
from app.models.grounding.remote_sensing_grounding import RemoteSensingGroundingAdapter
from app.models.change_detection.neural_change import NeuralChangeDetector
from app.models.optical_sar.neural_fusion import NeuralOpticalSARFusion
from app.agent.model_registry import ModelRegistry
from app.agent.controller import AgentController
from app.services.confidence import ConfidenceEngine
from training.datasets.bigearthnet import BigEarthNetDataset

@pytest.fixture
def mock_images(tmp_path):
    from PIL import Image
    opt_path = tmp_path / "test_optical.png"
    img1 = Image.new("RGB", (256, 256), color=(40, 180, 60))
    img1.save(opt_path)
    
    sar_path = tmp_path / "test_sar.png"
    img2 = Image.new("RGB", (256, 256), color=(10, 40, 200))
    img2.save(sar_path)
    
    return str(opt_path), str(sar_path)

def test_bigearthnet_dataset_loading():
    parquet_path = "data/BigEarthNet/BigEarthNet.txt.parquet"
    if os.path.exists(parquet_path):
        ds = BigEarthNetDataset(parquet_path, split="test", max_samples=10)
        assert len(ds) > 0
        sample = ds[0]
        assert "input_text" in sample and "target_text" in sample
        assert "s1_name" in sample and "patch_id" in sample

def test_vqa_fine_tuned_checkpoint():
    vqa = RemoteSensingVQAAdapter()
    loaded = vqa.load()
    assert loaded is True
    assert vqa.mode in ["REMOTE_SENSING_ADAPTED", "DEMO_MODE"]
    info = vqa.get_info()
    assert "name" in info and "status" in info

def test_real_dynamic_grounding(mock_images):
    opt_path, _ = mock_images
    grounding = RemoteSensingGroundingAdapter()
    grounding.load()
    res = grounding.predict({"primary_image_path": opt_path}, "Highlight the water body.")
    
    assert res["mode"] == "REAL_MODEL"
    assert "boxes" in res and len(res["boxes"]) > 0
    bbox = res["boxes"][0]
    assert len(bbox) == 4
    assert bbox[0] >= 0 and bbox[1] >= 0
    assert os.path.exists(res["mask_path"])

def test_pytorch_neural_change_detection(mock_images):
    opt_path, sar_path = mock_images
    detector = NeuralChangeDetector()
    detector.load()
    res = detector.predict({"primary_image_path": opt_path, "secondary_image_path": sar_path}, "What changed?")
    
    assert res["mode"] == "REAL_MODEL"
    assert "change_percentage" in res
    assert os.path.exists(res["change_map_path"])

def test_pytorch_neural_optical_sar_fusion(mock_images):
    opt_path, sar_path = mock_images
    fusion = NeuralOpticalSARFusion()
    fusion.load()
    res = fusion.predict({"primary_image_path": opt_path, "secondary_image_path": sar_path}, "Use optical and SAR together.")
    
    assert res["mode"] == "REAL_MODEL"
    assert "fusion_map_path" in res
    assert os.path.exists(res["fusion_map_path"])

def test_confidence_engine():
    conf = ConfidenceEngine.calculate_confidence(raw_score=0.92, model_mode="REAL_MODEL")
    assert conf.value >= 0.90
    assert conf.type == "model_derived"

def test_model_registry():
    models = ModelRegistry.list_models()
    assert len(models) == 4
    for m in models:
        assert "mode" in m and "device" in m and "supports_cpu" in m

def test_agent_controller_real_workflow(mock_images):
    opt_path, sar_path = mock_images
    controller = AgentController()
    meta1 = extract_image_metadata(opt_path)
    meta1["id"] = "img1"
    meta2 = extract_image_metadata(sar_path)
    meta2["id"] = "img2"

    res = controller.process_query("Highlight the water body.", mode="single", primary_image=meta1)
    assert res.task == "grounding"
    assert len(res.execution_steps) >= 4
    assert any("Mode:" in step.detail for step in res.execution_steps if step.detail)
