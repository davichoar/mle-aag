import os
from typing import List

import pandas as pd
from joblib import load
from sklearn.pipeline import Pipeline
from pydantic import BaseModel

from constants import ARTIFACT_PATH, TEST_FEATURES, FINAL_COLS
import logging
logger = logging.getLogger('healthcheck')
logging.basicConfig(level=logging.INFO)


class HealthCheckResponse(BaseModel):
    status: str
    message: List[str]

def healthcheck():
    # Initialize with good status
    status = "PASS"
    message = []
    model_exists = os.path.exists(ARTIFACT_PATH)
    if not model_exists:
        status = "FAILURE"
        message.append(f"model artifacts not placed in {model_path}")
    test_df = pd.DataFrame([TEST_FEATURES])
    try:
        pipeline = load(ARTIFACT_PATH)
        prediction = pipeline.predict(test_df[FINAL_COLS])
        logger.info(f'Prediction for healthcheck: {prediction[0]}')
    except Exception as e:
        status = "FAILURE"
        # Catch error messages of features/model errors
        message.append(str(e))
    return {"status": status, "message": message}