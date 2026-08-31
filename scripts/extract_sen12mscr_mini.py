import os
import json
import numpy as np
import pyarrow.parquet as pq
from PIL import Image

def extract_sen12ms_samples():
    output_dir = "data/SEN12MS"
    os.makedirs(output_dir, exist_ok=True)

    parquet_path = "/tmp/sen12ms_scene1.parquet"
    if not os.path.exists(parquet_path):
        raise FileNotFoundError(f"Parquet file not found at {parquet_path}")

    print(f"Reading local parquet file '{parquet_path}'...")
    table = pq.read_table(parquet_path)
    df = table.to_pandas()
    print(f"Parquet file loaded! Total rows: {len(df)}")

    sample_count = 0
    target_samples = 3

    for idx, row in df.iterrows():
        try:
            sar_raw = row["sar"]
            opt_raw = row["cloudy"]

            sar_shape = tuple(row["sar_shape"])
            opt_shape = tuple(row["opt_shape"])

            sar_arr = np.frombuffer(sar_raw, dtype=np.float32).reshape(sar_shape)
            opt_arr = np.frombuffer(opt_raw, dtype=np.int16).reshape(opt_shape)

            if sar_arr.shape != (256, 256, 2) or opt_arr.shape != (256, 256, 13):
                continue

            sample_count += 1
            sample_dir = os.path.join(output_dir, f"sample_{sample_count:03d}")
            os.makedirs(sample_dir, exist_ok=True)

            # Save authoritative .npy arrays
            sar_npy_path = os.path.join(sample_dir, "sar.npy")
            opt_npy_path = os.path.join(sample_dir, "optical.npy")

            np.save(sar_npy_path, sar_arr)
            np.save(opt_npy_path, opt_arr)

            # Generate SAR visualization preview PNG
            # Channel 0 is VV polarization. Clip & normalize dB values for clear visualization.
            vv_band = sar_arr[:, :, 0]
            vv_min, vv_max = np.percentile(vv_band, (2, 98))
            sar_norm = np.clip((vv_band - vv_min) / (vv_max - vv_min + 1e-6) * 255.0, 0, 255).astype(np.uint8)
            sar_img = Image.fromarray(sar_norm, mode="L")
            sar_png_path = os.path.join(sample_dir, "sar_preview.png")
            sar_img.save(sar_png_path)

            # Generate Optical RGB preview PNG (B4, B3, B2 correspond to red, green, blue)
            # In 13-band Sentinel-2 L1C/L2A: B2=idx 1, B3=idx 2, B4=idx 3
            rgb_arr = opt_arr[:, :, [3, 2, 1]].astype(np.float32)
            rgb_min, rgb_max = np.percentile(rgb_arr, (2, 98))
            rgb_norm = np.clip((rgb_arr - rgb_min) / (rgb_max - rgb_min + 1e-6) * 255.0, 0, 255).astype(np.uint8)
            opt_img = Image.fromarray(rgb_norm, mode="RGB")
            opt_png_path = os.path.join(sample_dir, "optical_preview.png")
            opt_img.save(opt_png_path)

            # Save metadata.json
            meta_path = os.path.join(sample_dir, "metadata.json")
            metadata = {
                "dataset": "SEN12MS-CR",
                "season": str(row.get("season", "fall")),
                "scene": str(row.get("scene", "scene_1")),
                "patch": str(row.get("patch", f"patch_{sample_count:03d}")),
                "sar_shape": list(sar_shape),
                "optical_shape": list(opt_shape),
                "sar_dtype": "float32",
                "optical_dtype": "int16"
            }

            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=2)

            print(f"✓ Extracted SEN12MS-CR Sample {sample_count:03d}:")
            print(f"   SAR Shape: {sar_arr.shape} ({sar_arr.dtype}), Optical Shape: {opt_arr.shape} ({opt_arr.dtype})")
            print(f"   Dir: {sample_dir}")

            if sample_count >= target_samples:
                break

        except Exception as e:
            print(f"Error parsing row {idx}: {e}")
            continue

    # Remove temp download file after extracting
    if os.path.exists(parquet_path):
        os.remove(parquet_path)
        print(f"Cleaned up temp file '{parquet_path}'.")

    print(f"SEN12MS-CR Mini Dataset Extraction Complete! Extracted {sample_count} valid paired samples.")

if __name__ == "__main__":
    extract_sen12ms_samples()
