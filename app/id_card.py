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


router = APIRouter(prefix="/id_card")


@router.post("/predict")
async def predict_id_card(front: UploadFile = File(...), back: UploadFile = File(...)):
    # Intialize response
    response_error = None
    response_data = {
        "result": {},
        "trace": {}
    }

    try:
        # Read image
        front_image = Image.open(io.BytesIO(await front.read()))
        back_image = Image.open(io.BytesIO(await back.read()))

        # Extract bboxs from image
        front_bboxs = await detect_bounding_boxs(front_image)
        back_bboxs = await detect_bounding_boxs(back_image)
        if not is_production_mode():
            response_data["trace"]["all_front_bboxs"] = Media.save_pil_image(
                visualize_bbox(front_image, front_bboxs))
            response_data["trace"]["all_back_bboxs"] = Media.save_pil_image(
                visualize_bbox(back_image, back_bboxs))

        # Read template
        front_template = load_template("cccd_front")
        back_template = load_template("cccd_back")

        # Filter bboxs
        filter_front_bboxs = await filter_bbox(front_bboxs, front_template, front_image.width, front_image.height)
        filter_back_bboxs = await filter_bbox(back_bboxs, back_template, back_image.width, back_image.height)
        if not is_production_mode():
            response_data["trace"]["filter_front_bboxs"] = Media.save_pil_image(visualize_bbox(
                front_image, list(filter_front_bboxs.values()), list(filter_front_bboxs.keys())))
            response_data["trace"]["filter_back_bboxs"] = Media.save_pil_image(visualize_bbox(
                back_image, list(filter_back_bboxs.values()), list(filter_back_bboxs.keys())))

        # Crop images
        front_images = await crop_images(front_image, filter_front_bboxs, front_template.padding)
        back_images = await crop_images(back_image, filter_back_bboxs, back_template.padding)
        if not is_production_mode():
            for label, image in front_images.items():
                response_data["trace"][f"front_{label}"] = Media.save_pil_image(
                    image)
            for label, image in back_images.items():
                response_data["trace"][f"back_{label}"] = Media.save_pil_image(
                    image)

        # Predict data
        for label, image in front_images.items():
            if label not in front_template.non_prediction_labels:
                response_data["result"][label] = await predict_data(image, front_template.template[label].regex)
            else:
                response_data["result"][label] = response_data["trace"][f"front_{label}"]
        for label, image in back_images.items():
            if label not in back_template.non_prediction_labels:
                response_data["result"][label] = await predict_data(image, back_template.template[label].regex)
            else:
                response_data["result"][label] = response_data["trace"][f"back_{label}"]

    # If error occurs
    except Exception as e:
        response_error = str(e)

    if not is_production_mode():
        del response_data["trace"]

    return get_response_format(response_data, response_error)
