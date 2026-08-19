import requests


API_BASE_URL = "http://localhost:8000"


def analyze_image(image_path: str) -> dict:
    """
    Send an image to the FastAPI vision endpoint
    and return the object detection result.
    """

    url = f"{API_BASE_URL}/api/vision/inspect"

    with open(image_path, "rb") as image_file:
        response = requests.post(
            url,
            files={
                "file": (
                    image_path,
                    image_file,
                    "image/jpeg",
                ),
            },
            timeout=120,
        )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    response.raise_for_status()

    return response.json()