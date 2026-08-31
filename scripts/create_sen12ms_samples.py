import os
import json
import numpy as np
from PIL import Image

def generate_sen12ms_samples():
    base_dir = "data/SEN12MS"
    os.makedirs(base_dir, exist_ok=True)

    sample_configs = [
        {"id": "sample_001", "season": "summer", "scene": "scene_101", "patch": "patch_001", "opt_seed": 42, "sar_seed": 142},
        {"id": "sample_002", "season": "fall", "scene": "scene_102", "patch": "patch_002", "opt_seed": 43, "sar_seed": 143},
        {"id": "sample_003", "season": "spring", "scene": "scene_103", "patch": "patch_003", "opt_seed": 44, "sar_seed": 144},
    ]

    for cfg in sample_configs:
        sample_dir = os.path.join(base_dir, cfg["id"])
        os.makedirs(sample_dir, exist_ok=True)

        # 1. Optical 13-band array (256, 256, 13) int16
        np.random.seed(cfg["opt_seed"])
        # Base reflectance values (1000 - 4000 int16)
        opt_arr = np.random.randint(800, 3500, size=(256, 256, 13), dtype=np.int16)
        # Add realistic spatial patterns for vegetation and urban structures
        y, x = np.ogrid[:256, :256]
        pattern1 = (np.sin(x / 20.0) + np.cos(y / 20.0)) * 500
        pattern2 = (np.cos(x / 10.0) * np.sin(y / 10.0)) * 800
        for b in range(13):
            opt_arr[:, :, b] = np.clip(opt_arr[:, :, b] + pattern1 + pattern2, 100, 10000).astype(np.int16)

        # Save optical.npy
        opt_npy_path = os.path.join(sample_dir, "optical.npy")
        np.save(opt_npy_path, opt_arr)

        # 2. SAR 2-channel array (256, 256, 2) float32 (VV and VH backscatter in dB: -25 to +5 dB)
        np.random.seed(cfg["sar_seed"])
        vv_channel = -12.0 + np.random.normal(0, 3.0, size=(256, 256)) + (pattern1 / 100.0)
        vh_channel = -18.0 + np.random.normal(0, 2.5, size=(256, 256)) + (pattern2 / 100.0)
        sar_arr = np.stack([vv_channel, vh_channel], axis=-1).astype(np.float32)

        # Save sar.npy
        sar_npy_path = os.path.join(sample_dir, "sar.npy")
        np.save(sar_npy_path, sar_arr)

        # 3. Generate SAR preview PNG (Channel 0 VV normalized)
        vv_band = sar_arr[:, :, 0]
        vv_min, vv_max = np.percentile(vv_band, (2, 98))
        sar_norm = np.clip((vv_band - vv_min) / (vv_max - vv_min + 1e-6) * 255.0, 0, 255).astype(np.uint8)
        sar_img = Image.fromarray(sar_norm, mode="L")
        sar_img.save(os.path.join(sample_dir, "sar_preview.png"))

        # 4. Generate Optical preview PNG (RGB B4, B3, B2)
        rgb_arr = opt_arr[:, :, [3, 2, 1]].astype(np.float32)
        rgb_min, rgb_max = np.percentile(rgb_arr, (2, 98))
        rgb_norm = np.clip((rgb_arr - rgb_min) / (rgb_max - rgb_min + 1e-6) * 255.0, 0, 255).astype(np.uint8)
        opt_img = Image.fromarray(rgb_norm, mode="RGB")
        opt_img.save(os.path.join(sample_dir, "optical_preview.png"))

        # 5. Metadata.json
        meta = {
            "dataset": "SEN12MS-CR",
            "season": cfg["season"],
            "scene": cfg["scene"],
            "patch": cfg["patch"],
            "sar_shape": [256, 256, 2],
            "optical_shape": [256, 256, 13],
            "sar_dtype": "float32",
            "optical_dtype": "int16"
        }
        with open(os.path.join(sample_dir, "metadata.json"), "w") as f:
            json.dump(meta, f, indent=2)

        print(f"✓ Created SEN12MS-CR {cfg['id']}: SAR {sar_arr.shape} ({sar_arr.dtype}), Optical {opt_arr.shape} ({opt_arr.dtype})")

    print("All 3 SEN12MS-CR samples created successfully!")

if __name__ == "__main__":
    generate_sen12ms_samples()
