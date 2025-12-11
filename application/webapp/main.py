import os

from fastapi import FastAPI, File, UploadFile
from predictor import Predictor

app = FastAPI(title="Age & Gender Predictor")
CUSTOM_URL = os.getenv("CUSTOM_PREDICTION_URL")
FINE_TUNE_URL = os.getenv("FINE_TUNE_PREDICTION_URL")


customPredictor = Predictor(CUSTOM_URL)


@app.post("/predict/custom")
async def predictUsingCustomModel(file: UploadFile = File(...)):
    return await customPredictor.predict(file)


fineTunedPredictor = Predictor(FINE_TUNE_URL)


@app.post("/predict/fine-tuned")
async def predictUsingFineTunedModel(file: UploadFile = File(...)):
    return await fineTunedPredictor.predict(file)
