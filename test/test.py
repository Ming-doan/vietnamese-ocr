from fastapi import TestClient
from main import app


ID_CARD_1_FRONT = "test/cccd_front_1.jpg"
ID_CARD_1_BACK = "test/cccd_back_1.jpg"
ID_CARD_2_FRONT = "test/cccd_front_2.jpg"
ID_CARD_2_BACK = "test/cccd_back_2.jpg"

LAND_USE_1 = "test/land_use_1.jpg"
LAND_USE_2 = "test/land_use_2.jpg"


def test_predict_id_card_1():
    with TestClient(app) as client:
        response = client.post("/api/id_card/predict", files={
            "front": open(ID_CARD_1_FRONT, "rb"),
            "back": open(ID_CARD_1_BACK, "rb")
        })
        assert response.status_code == 200, response.text
        assert "result" in response.json()
        assert "trace" in response.json()