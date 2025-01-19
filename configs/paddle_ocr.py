from paddleocr import PaddleOCR


ocr_model = PaddleOCR(use_angle_cls=False, lang="vi", use_gpu=False)
