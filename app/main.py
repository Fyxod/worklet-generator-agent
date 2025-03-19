from fastapi import FastAPI
from app.routers import root
import subprocess

app = FastAPI()

subprocess.Popen(["streamlit", "run", "streamlit_app/pdf_uploader.py", "--server.port", "8501", "--server.headless", "true"])

app.include_router(root.router)
