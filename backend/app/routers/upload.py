import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import settings
from app.geospatial.metadata import extract_image_metadata
from app.geospatial.validation import validate_image_file, validate_image_pair
from app.schemas.schemas import ImageMetadataResponse, ImageValidationResponse

router = APIRouter(prefix="/images", tags=["Image Management"])

# Memory storage for demo session images
IMAGE_DATABASE = {}

@router.post("/upload", response_model=ImageMetadataResponse)
async def upload_image(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ['.tif', '.tiff', '.geotiff', '.png', '.jpg', '.jpeg', '.webp']:
        raise HTTPException(status_code=400, detail=f"Unsupported image format: {ext}")

    img_id = f"img_{uuid.uuid4().hex[:8]}"
    clean_filename = f"{img_id}_{file.filename}"
    save_path = settings.UPLOADS_DIR / clean_filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    metadata = extract_image_metadata(str(save_path))
    metadata['id'] = img_id
    metadata['filename'] = clean_filename
    metadata['url'] = f"/storage/uploads/{clean_filename}"
    
    # Store in session registry
    IMAGE_DATABASE[img_id] = metadata
    return ImageMetadataResponse(**metadata)

@router.get("/{image_id}", response_model=ImageMetadataResponse)
async def get_image_metadata(image_id: str):
    if image_id not in IMAGE_DATABASE:
        raise HTTPException(status_code=404, detail=f"Image ID {image_id} not found.")
    return ImageMetadataResponse(**IMAGE_DATABASE[image_id])

@router.post("/validate", response_model=ImageValidationResponse)
async def validate_image_endpoint(primary_id: str, secondary_id: str = None):
    if primary_id not in IMAGE_DATABASE:
        raise HTTPException(status_code=404, detail=f"Primary image ID {primary_id} not found.")

    primary_meta = IMAGE_DATABASE[primary_id]

    if not secondary_id:
        res = validate_image_file(primary_meta['filepath'])
        return ImageValidationResponse(**res)
    else:
        if secondary_id not in IMAGE_DATABASE:
            raise HTTPException(status_code=404, detail=f"Secondary image ID {secondary_id} not found.")
        secondary_meta = IMAGE_DATABASE[secondary_id]
        res = validate_image_pair(primary_meta['filepath'], secondary_meta['filepath'])
        return ImageValidationResponse(**res)
