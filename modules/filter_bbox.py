import numpy as np
from templates import Template


async def filter_bbox(bboxs: list[list[float]], template: Template, w: int, h: int) -> dict[str, list[float]]:
    ious_bb: dict[str, list[float]] = {}
    # Iterate through template
    for key in template.template:
        p1 = np.array(template.template[key].bboxs[0]) * [w, h]
        p3 = np.array(template.template[key].bboxs[2]) * [w, h]
        ious_bb[key] = [p1, [p3[0], p1[1]], p3, [p1[0], p3[1]]]

        # Find the highest IoU among all bboxs
        max_iou = 0
        for bbox in bboxs:
            bbox = np.array(bbox)
            bbox_p1 = np.min(bbox, axis=0)
            bbox_p3 = np.max(bbox, axis=0)

            # Find intersection
            inter_p1 = np.maximum(p1, bbox_p1)
            inter_p3 = np.minimum(p3, bbox_p3)
            inter = np.maximum(inter_p3 - inter_p1, 0)

            # Find union
            union = (p3 - p1) * (bbox_p3 - bbox_p1) - inter

            # Find IoU
            iou = np.prod(inter) / np.prod(union)
            if iou > max_iou:
                ious_bb[key] = bbox.tolist()
                max_iou = iou

        # Reset if IoU is too low
        max_iou = 0

    return ious_bb
