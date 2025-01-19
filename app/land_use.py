import io
from PIL import Image
from fastapi import APIRouter, UploadFile, File
from templates import load_template
from configs.utils import is_production_mode
from modules.visualize_bbox import visualize_bbox
from modules.text_detector import detect_bounding_boxs
from modules.filter_bbox import filter_bbox
from modules.crop_images import crop_images
from modules.text_recognition import predict_data
from app.utils import get_response_format, Media


router = APIRouter(prefix="/land_use")


@router.post("/predict")
async def predict_land_use_document(image: UploadFile = File(...)):
    # Intialize response
    response_error = None
    response_data = {
        "result": {},
        "trace": {}
    }

    try:
        # Read image
        _image = Image.open(io.BytesIO(await image.read()))

        # Extract bboxs from image
        bboxs = await detect_bounding_boxs(_image)
        if not is_production_mode():
            response_data["trace"]["all_bboxs"] = Media.save_pil_image(
                await visualize_bbox(_image, bboxs))

        # Read template
        template = load_template("land_use_right")

        # Filter bboxs
        filter_bboxs = await filter_bbox(bboxs, template, _image.width, _image.height)
        if not is_production_mode():
            response_data["trace"]["filter_bboxs"] = Media.save_pil_image(await visualize_bbox(
                _image, list(filter_bboxs.values()), list(filter_bboxs.keys())))

        # Crop images
        images = await crop_images(_image, filter_bboxs, template.padding)
        if not is_production_mode():
            for label, img in images.items():
                response_data["trace"][f"{label}"] = Media.save_pil_image(img)

        # Predict data
        for label, img in images.items():
            if label not in template.non_prediction_labels:
                response_data["result"][label] = await predict_data(img, template.template[label].regex)
            else:
                response_data["result"][label] = response_data["trace"][f"{label}"]

    # If error occurs
    except Exception as e:
        response_error = str(e)

    if is_production_mode():
        del response_data["trace"]

    return get_response_format(response_data, response_error)
