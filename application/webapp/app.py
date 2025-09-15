import io, os, json
import numpy as np
import requests
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

TF_URL = os.getenv("TF_URL")

app = FastAPI(title="Age & Gender Demo")
templates = Jinja2Templates(directory="templates")

def preprocess(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((128, 128))
    x = (np.asarray(img, dtype=np.float32) / 255.0)[None, ...]  # (1,128,128,3)
    return x

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "Please upload an image.")
    x = preprocess(await file.read())
    try:
        r = requests.post(TF_URL, json={"instances": x.tolist()}, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(502, f"Model server error: {e}")
    return r.json()  # keep it simple: return raw TF Serving JSON
