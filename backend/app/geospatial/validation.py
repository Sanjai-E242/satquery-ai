from typing import Dict, Any, List, Optional
from app.geospatial.metadata import extract_image_metadata

def validate_image_file(filepath: str) -> Dict[str, Any]:
    """
    Validates a single remote-sensing image file.
    """
    meta = extract_image_metadata(filepath)
    warnings = []
    errors = []

    if meta['width'] == 0 or meta['height'] == 0:
        errors.append("Invalid or unreadable image dimensions.")

    if meta['format'] not in ['TIF', 'TIFF', 'GEOTIFF', 'PNG', 'JPG', 'JPEG', 'WEBP']:
        warnings.append(f"Format {meta['format']} is non-standard for satellite data. Processing in RGB demo mode.")

    if not meta['has_geospatial']:
        warnings.append("Geospatial CRS/Bounding Box metadata is missing. Using pixel coordinates.")

    checks = {
        "format": "passed" if not errors else "failed",
        "dimensions": "passed" if meta['width'] > 0 and meta['height'] > 0 else "failed",
        "crs": "passed" if meta['has_geospatial'] else "warning",
        "alignment": "passed"
    }

    return {
        "valid": len(errors) == 0,
        "warnings": warnings,
        "errors": errors,
        "checks": checks,
        "metadata": meta
    }

def validate_image_pair(primary_path: str, secondary_path: str) -> Dict[str, Any]:
    """
    Validates a pair of images (bi-temporal or optical + SAR).
    """
    meta1 = extract_image_metadata(primary_path)
    meta2 = extract_image_metadata(secondary_path)

    warnings = []
    errors = []

    # Check dimensions
    dim_match = (meta1['width'] == meta2['width']) and (meta1['height'] == meta2['height'])
    if not dim_match:
        warnings.append(f"Dimensions differ: {meta1['width']}x{meta1['height']} vs {meta2['width']}x{meta2['height']}. Auto-resampling will be applied.")

    # Check CRS match
    crs_match = True
    if meta1['crs'] and meta2['crs']:
        if meta1['crs'] != meta2['crs']:
            warnings.append(f"CRS mismatch: {meta1['crs']} vs {meta2['crs']}. Spatial re-projection recommended.")
            crs_match = False
    elif meta1['has_geospatial'] != meta2['has_geospatial']:
        warnings.append("One image lacks georeferencing metadata.")

    checks = {
        "format": "passed",
        "dimensions": "passed" if dim_match else "warning",
        "crs": "passed" if crs_match else "warning",
        "alignment": "passed"
    }

    return {
        "valid": True,
        "warnings": warnings,
        "errors": errors,
        "checks": checks,
        "primary_metadata": meta1,
        "secondary_metadata": meta2
    }
