import src.utils as utils
from datetime import datetime

def test_convert_to_date_time():
    date_str = "2023-10-01"
    expected_result = datetime.strptime(date_str, "%Y-%m-%d").date()
    assert utils.convert_to_date_time(date_str) == expected_result

def test_filter_hives_by_date_range():
    items = [
        {"datePlaced": "2023-01-01"},
        {"datePlaced": "2023-06-15"},
        {"datePlaced": "2023-12-31"}
    ]
    start_date_str = "2023-01-01"
    end_date_str = "2023-12-31"
    
    filtered_items = utils.filter_hives_by_date_range(items, start_date_str, end_date_str)
    assert len(filtered_items) == 3

    start_date_str = "2023-06-01"
    end_date_str = "2023-12-31"
    filtered_items = utils.filter_hives_by_date_range(items, start_date_str, end_date_str)
    assert len(filtered_items) == 2

def test_filter_crops_by_date_range():
    items = [
        {"floweringStart": "2023-04-01", "floweringEnd": "2023-04-30"},
        {"floweringStart": "2023-05-01", "floweringEnd": "2023-05-31"},
        {"floweringStart": "2023-06-01", "floweringEnd": "2023-06-30"}
    ]
    date_str = "2023-04-15"
    
    filtered_items = utils.filter_crops_by_date_range(items, date_str)
    assert len(filtered_items) == 1
    assert filtered_items[0]["floweringStart"] == "2023-04-01"
    assert filtered_items[0]["floweringEnd"] == "2023-04-30"

def test_calculate_distance():
    cords1 = (34.0522, -118.2437)  # Los Angeles
    cords2 = (36.1699, -115.1398)  # Las Vegas
    expected_distance = 370.0  # Approximate distance in km
    calculated_distance = utils.calculate_distance(cords1, cords2)
    assert abs(calculated_distance - expected_distance) < 5.0 

def test_is_valid_lat_long():
    assert utils.is_valid_lat_long(34.0522, -118.2437) is True
    assert utils.is_valid_lat_long(-91.0, 0.0) is False  
    assert utils.is_valid_lat_long(0.0, -181.0) is False 
    assert utils.is_valid_lat_long(90.0, 180.0) is True  

def test_is_crop_period_invalid():
    assert utils.is_crop_period_invalid("2023-04-01", "2023-04-30") is False
    assert utils.is_crop_period_invalid("2023-04-30", "2023-04-01") is True
    assert utils.is_crop_period_invalid("2023-05-01", "2023-05-31") is False
    assert utils.is_crop_period_invalid("2023-06-01", "2023-06-30") is False