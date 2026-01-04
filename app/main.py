from fastapi import FastAPI, HTTPException
from app.schemas.payload import TrafficFeatures, PredictionResponse
from app.services.model_service import model_service
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

@app.get("/health")
def health_check():
    return {"status": "active", "model_version": settings.VERSION}

@app.post("/predict", response_model=PredictionResponse)
def predict(payload: TrafficFeatures):
    try:
        result = model_service.predict(payload.features)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Inference Error")