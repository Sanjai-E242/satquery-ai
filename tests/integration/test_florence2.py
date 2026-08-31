import os
import sys
import pytest
from pathlib import Path
from PIL import Image

# Add project root and backend to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "backend"))

from app.models.vqa.remote_sensing_vqa import RemoteSensingVQAAdapter

@pytest.mark.integration
def test_florence2_real_inference(tmp_path):
    """
    Integration test verifying real Florence-2 Base checkpoint loading and inference.
    Requires downloaded model weights.
    """
    # 1. Create test image fixture
    img_path = tmp_path / "test_satellite.png"
    img = Image.new("RGB", (256, 256), color=(40, 160, 80))
    img.save(img_path)

    # 2. Instantiate and load adapter
    adapter = RemoteSensingVQAAdapter(model_id="microsoft/Florence-2-base")
    loaded = adapter.load()

    assert loaded is True, f"Failed to load Florence-2 checkpoint: {adapter.load_error}"
    assert adapter.mode in ["REAL_MODEL", "REMOTE_SENSING_ADAPTED"]
    assert adapter.processor is not None
    assert adapter.model is not None

    # 3. Test VQA Inference
    inputs = {"primary_image_path": str(img_path)}
    query = "What is the dominant land-cover type in this image?"
    res = adapter.predict(inputs, query)

    # 4. Verify outputs
    assert res["mode"] in ["REAL_MODEL", "REMOTE_SENSING_ADAPTED"]
    assert "Florence-2" in res["model"]
    assert res["device"] in ["mps", "cpu", "cuda"]
    assert "answer" in res and len(res["answer"].strip()) > 0
    assert "inference_time_ms" in res and res["inference_time_ms"] > 0
