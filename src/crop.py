from src.database import db
from src.error import IS_ERROR, IS_SUCCESS
from src.const import DATABASE
from pydantic import BaseModel

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

    def registerCrop(self) -> str:
        try:
            if not(-90 < self.latitude <=90) or not(-180 < self.longitude <= 180):
                raise ValueError(IS_ERROR["INVALID_LAT_LONG"]["message"])
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