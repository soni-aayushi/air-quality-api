# Air Quality API

## Overview
A RESTful API for accessing air quality data, focused on PM2.5 levels from the Global Annual PM2.5 Grids dataset.

## Used Technologies 
- FastAPI
- Python
- Docker

## Requirements
- Python 3.9+
- Docker (optional)

## Running the API Locally
1. Clone the repository:
   git clone https://github.com/YOUR_USERNAME/air-quality-api.git
   cd air-quality-api
   
## Install dependencies
pip install -r requirements.txt

## Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000

## Running the API with Docker
docker build -t air-quality-api .

## Stopping the Docker Container
docker stop air-quality-api

## Removing the Docker Container
docker rm air-quality-api

