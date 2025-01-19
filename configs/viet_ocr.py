from vietocr.predict import Predictor
from vietocr.tool.config import Cfg

_config = Cfg.load_config_from_name("vgg_transformer")
_config['cnn']['pretrained'] = False
_config['device'] = 'cpu'
text_recognition_model = Predictor(_config)
