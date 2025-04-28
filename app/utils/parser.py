from pathlib import Path
from kreuzberg import extract_file
from kreuzberg import ExtractionResult
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import shutil
from app.socket import sio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "../worklets")

image_dir = os.path.join(PROJECT_ROOT, "./resources/extracted_images")
archive_dir = os.path.join(PROJECT_ROOT, "./resources/archived_images")

os.makedirs(image_dir, exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)

SUPPORTED_EXTENSIONS = {
    '.pdf', '.docx', '.rtf', '.txt', '.epub', '.odt','.ppt', '.pptx','.xls', '.xlsx', '.csv','.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif','.html', '.xml',
}

async def extract_document(name):
    file_path = os.path.join(UPLOAD_DIR, name)
    ext = Path(name).suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")
    
    result: ExtractionResult = await extract_file(file_path)

    if result.content is None:
        result.content = ""

    for filename in os.listdir(image_dir):
        src = os.path.join(image_dir, filename)
        dst = os.path.join(archive_dir, filename)
        if os.path.isfile(src):
            shutil.move(src, dst)

    doc = fitz.open(file_path)
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        image_list = page.get_images(full=True)

        print(f"Page {page_number + 1} has {len(image_list)} images.")

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))

            image_path = os.path.join(image_dir, f"page{page_number + 1}_img{img_index + 1}.{image_ext}")
            image.save(image_path)

            # OCR the image
            await sio.emit("progress", {"message": "Extracting data from images..."})
            text = pytesseract.image_to_string(image)
            result.content += f" {text} \n"
            
    return result.content
