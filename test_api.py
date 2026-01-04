import requests
import numpy as np
import json
import sys

# Configuration
API_URL = "http://localhost:8000/predict"
HEALTH_URL = "http://localhost:8000/health"

# The pipeline expects raw features (78), NOT the reduced PCA features (23).
# The Scaler is the first gatekeeper.
REQUIRED_FEATURES = 78 

def log(msg, status="INFO"):
    colors = {
        "INFO": "\033[94m",    # Blue
        "SUCCESS": "\033[92m", # Green
        "ERROR": "\033[91m",   # Red
        "RESET": "\033[0m"
    }
    print(f"{colors.get(status, '')}[{status}] {msg}{colors['RESET']}")

def check_health():
    """Verifies the container is running and models are loaded."""
    try:
        response = requests.get(HEALTH_URL)
        if response.status_code == 200:
            log("Health check passed.", "SUCCESS")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            log(f"Health check failed: {response.status_code}", "ERROR")
            return False
    except requests.exceptions.ConnectionError:
        log("Could not connect to localhost:8000. Is the Docker container running?", "ERROR")
        return False

def test_prediction(n_features, description):
    """Sends a payload with n_features to the API."""
    log(f"Testing {description} (Payload Size: {n_features})...")
    
    # Generate dummy float data (simulating normalized network traffic)
    # Using float32 range similar to scaled data
    dummy_features = list(np.random.normal(loc=0.0, scale=1.0, size=n_features))
    
    payload = {"features": dummy_features}
    
    try:
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            log(f"Success! Model accepted the input.", "SUCCESS")
            print(f"   -> Threat Detected: {data['threat_detected']}")
            print(f"   -> Confidence:      {data['confidence']:.4f}")
            print(f"   -> Label:           {data['label']}")
            print(f"   -> Processing Time: {data['processing_time_ms']:.2f}ms")
            
        elif response.status_code == 400:
            # This is expected for the 'Trap' test
            log(f"API correctly rejected the input (Status 400).", "SUCCESS")
            print(f"   -> Error Message: {response.json()['detail']}")
            
        else:
            log(f"Unexpected Error: {response.status_code}", "ERROR")
            print(response.text)
            
    except Exception as e:
        log(f"Request failed: {e}", "ERROR")

if __name__ == "__main__":
    print("-" * 50)
    print("IDS API INTEGRATION TEST")
    print("-" * 50)

    # 1. Check if Server is Up
    if not check_health():
        sys.exit(1)
    
    print("\n" + "-" * 30)
    
    # 2. Test CORRECT Input (78 Raw Features)
    # This verifies the Scaler -> PCA -> SVM pipeline
    test_prediction(REQUIRED_FEATURES, "Correct Raw Input")

    print("\n" + "-" * 30)

    # 3. Test INCORRECT Input (23 PCA Features)
    # This verifies your 'model_service.py' validation logic
    # If the user mistakenly sends already-reduced data, the API should scream.
    test_prediction(23, "Incorrect (Already Reduced) Input")
    
    print("-" * 50)