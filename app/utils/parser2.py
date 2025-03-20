from pathlib import Path
from kreuzberg import extract_file
from kreuzberg import ExtractionResult
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "../worklets")

async def extract_document(name):
    pdf_path = os.path.join(PROJECT_ROOT, "../worklets", name)
    # Extract from a PDF file with default settings
    pdf_result: ExtractionResult = await extract_file(pdf_path)
    print(f"Content: {pdf_result.content}")
    return pdf_result.content

    # use this library to run it asyncrousnly
# import asyncio
# name="d.pdf"
# asyncio.run(extract_document(name))


#before using it runcmd as admin and run      choco install -y tesseract pandoc
#  then install pip install kreuzberg