from src.database import db
from src.const import DATABASE
from src.error import IS_ERROR

from pydantic import BaseModel
from datetime import datetime

class HiveModel(BaseModel):
    hiveId: str
    datePlaced: str
    latitude: float
    longitude: float
    numColonies: int

class Hive:
    """
    Represents a beehive with its details.
    Attributes:
        hiveId (str): Unique identifier for the hive.
        datePlaced (str): Date when the hive was placed.
        latitude (float): Latitude coordinate of the hive's location.
        longitude (float): Longitude coordinate of the hive's location.
        numColonies (int): Number of bee colonies in the hive.
    """
    def __init__(self, hive_model: HiveModel) -> None:
        self.hiveId = hive_model.hiveId
        self.datePlaced = hive_model.datePlaced
        self.latitude = hive_model.latitude
        self.longitude = hive_model.longitude
        self.numColonies = hive_model.numColonies
        self.timestamp = datetime.now().isoformat()

    def registerHive(self) -> dict:
        try:
            if not(-90 < self.latitude <=90) or not(-180 < self.longitude <= 180):
                raise ValueError(IS_ERROR["INVALID_LAT_LONG"]["message"])
            hive_data = {
                "hiveId": self.hiveId,
                "datePlaced": self.datePlaced,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "numColonies": self.numColonies,
                "timestamp": self.timestamp
            }
            register_id = db.register(DATABASE["HIVECOLLECTION"], hive_data)
            return register_id
        except Exception as e:
            raise e
    