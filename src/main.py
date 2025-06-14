from fastapi import FastAPI
from fastapi.responses import JSONResponse
import starlette.status as status
from datetime import datetime

from src.log import logger
from src.hive import HiveModel, Hive, get_filtered_hives
from src.error import IS_ERROR, IS_SUCCESS
from src.crop import CropModel, Crop, get_nearby_crop, get_all_crops
import src.utils as utils

app = FastAPI()

@app.post("/api/hives")
def register_hive(hive_model:HiveModel):
    """
    Register a new hive with the provided details.
    """
    try:
        hive_obj = Hive(hive_model=hive_model)
        register_id = hive_obj.registerHive()
        result = IS_SUCCESS["HIVE_REG_SUCCESS"]
        result["hiveId"] = register_id
        status_code = status.HTTP_200_OK

    except ValueError as ve:
        if IS_ERROR["INVALID_LAT_LONG"]["message"] in str(ve):
            logger.error(f"Invalid latitude or longitude for hive {hive_model.hiveId}: {str(ve)}")
            result = IS_ERROR["INVALID_LAT_LONG"]
            status_code = status.HTTP_400_BAD_REQUEST
        elif IS_ERROR["HIVE_ALREADY_EXISTS"]["message"] in str(ve):
            logger.error(f"Hive ID already exists {hive_model.hiveId}: {str(ve)}")
            result = IS_ERROR["HIVE_ALREADY_EXISTS"]
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            raise ve
    except Exception as e:
        logger.exception(f"Failed to register hive {hive_model.hiveId}: {str(e)}")
        result = IS_ERROR["HIVE_REG_FAILED"]
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
    return JSONResponse(status_code=status_code, content=result)

@app.get("/api/hives")
def get_hives(startDate: str = None, endDate: str = None):
    """
    Retrieve all registered hives, optionally filtered by startDate and endDate.
    """
    try:
        hives = get_filtered_hives(startDate=startDate, endDate=endDate)
        result = IS_SUCCESS["HIVES_RETRIEVED"]
        result["hives"] = hives
        status_code = status.HTTP_200_OK

    except Exception as e:
        logger.exception(f"Failed to retrieve hives: {str(e)}")
        result = IS_ERROR["HIVE_REG_FAILED"]
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
    return JSONResponse(status_code=status_code, content=result)

@app.post("/api/crops")
def register_crop(crop_model: CropModel):
    """
    Register a new crop with the provided details.
    """
    try:
        crop = Crop(crop_model=crop_model)
        register_id = crop.register_crop()
        result = IS_SUCCESS["CROP_REG_SUCCESS"]
        result["cropId"] = register_id
        status_code = status.HTTP_200_OK
    except ValueError as ve:
        logger.error(f"Invalid latitude or longitude for crop {crop_model.name}: {str(ve)}")
        result = IS_ERROR["CROP_REG_FAILED"]
        status_code = status.HTTP_400_BAD_REQUEST
    return JSONResponse(status_code=status_code, content=result)

@app.get("/api/crops/nearby")
def get_crops(latitude: float, longitude: float, radius: float = 100, date: str = datetime.now().date().isoformat()):
    """
    Retrieve crops within a specified radius from the given latitude and longitude.
    """
    try:
        crops = get_nearby_crop(latitude=latitude, longitude=longitude, radius=radius, date=date)
        result = IS_SUCCESS["CROPS_RETRIEVED"]
        result["crops"] = crops
        status_code = status.HTTP_200_OK
    except Exception as e:
        logger.exception(f"Failed to retrieve nearby crops: {str(e)}")
        result = IS_ERROR["CROP_RETRIEVE_FAILED"]
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
    return JSONResponse(status_code=status_code, content=result)

@app.get("/api/crops/export")
def export_crops():
    """
    Export all crops in a CSV format.
    """
    try:
        crops = get_all_crops()
        utils.export_crops_to_csv(crops)
        result = IS_SUCCESS["CROPS_EXPORTED"]
        status_code = status.HTTP_200_OK
    except Exception as e:
        logger.exception(f"Failed to export crops: {str(e)}")
        result = IS_ERROR["CROP_EXPORT_FAILED"]
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(status_code=status_code, content=result)