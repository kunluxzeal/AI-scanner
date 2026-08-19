from typing import Any

from pydantic import BaseModel


# class DetectionResponse(BaseModel):
#     task: str
#     model: str
#     device: str
#     inference_time: float
#     image_width: int
#     image_height: int
#     detections: dict[str, Any]

# from pydantic import BaseModel


class CropInspectionResponse(BaseModel):
    task: str
    model: str
    device: str
    inference_time: float

    image_width: int
    image_height: int

    crop: str
    external: str
    internal: str
    condition: str
    defect: str

    raw_response: str