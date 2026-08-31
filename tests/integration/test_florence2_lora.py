import os
import sys
import glob
import pytest
import torch
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

def test_florence2_lora_checkpoint_and_inference():
    checkpoint_dir = "checkpoints/rs_vlm_lora"
    assert os.path.exists(checkpoint_dir), f"Checkpoint directory '{checkpoint_dir}' does not exist"

    # 1. Verify weight tensor files exist
    saved_files = os.listdir(checkpoint_dir)
    weight_files = [f for f in saved_files if f.endswith(".safetensors") or f.endswith(".bin")]
    assert len(weight_files) > 0, f"No weight tensor file (.safetensors / .bin) found in '{checkpoint_dir}'"

    weight_path = os.path.join(checkpoint_dir, weight_files[0])
    weight_size_bytes = os.path.getsize(weight_path)
    assert weight_size_bytes > 100, f"Weight tensor file '{weight_path}' is empty or invalid ({weight_size_bytes} bytes)"

    # 2. Verify RemoteSensingVQAAdapter loads LoRA adapter cleanly
    from app.models.vqa.remote_sensing_vqa import RemoteSensingVQAAdapter

    adapter = RemoteSensingVQAAdapter(lora_dir=checkpoint_dir)
    loaded = adapter.load()
    assert loaded is True, "RemoteSensingVQAAdapter failed to load model/adapter"
    assert adapter.mode == "REMOTE_SENSING_ADAPTED", f"Expected mode 'REMOTE_SENSING_ADAPTED', got '{adapter.mode}'"

    # 3. Test real satellite image VQA inference
    png_patches = glob.glob("data/BigEarthNet/patches/*.png")
    assert len(png_patches) > 0, "No patch PNG files found in data/BigEarthNet/patches/"
    
    test_img_path = png_patches[0]
    result = adapter.predict(
        inputs={"primary_image_path": test_img_path},
        query="What is the dominant land-cover type in this image?"
    )

    assert result is not None, "Inference returned None"
    assert "answer" in result, "Result dictionary missing 'answer' key"
    assert isinstance(result["answer"], str), "Answer is not a string"
    assert len(result["answer"].strip()) > 0, "Answer string is empty"
    assert result["mode"] == "REMOTE_SENSING_ADAPTED", f"Expected inference mode 'REMOTE_SENSING_ADAPTED', got '{result['mode']}'"

    print("\n[Pytest Integration Pass] LoRA Checkpoint Verified & Adapter Inference Succeeded:")
    print("  Weight File:", weight_files[0], f"({weight_size_bytes:,} bytes)")
    print("  Mode:       ", result["mode"])
    print("  Model:      ", result["model"])
    print("  Answer:     ", result["answer"])
