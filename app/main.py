from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import root
import subprocess
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import socketio
from app.socket import sio

# Create the FastAPI app
fastapi_app = FastAPI()

# Add CORS middleware
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Mount static files (serve 'app/public' at '/static')
fastapi_app.mount("/static", StaticFiles(directory="app/public"), name="static")

# Include your router
fastapi_app.include_router(root.router)

# Wrap the FastAPI app with the Socket.IO server
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
