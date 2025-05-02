from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import root
from fastapi.middleware.cors import CORSMiddleware
import socketio
from app.socket import sio

# Create the FastAPI app
fastapi_app = FastAPI()

# Add CORS middleware
fastapi_app.add_middleware( # allowed all origins for now
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (serve 'app/public' at '/static')
fastapi_app.mount("/static", StaticFiles(directory="app/public"), name="static")

fastapi_app.include_router(root.router)

# Wrap the FastAPI app with the Socket.IO server
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
