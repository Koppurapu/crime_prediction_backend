from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- Imported CORS
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import pickle
import pandas as pd
from datetime import datetime
import os  # <-- Add this at the top of your file

# ... (other code) ...

# 2. DATABASE CONNECTION FUNCTION
def get_db_connection():
    # Grabs the secret URL from Render (or your local .env file)
    neon_connection_string = os.getenv("DATABASE_URL")
    
    if not neon_connection_string:
        raise Exception("CRITICAL: DATABASE_URL environment variable is missing!")
        
    return psycopg2.connect(neon_connection_string)

app = FastAPI(title="Crime Prediction API")

# --- THE CORS FIX ---
# This allows your React dashboard to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. LOAD THE AI MODEL (Bulletproofed)
model = None  # Define empty variable first to prevent crash
try:
    with open('xgboost_crime_model.pkl', 'rb') as file:
        model = pickle.load(file)
    print("✅ AI Model Loaded Successfully!")
except Exception as e:
    print(f"❌ CRITICAL ERROR: Could not find 'xgboost_crime_model.pkl'.")
    print(f"Details: {e}")
    print("Make sure your terminal is inside the TEKPROJECT folder before running uvicorn!")


# 3. DEFINE THE DATA STRUCTURE
class Incident(BaseModel):
    latitude: float
    longitude: float
    hour_of_day: int
    month_of_year: int
    is_weekend: int
    is_payday: int
    season: int
    area_type_encoded: int
    district_encoded: int

# 4. ENDPOINT: PREDICT CRIME RISK
@app.post("/api/predict")
async def predict_risk(incident: Incident):
    # Safeguard: Prevent crash if model failed to load
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Service Unavailable: The AI Model file is missing from the server directory."
        )

    try:
        # Convert incoming JSON from React into a Pandas DataFrame
        input_data = pd.DataFrame([incident.dict()])
        
        # --- THE CAPITALIZATION FIX ---
        # The AI expects 'Latitude' and 'Longitude' with capital L's
        input_data = input_data.rename(columns={
            "latitude": "Latitude", 
            "longitude": "Longitude"
        })
        
        # Ask the AI to predict the probability
        probabilities = model.predict_proba(input_data)[0]
        high_risk_prob = float(probabilities[1])
        
        # Determine if it triggers the alert (Using a strict 70% threshold)
        is_high_risk = bool(high_risk_prob >= 0.70)

        # Connect to DB and save the prediction
        db = get_db_connection()
        cursor = db.cursor()
        sql = """INSERT INTO risk_predictions 
                 (target_date, district_encoded, area_type_encoded, risk_probability, is_high_risk) 
                 VALUES (%s, %s, %s, %s, %s)"""
        val = (datetime.now().date(), incident.district_encoded, incident.area_type_encoded, high_risk_prob, is_high_risk)
        cursor.execute(sql, val)
        db.commit()
        db.close()

        return {
            "status": "success",
            "risk_probability": round(high_risk_prob * 100, 2),
            "is_high_risk_alert": is_high_risk,
            "message": "Prediction saved to database."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. ENDPOINT: FETCH PREDICTIONS FOR REACT DASHBOARD
@app.get("/api/dashboard/alerts")
async def get_alerts():
    try:
        db = get_db_connection()
        cursor = db.cursor(cursor_factory=RealDictCursor) # Returns rows as dictionaries (JSON serializable)
        # Fetch only today's high-risk alerts for the map
        cursor.execute("SELECT * FROM risk_predictions WHERE is_high_risk = true ORDER BY predicted_at DESC LIMIT 50")
        alerts = cursor.fetchall()
        db.close()
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
