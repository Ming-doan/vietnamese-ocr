import os
import uuid
from PIL import Image
from fastapi.responses import JSONResponse


def get_response_format(data: dict = {}, error: str | None = None):
    return JSONResponse(
        status_code=200 if not error else 400,
        content={"data": data, "error": error},
    )


class Media:
    media_path = os.path.join(os.getcwd(), "media")

    @staticmethod
    def create_media_directory():
        os.makedirs(Media.media_path, exist_ok=True)

    @staticmethod
    def save_pil_image(image: Image.Image) -> str:
        _path = os.path.join(Media.media_path, f"{uuid.uuid4()}.jpg")
        image.save(_path)
        return f"media/{os.path.basename(_path)}"


# Initialize media
Media.create_media_directory()
