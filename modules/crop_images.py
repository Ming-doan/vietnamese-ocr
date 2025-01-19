from PIL import Image


async def crop_images(image: Image.Image, ious: dict[str, list[float]], padding: float = 15.0) -> dict[str, Image.Image]:
    images: dict[str, Image.Image] = {}
    for key in ious:
        p1, p2, p3, p4 = ious[key]
        x = int(min(p1[0], p2[0], p3[0], p4[0]) - padding)
        y = int(min(p1[1], p2[1], p3[1], p4[1]) - padding)
        w = int(max(p1[0], p2[0], p3[0], p4[0]) - x + padding)
        h = int(max(p1[1], p2[1], p3[1], p4[1]) - y + padding)
        images[key] = image.crop((x, y, x + w, y + h))
    return images
