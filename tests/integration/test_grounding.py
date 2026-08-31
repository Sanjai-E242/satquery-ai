import os
import sys
import glob
import pytest
import torch
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

def test_real_florence2_grounding_adapter():
    from app.models.grounding.remote_sensing_grounding import RemoteSensingGroundingAdapter

    adapter = RemoteSensingGroundingAdapter()
    loaded = adapter.load()
    assert loaded is True, "RemoteSensingGroundingAdapter failed to load Florence-2 Base pretrained checkpoint"
    assert adapter.mode == "REAL_MODEL", f"Expected mode 'REAL_MODEL', got '{adapter.mode}'"

    png_patches = glob.glob("data/BigEarthNet/patches/*.png")
    assert len(png_patches) > 0, "No patch PNG files found in data/BigEarthNet/patches/"

    test_img_path = png_patches[0]
    query = "Highlight the main water body in the image."

    res = adapter.predict(
        inputs={"primary_image_path": test_img_path},
        query=query
    )

    assert res is not None, "Grounding prediction returned None"
    assert "bounding_box" in res, "Result missing 'bounding_box' key"
    assert "mask_path" in res, "Result missing 'mask_path' key"
    assert "mask_relative_url" in res, "Result missing 'mask_relative_url' key"

    bbox = res["bounding_box"]
    assert len(bbox) == 4, f"Bounding box should have 4 coordinates [xmin, ymin, xmax, ymax], got {bbox}"
    assert bbox[2] > bbox[0], f"Invalid x coordinates: xmax ({bbox[2]}) <= xmin ({bbox[0]})"
    assert bbox[3] > bbox[1], f"Invalid y coordinates: ymax ({bbox[3]}) <= ymin ({bbox[1]})"

    assert os.path.exists(res["mask_path"]), f"Generated mask image file '{res['mask_path']}' does not exist"
    assert res["mode"] == "REAL_MODEL", f"Expected mode 'REAL_MODEL', got '{res['mode']}'"
    assert res["confidence"]["type"] == "model_derived", f"Expected confidence type 'model_derived', got '{res['confidence']['type']}'"

    print("\n[Pytest Integration Pass] Florence-2 Pretrained Phrase Grounding Verified:")
    print("  Model:       ", res["model"])
    print("  Mode:        ", res["mode"])
    print("  Bounding Box:", bbox)
    print("  Confidence:  ", res["confidence"])
    print("  Mask URL:    ", res["mask_relative_url"])
