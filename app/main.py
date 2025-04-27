from fastapi import FastAPI
from app.routers import root
import subprocess
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import socketio
from app.socket import sio

fastapi_app = FastAPI()

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

fastapi_app.include_router(root.router)

app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
