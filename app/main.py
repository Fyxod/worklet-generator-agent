from fastapi import FastAPI
from app.routers import root
import subprocess
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

streamlit_path = os.path.join(os.path.dirname(sys.executable), "streamlit")

subprocess.Popen([
    streamlit_path, "run", "streamlit_app/pdf_uploader.py",
    "--server.port", "8501",
    "--server.headless", "true",
    "--server.address", "127.0.0.1"
])

app.include_router(root.router)
