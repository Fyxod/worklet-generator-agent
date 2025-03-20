from pathlib import Path
from kreuzberg import extract_file
from kreuzberg import ExtractionResult
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "../worklets")
async def extract_document(name):
    pdf_path = os.path.join(PROJECT_ROOT, "../worklets", name)
    pdf_result: ExtractionResult = await extract_file(pdf_path)
    return pdf_result.content
