import joblib
import os
import time
import numpy as np
from app.core.config import settings

class IDSPipeline:
    def __init__(self):
        self.scaler = None
        self.pca = None
        self.svm = None
        self._load_models()

    def _load_models(self):
        print(f"[*] Loading artifacts from {settings.MODEL_DIR}...")
        try:
            
            self.scaler = joblib.load(os.path.join(settings.MODEL_DIR, settings.SCALER_FILENAME))
            self.pca = joblib.load(os.path.join(settings.MODEL_DIR, settings.PCA_FILENAME))
            self.svm = joblib.load(os.path.join(settings.MODEL_DIR, settings.SVM_FILENAME))
            
            print(f"   -> Scaler expects {self.scaler.n_features_in_} features")
            print(f"   -> PCA expects {self.pca.n_features_in_} features")
            print("[SUCCESS] Pipeline loaded.")
        except FileNotFoundError as e:
            raise RuntimeError(f"CRITICAL: Artifact missing. {e}")

    def predict(self, features: list[float]) -> dict:
        start_time = time.perf_counter()

        # 1. Validation: Check input length 
        if len(features) != self.scaler.n_features_in_:
            raise ValueError(
                f"Feature mismatch! Model expects {self.scaler.n_features_in_}, "
                f"but received {len(features)}."
            )

        # 2. Preprocessing Pipeline
        # Reshape to 2D array: [78 features] -> [[78 features]]
        input_vector = np.array(features).reshape(1, -1)

        # Step A: Scaling 
        scaled_data = self.scaler.transform(input_vector)

        # Step B: PCA 
        pca_data = self.pca.transform(scaled_data)

        # Step C: SVM Inference
        prediction = self.svm.predict(pca_data)[0] 
        
        try:
            probs = self.svm.predict_proba(pca_data)[0]
            confidence = float(np.max(probs))
        except AttributeError:
            # Fallback for standard SVM
            confidence = 1.0 

        processing_time = (time.perf_counter() - start_time) * 1000
        
        is_threat = bool(prediction == 1)

        return {
            "threat_detected": is_threat,
            "label": "ATTACK" if is_threat else "BENIGN",
            "confidence": confidence,
            "processing_time_ms": round(processing_time, 4)
        }

model_service = IDSPipeline()