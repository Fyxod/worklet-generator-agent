from pathlib import Path
from kreuzberg import extract_file
from kreuzberg import ExtractionResult
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "../worklets")

SUPPORTED_EXTENSIONS = {
    # Documents
    '.pdf', '.docx', '.rtf', '.txt', '.epub', '.odt',
    # Presentations
    '.ppt', '.pptx',
    # Spreadsheets
    '.xls', '.xlsx', '.csv',
    # Images (OCR)
    '.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif',
    # Web content
    '.html', '.xml',
}

async def extract_document(name):
    file_path = os.path.join(UPLOAD_DIR, name)
    ext = Path(name).suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")
    
    result: ExtractionResult = await extract_file(file_path)
    return result.content
