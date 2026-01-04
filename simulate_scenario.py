import pandas as pd
import requests
import json
import random
import time

# Configuration
PARQUET_PATH = "data/processed/clean_cicids_combined.parquet"
API_URL = "http://localhost:8000/predict"

# Metadata columns to drop (Must match sprint3_prepro.py)
DROP_COLS = ['Label', 'Timestamp', 'Flow ID', 'Source IP', 'Destination IP', 'SimillarHTTP']

def get_sample_payload(df, label_type):
    """
    Extracts a random row matching the specific label (BENIGN or Attack).
    """
    if label_type == "BENIGN":
        subset = df[df['Label'] == 'BENIGN']
    else:
        subset = df[df['Label'] != 'BENIGN']
        
    if subset.empty:
        raise ValueError(f"No data found for label type: {label_type}")

    # Pick 1 random row
    row = subset.sample(1).iloc[0]
    
    # Get the true label for verification
    true_label = row['Label']
    
    # Drop metadata 
    features_series = row.drop(labels=DROP_COLS, errors='ignore')
    
    # Convert numpy types to native Python floats
    features = features_series.values.astype(float).tolist()
    
    return features, true_label

def send_traffic(features, true_label):
    """Sends the feature vector to the API."""
    try:
        payload = {"features": features}
        
        # Timing the network request
        start = time.perf_counter()
        response = requests.post(API_URL, json=payload)
        latency = (time.perf_counter() - start) * 1000
        
        if response.status_code == 200:
            res_json = response.json()
            
            # Visual formatting
            status_color = "\033[91m" if res_json['threat_detected'] else "\033[92m" # Red if Threat, Green if Safe
            reset = "\033[0m"
            
            print(f"[*] True Label:      {true_label}")
            print(f"    API Prediction:  {status_color}{res_json['label']} (Confidence: {res_json['confidence']:.4f}){reset}")
            print(f"    Inference Time:  {res_json['processing_time_ms']:.2f}ms (Internal) + {latency:.2f}ms (Network)")
            
            # Verification logic
            if (true_label == "BENIGN" and not res_json['threat_detected']) or \
               (true_label != "BENIGN" and res_json['threat_detected']):
                print("    ✅ SUCCESS: Prediction matches reality.")
            else:
                print("    ❌ MISMATCH: Model got it wrong.")
                
        else:
            print(f"[!] Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"[!] Connection Failed: {e}")

if __name__ == "__main__":
    print(f"[*] Loading Dataset from {PARQUET_PATH}...")
    try:
        # Load only necessary columns to save RAM if file is huge
        # But for simplicity, we load all and drop later
        df = pd.read_parquet(PARQUET_PATH)
        print(f"[*] Data Loaded. Total Rows: {len(df)}")
    except Exception as e:
        print(f"[!] Critical Error loading Parquet: {e}")
        print("    Are you running this from the project root?")
        exit(1)

    print("\n--- SIMULATING NORMAL USER (BENIGN) ---")
    feat_benign, label_benign = get_sample_payload(df, "BENIGN")
    send_traffic(feat_benign, label_benign)
    
    print("\n--- SIMULATING ATTACKER (ATTACK) ---")
    feat_attack, label_attack = get_sample_payload(df, "ATTACK") # Fetches any non-benign
    send_traffic(feat_attack, label_attack)