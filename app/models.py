# app/models.py
from sqlalchemy import Column, Integer, Date
from app.database import Base

class AirQualityRawMini(Base):
    __tablename__ = "air_quality_raw_mini"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    aqi = Column(Integer, nullable=False)
