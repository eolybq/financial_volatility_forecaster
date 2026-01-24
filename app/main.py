from config import setup_logging
setup_logging()


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class PredictionResponse(BaseModel):
    ticker: str
    predicted_volatility: float



@app.get("/predict/{ticker}")
def predict_volatility(ticker: str):
