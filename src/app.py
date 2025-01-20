from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import joblib
from src.preprocess_data import preprocess_input_data
from src.config import APP_NAME, VERSION, DESCRIPTION
from typing import Annotated
from sklearn.base import BaseEstimator
import pandas as pd


app = FastAPI(title=APP_NAME, version=VERSION, description=DESCRIPTION)

class CustomerData(BaseModel):
    quantity: float
    unit_price: float
    country: str


def load_model() -> tuple[BaseEstimator, BaseEstimator]:
    try:
        kmeans_model = joblib.load("models/kmeans_model.joblib")
        try:
          label_encoder = joblib.load("models/label_encoder.joblib")
        except Exception as e:
          label_encoder = None
        return kmeans_model, label_encoder

    except Exception as e:
        raise Exception(f"Error loading models: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Customer Segmentation API"}


@app.post("/predict")
def predict_cluster(data: CustomerData, model: Annotated[tuple[BaseEstimator, BaseEstimator], Depends(load_model)]):
    kmeans_model, label_encoder = model
    try:
        total_price = data.quantity * data.unit_price

        input_df = pd.DataFrame([
            {'Quantity': data.quantity,
             'UnitPrice': data.unit_price,
             'Country': data.country,
             'TotalPrice': total_price}
        ])


        processed_data = preprocess_input_data(input_df)
        cluster = kmeans_model.predict(processed_data)[0]


        # if label_encoder:
        #     cluster = label_encoder.inverse_transform([cluster])[0]

        return {"predicted_cluster": int(cluster)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))