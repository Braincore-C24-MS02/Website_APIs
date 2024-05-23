# For running the FastAPI server
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
import uvicorn 

from firebase_helper import init_firestore, add_data

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

@app.get("/")
async def root():
    return {"message": "Hello from Fastapi"} 

@app.get("/add_data")
async def add_data_to_firestore():
    data = {
        "device-id": 1,
        "is-active": False,
        "message": "this is a test message sent from the FastAPI server",
        "timestamp": "2021-09-01T12:00:00"
    }
    add_data('device-activity', data)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)