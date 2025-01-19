from PIL import Image
import numpy as np
import cv2 as cv


async def visualize_bbox(image: Image.Image, bboxs: list[list[float]], labels: list[str] | None = None) -> Image.Image:
    image = np.array(image)
    for i, bbox in enumerate(bboxs):
        if len(bbox) > 0:
            p1, p2, p3, p4 = bbox
            # Draw polygon
            cv.polylines(image, [np.array([p1, p2, p3, p4], np.int32)],
                         isClosed=True, color=(0, 255, 0), thickness=2)
            # Draw label if available
            if labels:
                cv.putText(image, labels[i], (int(p1[0]), int(
                    p1[1]) - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    return Image.fromarray(image)
