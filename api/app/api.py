from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import tempfile
import os
from app.utils import load_and_preprocess_image, model, classes
import torch

router = APIRouter()

# Endpoint do przesyłania jednego zdjęcia
@router.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        preprocessed_image = load_and_preprocess_image(temp_path)
        with torch.no_grad():
            prediction = model(preprocessed_image)

        prediction_scores = prediction.squeeze().tolist()
        prediction_dict = {class_name: score for class_name, score in zip(classes, prediction_scores)}

        return JSONResponse(content=prediction_dict)
    finally:
        os.remove(temp_path)


# Endpoint do przesyłania wielu zdjęć
@router.post("/process-images/")
async def process_images(files: list[UploadFile] = File(...)):
    predictions = []

    for file in files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        try:
            preprocessed_image = load_and_preprocess_image(temp_path)
            with torch.no_grad():
                prediction = model(preprocessed_image)

    
            prediction_scores = prediction.squeeze().tolist()
            prediction_dict = {class_name: score for class_name, score in zip(classes, prediction_scores)}
            predictions.append(prediction_dict)

        finally:
            os.remove(temp_path)

    return JSONResponse(content={"predictions": predictions})
