from src.database import db
from src.const import DATABASE
from src.error import IS_ERROR
import src.utils as utils

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

    def registerHive(self) -> str:
        try:
            if utils.is_valid_lat_long(self.latitude, self.longitude) is False:
                raise ValueError(IS_ERROR["INVALID_LAT_LONG"]["message"])
            hive_data = {
                "hiveId": self.hiveId,
                "datePlaced": self.datePlaced,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "numColonies": self.numColonies,
                "timestamp": self.timestamp
            }
            register_id = db.register(DATABASE["HIVECOLLECTION"], hive_data, is_hive=True)
            return str(register_id)
        except Exception as e:
            raise e
    


def getHives(startDate:str = None, endDate:str = None) -> list:
    """
    Retrieve all registered hives from the database.
    Returns:
        list: A list of dictionaries containing hive details.
    """
    try:
        if startDate or endDate:
            hives = db.get_all(DATABASE["HIVECOLLECTION"])
            hives = utils.filter_hives_by_date_range(hives, start_date_str=startDate, end_date_str=endDate)
        else:
            hives = db.get_all(DATABASE["HIVECOLLECTION"])
        return hives
    except Exception as e:
        raise e