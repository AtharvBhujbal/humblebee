from datetime import datetime
from geopy.distance import distance
import pandas as pd

def convert_to_date_time(date_str: str) -> datetime:
    """
    Convert a date string to a datetime object.
    Args:
        date_str (str): Date string in 'YYYY-MM-DD' format.
    Returns:
        datetime: Corresponding datetime object in 'YYYY-MM-DD' format.
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def filter_hives_by_date_range(items: list, start_date_str: str = None, end_date_str: str = None) -> list:
    """
    Filter items by a date range.
    Args:
        items (list): List of items with 'datePlaced' field.
        start_date_str (str): Start date in 'YYYY-MM-DD' format.
        end_date_str (str): End date in 'YYYY-MM-DD' format.
    Returns:
        list: Filtered list of items within the specified date range.
    """
    start_date = convert_to_date_time(start_date_str) if start_date_str else None
    end_date = convert_to_date_time(end_date_str) if end_date_str else None

    filtered_items = []
    for item in items:
        placed_date = convert_to_date_time(item["datePlaced"])
        if (not start_date or placed_date >= start_date) and (not end_date or placed_date <= end_date):
            filtered_items.append(item)

    return filtered_items

def filter_crops_by_date_range(items: list, date_str: str) -> list:
    """
    Filter crops by a specific date.
    Args:
        items (list): List of crops with 'floweringStart' and 'floweringEnd' fields.
        date_str (str): Date in 'YYYY-MM-DD' format.
    Returns:
        list: Filtered list of crops that are flowering on the specified date.
    """
    date = convert_to_date_time(date_str)
    filtered_items = []
    
    for item in items:
        flowering_start = convert_to_date_time(item["floweringStart"])
        flowering_end = convert_to_date_time(item["floweringEnd"])
        if flowering_start <= date <= flowering_end:
            filtered_items.append(item)

    return filtered_items

def calculate_distance(cords1: tuple, cords2: tuple) -> float:
    """
    Calculate the distance between two geographical coordinates.
    Args:
        cords1 (tuple): First coordinate as (latitude, longitude).
        cords2 (tuple): Second coordinate as (latitude, longitude).
    Returns:
        float: Distance in meters between the two coordinates.
    """
    return distance(cords1, cords2).km

def is_valid_lat_long(latitude: float, longitude: float) -> bool:
    """
    Check if the latitude and longitude values are valid.
    Args:
        latitude (float): Latitude value.
        longitude (float): Longitude value.
    Returns:
        bool: True if valid, False otherwise.
    """
    return -90 < latitude <= 90 and -180 < longitude <= 180

def is_crop_period_invalid(flowering_start: str, flowering_end: str) -> bool:
    """
    Check if the crop flowering period is valid.
    Args:
        flowering_start (str): Flowering start date in 'YYYY-MM-DD' format.
        flowering_end (str): Flowering end date in 'YYYY-MM-DD' format.
    Returns:
        bool: True if the period is invalid, False otherwise.
    """
    start_date = convert_to_date_time(flowering_start)
    end_date = convert_to_date_time(flowering_end)
    return start_date >= end_date

def export_crops_to_csv(crops: list) -> None:
    """
    Export crops to a CSV file.
    Args:
        crops (list): List of crops to export.
        filename (str): Name of the output CSV file.
    """
    df = pd.DataFrame(crops)
    df.drop(columns=["_id"], inplace=True, errors='ignore')
    df.to_csv("crops.csv", index=False)