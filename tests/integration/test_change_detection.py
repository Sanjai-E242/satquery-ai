import os
import sys
import glob
import pytest
import torch
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

def test_real_pytorch_change_detector():
    from app.models.change_detection.neural_change import NeuralChangeDetector

    detector = NeuralChangeDetector()
    loaded = detector.load()
    assert loaded is True, "NeuralChangeDetector failed to load pretrained PyTorch ResNet-18 model weights"
    assert detector.mode == "REAL_MODEL", f"Expected mode 'REAL_MODEL', got '{detector.mode}'"

    png_patches = glob.glob("data/BigEarthNet/patches/*.png")
    assert len(png_patches) >= 2, "At least 2 patch PNG files required in data/BigEarthNet/patches/"

    img_path1 = png_patches[0]
    img_path2 = png_patches[1]
    query = "Analyze bi-temporal land-cover changes between T1 and T2 imagery."

    res = detector.predict(
        inputs={
            "primary_image_path": img_path1,
            "secondary_image_path": img_path2
        },
        query=query
    )

    assert res is not None, "Neural change prediction returned None"
    assert "change_percentage" in res, "Result missing 'change_percentage' key"
    assert "change_map_path" in res, "Result missing 'change_map_path' key"
    assert "change_map_relative_url" in res, "Result missing 'change_map_relative_url' key"

    change_pct = res["change_percentage"]
    assert isinstance(change_pct, (int, float)), f"Change percentage is not a number: {change_pct}"
    assert 0.0 <= change_pct <= 100.0, f"Change percentage out of bounds [0..100]: {change_pct}"

    assert os.path.exists(res["change_map_path"]), f"Generated change map overlay file '{res['change_map_path']}' does not exist"
    assert res["mode"] == "REAL_MODEL", f"Expected mode 'REAL_MODEL', got '{res['mode']}'"
    assert res["confidence"]["type"] == "model_derived", f"Expected confidence type 'model_derived', got '{res['confidence']['type']}'"

    print("\n[Pytest Integration Pass] PyTorch Siamese Dual-Stream Change Detector Verified:")
    print("  Model:             ", res["model"])
    print("  Mode:              ", res["mode"])
    print("  Device:            ", res["device"])
    print("  Change Percentage: ", change_pct, "%")
    print("  Confidence:        ", res["confidence"])
    print("  Change Map URL:    ", res["change_map_relative_url"])
