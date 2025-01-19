from PIL import Image
import numpy as np
from configs.paddle_ocr import ocr_model


async def detect_bounding_boxs(image: Image.Image) -> list[list[float]]:
    # Detect text bounding boxes
    return ocr_model.ocr(np.array(image), cls=True, det=True, rec=False)[0]
