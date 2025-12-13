import os

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from predictor import Predictor

CUSTOM_URL = os.getenv("CUSTOM_PREDICTION_URL")
FINE_TUNE_URL = os.getenv("FINE_TUNE_PREDICTION_URL")

app = FastAPI(title="Age & Gender Predictor")

# TODO: Remove dev-only settings for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ dev-only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

customPredictor = Predictor(CUSTOM_URL)
fineTunedPredictor = Predictor(FINE_TUNE_URL)


@app.post("/predict/custom")
async def predictUsingCustomModel(image: UploadFile = File(...)):
    return await customPredictor.predict(image)


@app.post("/predict/fine-tuned")
async def predictUsingFineTunedModel(image: UploadFile = File(...)):
    return await fineTunedPredictor.predict(image)
