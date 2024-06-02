# For running the FastAPI server
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
import uvicorn 
import requests

from firebase_helper import *
from misc_helper import *

app = FastAPI() 

# TODO: Only add the whitelisted origins (frontend URL) here later
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

firebase_app = init_firebase_app('.env')
db = init_firestore(env_file='.env', app=firebase_app)
storage = init_storage(env_file='.env', app=firebase_app)

@app.get("/")
async def root():
    return {"message": "Hello from Fastapi"} 

@app.get("/send/test-send-activity")
async def add_test_data_to_firestore():
    data = {
        "device-id": 1,
        "is-active": False,
        "message": "this is a test message sent from the FastAPI server",
        "timestamp": "2021-09-01T12:00:00"
    }
    add_test_data('device-activity', data, db=db)
    return {"message": "Data added successfully"}

@app.post("/send/send-data")
async def send_data(frame: UploadFile = File(...)):
    try:
        frame_bytes = await frame.read()
        driver_id = "driver1" #TODO: Change hardcode to actual implementation later on
        timestamp_url = "http://worldtimeapi.org/api/timezone/Asia/Jakarta"
        response = requests.get(timestamp_url).json()
        timestamp = str(parse_datetime(response['datetime']))
        add_driver_frame(frame_bytes, driver_id, timestamp, storage=storage)
        return {"message": "Data added successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)