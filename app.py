import pandas as pd
from fastapi import FastAPI, Response
from joblib import load
from sklearn.pipeline import Pipeline
from starlette import status

from constants import ARTIFACT_PATH
from utils import format_dataframe
from healthcheck import healthcheck, HealthCheckResponse
from domain import MonthData, PredictResponse

pipeline = load(ARTIFACT_PATH)
app = FastAPI()


@app.post("/predict", response_model=PredictResponse)
async def predict(month_data: MonthData):
    df = format_dataframe(month_data)
    predicted_milk_price = model.predict(df)
    return {"precio": predicted_milk_price}


@app.get("/health", status_code=200, response_model=HealthCheckResponse)
async def health(response: Response):
    health_check_response = health_check()
    if health_check_response.get("status") == "FAILURE":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return health_check_response