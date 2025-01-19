from PIL import Image
import numpy as np
import cv2 as cv
from configs.cv_qr_detector import qr_detector


async def detect_and_read_qr(image: Image.Image) -> tuple[Image.Image | None, str | None]:
    image = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
    data, bbox, _ = qr_detector.detectAndDecode(image)

    if data is not False:
        # Crop the QR
        points = np.array([point for point in bbox[0]])
        x, y, w, h = cv.boundingRect(points)
        cropped_qr = image[y:y+h, x:x+w]

        # Read the QR
        return Image.fromarray(cv.cvtColor(cropped_qr, cv.COLOR_BGR2RGB)), data
    else:
        return None, None
