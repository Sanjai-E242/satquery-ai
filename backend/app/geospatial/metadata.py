import os
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image

try:
    import rasterio
    RASTERIO_AVAILABLE = True
except ImportError:
    RASTERIO_AVAILABLE = False

def extract_image_metadata(filepath: str) -> Dict[str, Any]:
    """
    Extracts structured geospatial or optical metadata from satellite image.
    Supports GeoTIFF, TIFF, PNG, JPEG.
    """
    file_path = Path(filepath)
    filename = file_path.name
    file_size = file_path.stat().st_size
    ext = file_path.suffix.lower()

    metadata = {
        "filename": filename,
        "filepath": str(file_path),
        "file_size_bytes": file_size,
        "format": ext.replace(".", "").upper(),
        "width": 0,
        "height": 0,
        "bands": 1,
        "dtype": "unknown",
        "crs": None,
        "bounds": None,
        "resolution": None,
        "modality": "unknown",
        "has_geospatial": False
    }

    # Detect modality from filename hints
    name_lower = filename.lower()
    if any(k in name_lower for k in ['s1', 'sar', 'radar', 'vv', 'vh', 'risat']):
        metadata['modality'] = 'sar'
    elif any(k in name_lower for k in ['s2', 'opt', 'rgb', 'cartosat', 'msi']):
        metadata['modality'] = 'optical'
    else:
        metadata['modality'] = 'optical'

    if RASTERIO_AVAILABLE and ext in ['.tif', '.tiff', '.geotiff']:
        try:
            with rasterio.open(filepath) as dataset:
                metadata['width'] = dataset.width
                metadata['height'] = dataset.height
                metadata['bands'] = dataset.count
                metadata['dtype'] = str(dataset.dtypes[0])
                
                if dataset.crs:
                    metadata['crs'] = str(dataset.crs)
                    metadata['has_geospatial'] = True
                    b = dataset.bounds
                    metadata['bounds'] = [b.left, b.bottom, b.right, b.top]
                    res = dataset.res
                    metadata['resolution'] = [res[0], res[1]]
                return metadata
        except Exception:
            pass

    # Fallback using PIL
    try:
        with Image.open(filepath) as img:
            metadata['width'] = img.width
            metadata['height'] = img.height
            bands_count = len(img.getbands())
            metadata['bands'] = bands_count
            metadata['dtype'] = str(img.mode)
            if bands_count == 1 and metadata['modality'] == 'unknown':
                metadata['modality'] = 'sar'
    except Exception as e:
        print(f"Error opening image with PIL: {e}")

    return metadata
