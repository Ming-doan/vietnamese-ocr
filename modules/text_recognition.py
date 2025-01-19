import re
from PIL import Image
from configs.viet_ocr import text_recognition_model


async def predict_data(image: Image.Image, regex: str | None = None) -> str | None:
    result = text_recognition_model.predict(image)
    if regex:
        _match = re.search(regex, result)
        if _match:
            return _match.group()
        else:
            return None
    return result
