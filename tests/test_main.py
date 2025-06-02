from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime

from src.error import IS_ERROR, IS_SUCCESS
import src.utils as utils
from src.main import app
client = TestClient(app)

@patch("src.database.db.register")
def test_register_hive(mock_register):
    response = client.post("/api/hives", json={
        "hiveId": "hive123",
        "datePlaced": "2023-10-01",
        "latitude": 34.0522,
        "longitude": -118.2437,
        "numColonies": 5
    })
    assert response.status_code == 200
    assert response.json() == IS_SUCCESS["HIVE_REG_SUCCESS"]
    assert response.json()["message"] == "Hive registered successfully"
    mock_register.assert_called_once()

@patch("src.database.db.register")
def test_register_hive_invalid_lat_long(mock_register):
    response = client.post("/api/hives", json={
        "hiveId": "hive123",
        "datePlaced": "2023-10-01",
        "latitude": 100.0,  # Invalid latitude
        "longitude": -118.2437,
        "numColonies": 5
    })
    assert response.status_code == 400
    assert response.json() == IS_ERROR["INVALID_LAT_LONG"]
    mock_register.assert_not_called()

@patch("src.database.db.register")
def test_register_hive_already_exists(mock_register):
    mock_register.side_effect = ValueError(IS_ERROR["HIVE_ALREADY_EXISTS"]["message"])
    response = client.post("/api/hives", json={
        "hiveId": "hive123",
        "datePlaced": "2023-10-01",
        "latitude": 34.0522,
        "longitude": -118.2437,
        "numColonies": 5
    })
    assert response.status_code == 400
    assert response.json() == IS_ERROR["HIVE_ALREADY_EXISTS"]
    mock_register.assert_called_once()

@patch("src.database.db.get_all")
def test_get_hives(mock_get_hives):
    mock_get_hives.return_value = [
        {
            "hiveId": "hive123",
            "datePlaced": "2023-10-01",
            "latitude": 34.0522,
            "longitude": -118.2437,
            "numColonies": 5
        }
    ]
    
    response = client.get("/api/hives",params={
        "startDate": "2023-01-01",
        "endDate": "2023-12-31"
    })
    assert response.status_code == 200
    assert response.json() == {
        "message": IS_SUCCESS["HIVES_RETRIEVED"]["message"],
        "hives": mock_get_hives.return_value
    }
    mock_get_hives.assert_called_once()

@patch("src.database.db.register")
def test_register_crop(mock_register):
    response = client.post("/api/crops", json={
        "name": "Sunflower",
        "floweringStart": "2025-04-10",
        "floweringEnd": "2025-04-25",
        "latitude": 26.9124,
        "longitude": 75.7873,
        "recommendedHiveDensity": 5
    })
    assert response.status_code == 200
    assert response.json() == IS_SUCCESS["CROP_REG_SUCCESS"]
    mock_register.assert_called_once()

@patch("src.database.db.register")
def test_get_nearby_crop(mock_register):
    mock_register.return_value = "crop123"
    response = client.post("/api/crops", json={
        "name": "Sunflower",
        "floweringStart": "2025-04-10",
        "floweringEnd": "2025-04-25",
        "latitude": 26.9124,
        "longitude": 75.7873,
        "recommendedHiveDensity": 5
    })
    assert response.status_code == 200
    assert response.json() == IS_SUCCESS["CROP_REG_SUCCESS"]
    response = client.get("/api/crops/nearby", params={
        "latitude": 26.9124,
        "longitude": 75.7873,
        "radius": 1000,
        "date": utils.convert_to_date_time("2025-04-15")
    })
    mock_register.assert_called_once()
    assert response.status_code == 200
    assert response.json() == IS_SUCCESS["CROPS_RETRIEVED"]
    mock_register.assert_called_once()