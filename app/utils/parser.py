from pathlib import Path
from kreuzberg import extract_file
from kreuzberg import ExtractionResult
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "../worklets")

image_dir = os.path.join(PROJECT_ROOT, "./resources/extracted_images")
archive_dir = os.path.join(PROJECT_ROOT, "./resources/archived_images")

os.makedirs(image_dir, exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)

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
            text = pytesseract.image_to_string(image)
            result.content += f" {text} \n"
            
    return result.content
# # parser 2
# from pathlib import Path
# from kreuzberg import extract_file
# from kreuzberg import ExtractionResult
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.dirname(BASE_DIR)
# UPLOAD_DIR = os.path.join(PROJECT_ROOT, "../worklets")

# SUPPORTED_EXTENSIONS = {
#     # Documents
#     '.pdf', '.docx', '.rtf', '.txt', '.epub', '.odt',
#     # Presentations
#     '.ppt', '.pptx',
#     # Spreadsheets
#     '.xls', '.xlsx', '.csv',
#     # Images (OCR)
#     '.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif',
#     # Web content
#     '.html', '.xml',
# }

# async def extract_document(name):
#     file_path = os.path.join(UPLOAD_DIR, name)
#     ext = Path(name).suffix.lower()

#     if ext not in SUPPORTED_EXTENSIONS:
#         raise ValueError(f"Unsupported file type: {ext}")
    
#     result: ExtractionResult = await extract_file(file_path)
#     return result.content
# # parser1
# mport pandas as pd
# from tabula.io import read_pdf
# import tabula
# import json
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.dirname(BASE_DIR)

# UPLOAD_DIR = os.path.join(PROJECT_ROOT, "../worklets")

# parameters = [
#     {"page": 1, "extraction_method": "stream", "selection_id": "K1742359645874", "x1": 12, "x2": 412.8, "y1": 79.8, "y2": 283.8},
#     {"page": 1, "extraction_method": "stream", "selection_id": "J1742359651382", "x1": 434.4, "x2": 956.4, "y1": 73.8, "y2": 339},
#     {"page": 1, "extraction_method": "stream", "selection_id": "U1742359655886", "x1": 16.8, "x2": 393.6, "y1": 453, "y2": 539.4}
# ]

# def extract_tables_from_pdf(pdf_path):
#     print("EVERYTHING GOOD GOOD GOOD GOOD GOOD OGOD 1")
#     pdf_path = os.path.join(PROJECT_ROOT, "../worklets", pdf_path)
#     print("EVERYTHING GOOD GOOD GOOD GOOD GOOD OGOD 2")
#     extracted_tables = []
#     for param in parameters:
#         area = [param["y1"], param["x1"], param["y2"], param["x2"]]
#         tables = tabula.read_pdf(pdf_path, pages=param["page"], area=area, stream=True)
#         if isinstance(tables, list):
#             extracted_tables.extend([table.to_dict(orient="records") for table in tables])
#         else:
#             extracted_tables.append(tables.to_dict(orient="records"))
#     print("EVERYTHING GOOD GOOD GOOD GOOD GOOD OGOD 3")
#     return json.dumps(extracted_tables)

# #configure it before u run on ur machine
# if __name__ == "__main__":
#     pdf_path = "../../worklets/Kanpur-1742112366211.pdf"
#     extracted_data = extract_tables_from_pdf(pdf_path)
#     print(extracted_data)
