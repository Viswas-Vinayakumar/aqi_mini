# app/main.py
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from sqlalchemy import text
from fastapi import Body
from datetime import date



Base.metadata.create_all(bind=engine)

app = FastAPI(title="AQI Mini")

@app.get("/")
def health():
    return {"status": "ok"}

#get all data using the get command

@app.get("/aqi/raw")
def get_raw_aqi():
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT date, aqi FROM air_quality_raw_mini ORDER BY date"
            )
        )
        rows = result.fetchall()

    return [
        {"date": row.date.isoformat(), "aqi": row.aqi}
        for row in rows
    ]

# Post predicted values using the post command

@app.post("/aqi/predictions")
def add_predictions(payload: dict = Body(...)):
    model_version = payload["model_version"]
    predictions = payload["predictions"]

    with engine.connect() as conn:
        for p in predictions:
            conn.execute(
                text(
                    """
                    INSERT INTO aqi_predictions_mini
                    (prediction_date, target_date, predicted_aqi, model_version)
                    VALUES (:prediction_date, :target_date, :predicted_aqi, :model_version)
                    """
                ),
                {
                    "prediction_date": date.today(),
                    "target_date": p["target_date"],
                    "predicted_aqi": p["predicted_aqi"],
                    "model_version": model_version,
                },
            )
        conn.commit()

    return {"status": "predictions stored"}

# Get predictions using the get command

@app.get("/aqi/predictions")
def get_predictions():
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT
                    prediction_date,
                    target_date,
                    predicted_aqi,
                    model_version
                FROM aqi_predictions_mini
                ORDER BY target_date
                """
            )
        )
        rows = result.fetchall()

    return [
        {
            "prediction_date": row.prediction_date.isoformat(),
            "target_date": row.target_date.isoformat(),
            "predicted_aqi": row.predicted_aqi,
            "model_version": row.model_version,
        }
        for row in rows
    ]

