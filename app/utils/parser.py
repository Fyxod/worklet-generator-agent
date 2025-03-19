import pandas as pd
from tabula.io import read_pdf
import tabula
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "../worklets")

parameters = [
    {"page": 1, "extraction_method": "stream", "selection_id": "K1742359645874", "x1": 12, "x2": 412.8, "y1": 79.8, "y2": 283.8},
    {"page": 1, "extraction_method": "stream", "selection_id": "J1742359651382", "x1": 434.4, "x2": 956.4, "y1": 73.8, "y2": 339},
    {"page": 1, "extraction_method": "stream", "selection_id": "U1742359655886", "x1": 16.8, "x2": 393.6, "y1": 453, "y2": 539.4}
]

def extract_tables_from_pdf(pdf_path):
    print("EVERYTHING GOOD GOOD GOOD GOOD GOOD OGOD 1")
    pdf_path = os.path.join(PROJECT_ROOT, "../worklets", pdf_path)
    print("EVERYTHING GOOD GOOD GOOD GOOD GOOD OGOD 2")
    extracted_tables = []
    for param in parameters:
        area = [param["y1"], param["x1"], param["y2"], param["x2"]]
        tables = tabula.read_pdf(pdf_path, pages=param["page"], area=area, stream=True)
        if isinstance(tables, list):
            extracted_tables.extend([table.to_dict(orient="records") for table in tables])
        else:
            extracted_tables.append(tables.to_dict(orient="records"))
    print("EVERYTHING GOOD GOOD GOOD GOOD GOOD OGOD 3")
    return json.dumps(extracted_tables)

#configure it before u run on ur machine
if __name__ == "__main__":
    pdf_path = "../../worklets/Kanpur-1742112366211.pdf"
    extracted_data = extract_tables_from_pdf(pdf_path)
    print(extracted_data)
