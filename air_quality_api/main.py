from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import Optional

app = FastAPI()

df = pd.read_csv("PM25_dataset.csv")
print(df.head())

if df.isnull().values.any():
    print("Warning: Data contains missing values.")
    df.fillna(0, inplace=True)  

class AirQualityEntry(BaseModel):
    Year: int
    Latitude: float
    Longitude: float
    PM25: float

@app.get("/data")
def get_all_data():
    return df.to_dict(orient="records")

@app.get("/data/{id}")
def get_data_by_id(id: int):
    if id < 0 or id >= len(df):
        raise HTTPException(status_code=404, detail="Data entry not found")
    
    entry = df.iloc[id]
    return entry.to_dict() 

@app.post("/data")
def add_data(entry: AirQualityEntry):
    new_data = pd.DataFrame([entry.dict()]) 
    global df 
    df = pd.concat([df, new_data], ignore_index=True)  
    return {"message": "Data added successfully"}  

@app.put("/data/{id}")
def update_data(id: int, entry: AirQualityEntry):
    if id < 0 or id >= len(df):
        raise HTTPException(status_code=404, detail="Data entry not found")
    
    df.loc[id] = entry.dict() 
    return {"message": "Data updated successfully"} 

@app.delete("/data/{id}")
def delete_data(id: int):
    if id < 0 or id >= len(df):
        raise HTTPException(status_code=404, detail="Data entry not found")
    
    df.drop(index=id, inplace=True)  
    df.reset_index(drop=True, inplace=True)  
    return {"message": "Data deleted successfully"}  

@app.get("/data/filter")
def filter_data(
    year: Optional[int] = None, 
    lat: Optional[float] = None, 
    long: Optional[float] = None
):
    """Filter data based on specified criteria."""
    filtered_df = df.copy()  
    
    if year is not None:
        filtered_df = filtered_df[filtered_df["Year"] == year]
    if lat is not None:
        filtered_df = filtered_df[filtered_df["Latitude"] == lat]
    if long is not None:
        filtered_df = filtered_df[filtered_df["Longitude"] == long]

    if filtered_df.empty:
        raise HTTPException(status_code=404, detail="No matching data found")

    return filtered_df.to_dict(orient="records")  

@app.get("/data/stats")
def get_stats():
    """Provide basic statistics about the air quality data."""
    stats = {
        "count": len(df),  
        "average_pm25": df["PM2.5"].mean(), 
        "min_pm25": df["PM2.5"].min(),  
        "max_pm25": df["PM2.5"].max(), 
    }
    return stats 
