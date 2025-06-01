from fastapi import FastAPI
from fastapi.responses import JSONResponse
import starlette.status as status

from src.log import logger
from src.hive import HiveModel, Hive
from src.error import IS_ERROR, IS_SUCCESS

app = FastAPI()

@app.post("/api/hives")
async def register_hive(hive_model:HiveModel):
    """
    Register a new hive with the provided details.
    """
    try:
        hive_obj = Hive(hive_model=hive_model)
        register_id = hive_obj.registerHive()
        result = IS_SUCCESS["HIVE_REG_SUCCESS"]
        result["hiveId"] = str(register_id)
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

