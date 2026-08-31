import os
import pandas as pd
import torch
from torch.utils.data import Dataset
from PIL import Image
from typing import Tuple, Dict, Any, List, Optional

class BigEarthNetVQADataset(Dataset):
    """
    PyTorch Dataset for BigEarthNet Real Remote-Sensing Satellite Image VQA pairs.
    Reads verified real RGB PNG patches from data/BigEarthNet/patches/ and text from subset_manifest.csv.
    """
    def __init__(
        self,
        manifest_path: str = "data/BigEarthNet/subset_manifest.csv",
        patches_dir: str = "data/BigEarthNet/patches",
        split: str = "train",
        val_ratio: float = 0.2,
        seed: int = 42,
        max_samples: Optional[int] = None
    ):
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifest CSV not found at '{manifest_path}'")

        df = pd.read_csv(manifest_path)
        self.patches_dir = patches_dir

        # 1. Filter QA pairs where actual patch image file exists on disk
        valid_rows = []
        unique_patches = set()
        for idx, row in df.iterrows():
            pid = str(row['patch_id'])
            img_path = os.path.join(patches_dir, f"{pid}.png")
            if os.path.exists(img_path) and os.path.getsize(img_path) > 100:
                valid_rows.append(row)
                unique_patches.add(pid)

        valid_df = pd.DataFrame(valid_rows)
        if valid_df.empty:
            raise ValueError(f"No valid patch images found in '{patches_dir}' matching manifest.")

        # 2. Deterministic Train / Validation Split by Unique Patch ID to prevent leakage
        unique_patch_list = sorted(list(unique_patches))
        g = torch.Generator().manual_seed(seed)
        shuffled_indices = torch.randperm(len(unique_patch_list), generator=g).tolist()
        
        num_val = int(len(unique_patch_list) * val_ratio)
        val_patch_ids = set([unique_patch_list[i] for i in shuffled_indices[:num_val]])
        train_patch_ids = set([unique_patch_list[i] for i in shuffled_indices[num_val:]])

        if split == "train":
            split_df = valid_df[valid_df['patch_id'].isin(train_patch_ids)].copy()
        else:
            split_df = valid_df[valid_df['patch_id'].isin(val_patch_ids)].copy()

        if max_samples and max_samples < len(split_df):
            split_df = split_df.iloc[:max_samples]

        self.samples = split_df.to_dict('records')
        self.split = split
        self.total_patches = len(unique_patches)
        self.total_qa_rows = len(valid_df)
        self.train_patch_count = len(train_patch_ids)
        self.val_patch_count = len(val_patch_ids)

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        row = self.samples[idx]
        pid = str(row['patch_id'])
        img_path = os.path.join(self.patches_dir, f"{pid}.png")
        
        image = Image.open(img_path).convert("RGB")
        prompt = f"<VQA> {row['input']}"
        target = str(row['output'])

        return {
            "image": image,
            "prompt": prompt,
            "target": target,
            "patch_id": pid,
            "category": str(row.get("category", "")),
            "image_path": img_path
        }

def get_datasets(
    manifest_path: str = "data/BigEarthNet/subset_manifest.csv",
    patches_dir: str = "data/BigEarthNet/patches",
    val_ratio: float = 0.2,
    seed: int = 42
) -> Tuple[BigEarthNetVQADataset, BigEarthNetVQADataset]:
    train_ds = BigEarthNetVQADataset(manifest_path, patches_dir, split="train", val_ratio=val_ratio, seed=seed)
    val_ds = BigEarthNetVQADataset(manifest_path, patches_dir, split="val", val_ratio=val_ratio, seed=seed)

    print("=== BIGEARTHNET REAL DATASET SPLIT SUMMARY ===")
    print(f"Total image patches:  {train_ds.total_patches}")
    print(f"Total QA rows:       {train_ds.total_qa_rows}")
    print(f"Train samples (rows): {len(train_ds)} (across {train_ds.train_patch_count} patches)")
    print(f"Validation samples:   {len(val_ds)} (across {val_ds.val_patch_count} patches)")
    return train_ds, val_ds

if __name__ == "__main__":
    t_ds, v_ds = get_datasets()
    sample = t_ds[0]
    print("\nSample Item 0:")
    print("  Image size:", sample['image'].size)
    print("  Prompt:", sample['prompt'])
    print("  Target:", sample['target'])
