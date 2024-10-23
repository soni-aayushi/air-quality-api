from pydantic import BaseModel

class AirQualityEntry(BaseModel):
    Year: int
    Latitude: float
    Longitude: float
    PM25: float
