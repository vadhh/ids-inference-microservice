# Network Intrusion Detection (IDS) Microservice

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-green?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=flat-square)
![ML](https://img.shields.io/badge/Sklearn-SVM%20%2B%20PCA-orange?style=flat-square)

A production-grade Machine Learning microservice for real-time Network Intrusion Detection. This project refactors an academic thesis ("Optimization of SVM utilizing PCA") into a scalable, containerized REST API.

It utilizes **Principal Component Analysis (PCA)** to reduce network traffic feature space by **70% (78 $\to$ 23 features)** while maintaining **95% variance**, resulting in significantly faster inference times for real-time deployment.

## 🏗 Architecture

The system transforms raw network traffic vectors into threat predictions using a strict scikit-learn pipeline.

```mermaid
graph LR
    A[Client Request] -->|JSON (78 Features)| B(FastAPI Endpoint)
    B --> C{Input Validation}
    C -->|Valid| D[Standard Scaler]
    D -->|Normalized| E[PCA Transform]
    E -->|Reduced (23 Features)| F[SVM Classifier]
    F -->|Prediction| G[Response]
    C -->|Invalid| H[400 Error]
```

## 🚀 Key Features
- Dimensionality Reduction: Compresses 78 CIC-IDS-2017 features into 23 principal components using PCA.
- Production API: Exposes the model via FastAPI with strict Pydantic schema validation.
- Containerized: Fully dockerized environment using python:3.10-slim for consistent deployment.
- Performance:Accuracy: ~86-88% (Benchmark against CIC-IDS-2017 dataset).
- Latency: Sub-millisecond internal inference time.📂 

## Project Structure
```Plaintext.
├── app/
│   ├── core/           # Config & Settings
│   ├── schemas/        # Pydantic Models (Input/Output Contracts)
│   ├── services/       # Inference Engine (Singleton Pattern)
│   └── main.py         # API Entrypoint
├── models/             # Serialized Artifacts (Scaler, PCA, SVM)
├── Dockerfile          # Multi-stage build instructions
└── requirements.prod.txt
```
## 🛠 Installation & Usage
1. Run with Docker (Recommended)
```Bash
# Build the image
docker build -t ids-api:v1 .

# Run container (Exposed on port 8000)
docker run -d -p 8000:8000 --name ids-service ids-api:v1
```
2. API Endpoints
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /health | Health check and model status |
| POST | /predict | Main inference endpoint |

3. Example Request
Input: Raw feature vector (78 floats) representing network flow statistics.
```Bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"features": [80, 10452, 0, ... (78 features) ...]}'
```
Output:
```JSON
{
  "threat_detected": true,
  "confidence": 0.985,
  "label": "ATTACK",
  "processing_time_ms": 0.42
}
```

## 📊 Performance Metrics (Thesis Results)
The transition from raw features to PCA features demonstrated a massive reduction in complexity with minimal loss in detection capability.
| Metric | Original (78 Features) | PCA (23 Features) | Impact |
| --- | --- | --- | --- |
| Information Retained | 100% | 95% | 5% Loss | 
| Training Time | High | Low | Speedup | 
| Accuracy (Weighted) | 0.88 | 0.86 | ~2% Drop | 

Note: The slight drop in accuracy is a strategic trade-off for the massive gain in throughput required for real-time network monitoring.