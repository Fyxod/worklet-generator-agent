from fastapi import FastAPI
from app.routers import root
import subprocess

app = FastAPI()

import sys
import os

streamlit_path = os.path.join(os.path.dirname(sys.executable), "streamlit")

subprocess.Popen([
    streamlit_path, "run", "streamlit_app/pdf_uploader.py",
    "--server.port", "8501",
    "--server.headless", "true",
    "--server.address", "0.0.0.0"
])

app.include_router(root.router)
