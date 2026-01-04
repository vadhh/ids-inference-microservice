import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "IDS-Thesis-Microservice"
    VERSION: str = "1.0.0"
    
    MODEL_DIR: str = "models"
    
    SCALER_FILENAME: str = "sprint6_scaler.pkl"
    PCA_FILENAME: str = "sprint6_pca_model.pkl"
    SVM_FILENAME: str = "sprint6_svm_model.pkl"

    class Config:
        env_file = ".env"

settings = Settings()