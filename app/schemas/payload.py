from pydantic import BaseModel, Field, validator
from typing import List

class TrafficFeatures(BaseModel):
    features: List[float] = Field(
        ..., 
        description="Raw list of numeric network features (excluding Timestamp, IPs, Flow ID)",
        min_items=1
    )

class PredictionResponse(BaseModel):
    threat_detected: bool
    confidence: float
    label: str
    processing_time_ms: float