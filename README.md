# Humblebee

## Implemented APIs

| **API Endpoint**      | **API Name**       | **Request Type** | **Description**                                                                 |
|-----------------------|--------------------|------------------|---------------------------------------------------------------------------------|
| `api/hives`           | **Register Hive**  | `POST`           | Allows users to register a new hive with its details. |
| `api/hives/`      | **Get Hive**       | `GET`            | Allows users to retrieves all hive or filter by dates. |
| `api/crops`           | **Register Crop**  | `POST`           | Allow users to register a new crop with its details. |
| `api/crops/nearby`    | **Get Crop**       | `GET`            | Allow users to retrieves all crops or filters them by start and end date. |
| `api/crops/export` | **Export Crops**   | `GET`            | Allows users to export all crops in CSV format. |

## Installation

1. Clone the repository:
    ```bash
    git clone git@github.com:AtharvBhujbal/humblebee.git
    ```
2. Navigate to the project directory:
    ```bash
    cd humblebee
    ```
3. Install the dependencies:
    1. Create a virtual environment:

        ```bash
        python -m venv .venv
        ```

    2. Activate the virtual environment:

        ```bash
        source .venv/bin/activate
        ```

    3. Install backend dependencies:

        ```bash
        pip install -r requirements.txt
        ``` 

    4. Verify the setup by running unit tests:

        ```bash
        pytest
        ```

       This ensures that the environment is correctly configured and all dependencies are functioning as expected.
        

4. Start the backend server:

    ```bash
    uvicorn src.main:app --reload
    ```

5. Open your browser and navigate to [`/docs`](http://localhost:8000/docs) to access the API documentation.

## Usage
I have created a Postman collection to test the API endpoints.
You can access it [here](https://atharvbhujbal.postman.co/workspace/Atharv-Bhujbal's-Workspace~349517e4-4b00-4422-8e36-9e5c17935361/request/44363547-9f98e422-a96b-41b1-ad21-8d9f0d06da3c).

## Logic
The logic for the Humblebee API is implemented in the `src` directory. The main components include:
- **`src/main.py`**: The entry point for the FastAPI application contains all the api routes.
- **`src/utils.py`**: Contains utility functions for various operations.
- **`src/const.py`**: Defines constants used throughout the application.
- **`src/error.py`**: Defines custom error response for the API.
- **`src/log.py`**: Configures logging for the application.

- **`src/database.py`**: Handles database connections and operations.
- **`src/hive.py`**: Contains the main logic for the Hive class.
    - Contains - 
        - a. HiveModel - Defines the data model for the Hive.
        - b. RegisterHive - Function to register a new Hive in Hive class.
        - c. GetHive - Function to retrieve a Hive by its ID.
- **`src/crop.py`**: Contains the main logic for the Crop class.
    - Contains -
        - a. CropModel - Defines the data model for the Crop.
        - b. RegisterCrop - Function to register a new Crop in Crop class.
        - c. GetCrop - Function to retrieve all Crops or filter by start and end date.

## Few Points to Note
1. The logic for each entity (Hive, Crop) is encapsulated in its own module for better organization and maintainability.
    - Note : Function like `get_filtered_hives` and `get_nearby_crop` are implemented in the same file as the class to keep the code organized and easy to follow. They are not present in the same class because we have to make init variables optional and we can not do that in the same class.
2. I like to keep my code clean and readable, so I have used type docstrings to make the code self-explanatory.
3. Keeping the code DRY (Don't Repeat Yourself) is important, so I have used utility functions to avoid code duplication.
4. I have used uderscore naming convetion for function naming instead of camelCase.
5. I have used `pytest` for unit testing and have written tests for all the functions in the `tests` directory.