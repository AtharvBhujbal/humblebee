from src.database import db
from src.error import IS_ERROR, IS_SUCCESS
from src.const import DATABASE
from pydantic import BaseModel
import src.utils as utils

class CropModel(BaseModel):
    name: str
    floweringStart: str
    floweringEnd: str
    latitude: float
    longitude: float
    recommendedHiveDensity: int

class Crop:
    def __init__(self, crop_model: CropModel) -> None:
        self.name = crop_model.name
        self.floweringStart = crop_model.floweringStart
        self.floweringEnd = crop_model.floweringEnd
        self.latitude = crop_model.latitude
        self.longitude = crop_model.longitude
        self.recommendedHiveDensity = crop_model.recommendedHiveDensity

    def register_crop(self) -> str:
        try:
            if utils.is_valid_lat_long(self.latitude, self.longitude) is False:
                raise ValueError(IS_ERROR["INVALID_LAT_LONG"]["message"])
            if utils.is_crop_period_invalid(self.floweringStart, self.floweringEnd):
                raise ValueError("Flowering start date must be before flowering end date.")
            crop_data = {
                "name": self.name,
                "floweringStart": self.floweringStart,
                "floweringEnd": self.floweringEnd,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "recommendedHiveDensity": self.recommendedHiveDensity
            }
            register_id = db.register(DATABASE["CROPCOLLECTION"], crop_data)
            return str(register_id)
        except Exception as e:
            raise e
        
def get_nearby_crop(latitude: float, longitude: float, radius: int, date: str) -> list:
    try:
        if utils.is_valid_lat_long(latitude, longitude) is False:
            raise ValueError(IS_ERROR["INVALID_LAT_LONG"]["message"])
        
        crops = db.get_all(DATABASE["CROPCOLLECTION"])
        crops = utils.filter_crops_by_date_range(crops, date)
        nearby_crops = []
        
        for crop in crops:
            crop_coords = (crop["latitude"], crop["longitude"])
            distance_to_crop = utils.calculate_distance((latitude, longitude), crop_coords)
            if distance_to_crop <= radius:
                nearby_crops.append(crop)
        
        return nearby_crops
    except Exception as e:
        raise e