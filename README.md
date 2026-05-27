# 🛡️ Crime Prediction API (Backend)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![XGBoost](https://img.shields.io/badge/Machine%20Learning-XGBoost-orange.svg)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791.svg)
![Render](https://img.shields.io/badge/Deployed_on-Render-black.svg)

This is the backend intelligence engine for the **Nexus Crime Prediction Platform**. It is a robust, cloud-optimized REST API built with FastAPI that serves real-time Machine Learning predictions and interfaces with a live PostgreSQL database.

## 🚀 Features

* **Real-time ML Inference:** Uses a highly-optimized XGBoost Classification model to predict the probability of high-risk criminal activity based on temporal and geographic parameters.
* **Database Integration:** Connects securely to a NeonDB PostgreSQL database to fetch and serve recent active threat alerts.
* **Cloud-Ready:** fully optimized for serverless/cloud deployment with a compressed `.pkl` model and environment variable security.
* **CORS Configured:** Securely accepts cross-origin requests from the Vercel-hosted React frontend.

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Machine Learning:** XGBoost, Scikit-learn, Pandas
* **Server:** Uvicorn
* **Database:** PostgreSQL (Hosted on NeonDB), `psycopg2-binary`
* **Deployment:** Render

## 📁 Repository Structure

\`\`\`text
crime_prediction_backend/
├── main.py                  # Core FastAPI application and routing
├── requirements.txt         # Python dependencies
├── xgboost_crime_model.pkl  # Cloud-optimized pre-trained ML model
├── .gitignore               # Security exclusions (ignores .env and heavy datasets)
└── README.md                # Documentation
\`\`\`

## 🔌 API Endpoints

### 1. Predict Threat Level
* **Endpoint:** `POST /api/predict`
* **Description:** Accepts environmental parameters and returns a calculated risk probability.
* **Payload Example:**
  \`\`\`json
  {
    "hour_of_day": 21,
    "is_weekend": 1,
    "district_encoded": 5,
    "area_type_encoded": 120
  }
  \`\`\`
* **Response Example:**
  \`\`\`json
  {
    "risk_probability": 85.4,
    "is_high_risk_alert": true,
    "message": "High Risk Alert Generated"
  }
  \`\`\`

### 2. Fetch Live Alerts
* **Endpoint:** `GET /api/dashboard/alerts`
* **Description:** Retrieves the latest high-risk incidents from the PostgreSQL database for the live feed.

## 💻 Local Development Setup

To run this API on your local machine, follow these steps:

1. **Clone the repository:**
   \`\`\`bash
   git clone https://github.com/YOUR-GITHUB-USERNAME/crime_prediction_backend.git
   cd crime_prediction_backend
   \`\`\`

2. **Create and activate a virtual environment:**
   * **Windows:**
     \`\`\`bash
     python -m venv venv
     venv\Scripts\activate
     \`\`\`
   * **Mac/Linux:**
     \`\`\`bash
     python3 -m venv venv
     source venv/bin/activate
     \`\`\`

3. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add your secure NeonDB connection string:
   \`\`\`env
   DATABASE_URL=postgresql://your_user:your_password@your_host/neondb?sslmode=require
   \`\`\`

5. **Start the Development Server:**
   \`\`\`bash
   uvicorn main:app --reload
   \`\`\`
   *The API will be live at `http://127.0.0.1:8000`*

## 🔒 Security Note
This repository strictly ignores the `.env` file and all local datasets (`*.csv`) to prevent sensitive credentials and large files (bypassing GitHub's 100MB limit) from being exposed to the public. 

