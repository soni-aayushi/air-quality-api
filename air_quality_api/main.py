from fastapi import FastAPI, HTTPException
import pandas as pd
from typing import Optional
from models.air_quality_model import AirQualityEntry  

app = FastAPI()

df = pd.read_csv("database/PM25_dataset.csv")
print(df.head())

if df.isnull().values.any():
    print("Warning: Data contains missing values.")
    df.fillna(0, inplace=True)

@app.get("/data")
def get_all_data():
    try:
        if df.empty:
            raise HTTPException(status_code=500, detail="DataFrame is empty or not loaded")
        
        data = df.to_dict(orient="records")
        print(data)  
        return data
    except Exception as e:
        print("Error while getting all data:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/data/{id}")
def get_data_by_id(id: int):
    try:
        if id < 0 or id >= len(df):
            raise HTTPException(status_code=404, detail="Data entry not found")
        
        entry = df.iloc[id]
        print(f"Fetching entry at index {id}: {entry}")
        return entry.to_dict()
    except Exception as e:
        print(f"Error occurred while fetching data by id: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
 

@app.post("/data")
def add_data(entry: AirQualityEntry):
    new_data = pd.DataFrame([entry.dict()]) 
    global df 
    df = pd.concat([df, new_data], ignore_index=True)  
    
    df.to_csv("database/PM25_dataset.csv", index=False)  
    
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
    stats = {
        "count": len(df),  
        "average_pm25": df["PM25"].mean(),
        "min_pm25": df["PM25"].min(),  
        "max_pm25": df["PM25"].max(), 
    }
    return stats 
