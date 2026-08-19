from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image

# from .florence import florence_service
from .schemas import CropInspectionResponse
from .gemma4 import gemma4_service


app = FastAPI(
    title="IntelliScan AI Backend",
    description="FastAPI backend for IntelliScan Edge AI.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "IntelliScan AI Backend",
        "status": "online",
        "model": gemma4_service.model_name,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
         "model": gemma4_service.model_name,
        "device": "cpu",
    }


@app.post(
    "/api/vision/inspect",
    response_model=CropInspectionResponse,
)
async def detect_objects(
    file: UploadFile = File(...),
):
    
    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="File type could not be determined.",
        )

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are supported.",
        )

    try:
        contents = await file.read()

        image = Image.open(
            BytesIO(contents)
        ).convert("RGB")

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image: {exc}",
        )

    # Run Gemma 4 inspection
    try:
        result = gemma4_service.inspect_crop(
            image
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Gemma 4 inference failed: {exc}",
        )

    return result