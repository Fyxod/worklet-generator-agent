from app.llm import llm
from typing import Annotated
from fastapi import  UploadFile, File
import os
import aiofiles
from datetime import datetime
from fastapi import APIRouter
import shutil
from pathlib import Path
from pydantic import BaseModel
from fastapi.responses import RedirectResponse, FileResponse
from app.utils.parser import extract_tables_from_pdf
from app.utils.parser2 import extract_document
from app.utils.generate_worklets import generate_worklets
from app.utils.generatepdf import generatePdf


class Query(BaseModel):
    query: str

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "../worklets")
os.makedirs(UPLOAD_DIR, exist_ok=True)

GENERATED_DIR = os.path.join(PROJECT_ROOT, "./resources/generated_worklets")
DESTINATION_DIR = os.path.join(PROJECT_ROOT, "./resources/archived_worklets")
os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(DESTINATION_DIR, exist_ok=True)

router=APIRouter(
    prefix='',
    tags=['root']
)

@router.get('/')
def read_root():
    return RedirectResponse(url="http://localhost:8501")

@router.get("/home")
def frontend_redirect():
    return RedirectResponse(url="http://localhost:8501")
    
@router.post('/upload')
async def upload_multiple(files: Annotated[list[UploadFile], File()]):
    print("printong",files)
    
    saved_files = []

    for file in files:
        timestamp = int(datetime.now().timestamp() * 1000)  

        filename, ext = os.path.splitext(file.filename)

        new_filename = f"{filename}-{timestamp}{ext}"  
        file_path = os.path.join(UPLOAD_DIR, new_filename)

        async with aiofiles.open(file_path, "wb") as buffer:
            content = await file.read() 
            await buffer.write(content)

        saved_files.append(new_filename)

    extracted_data_all = {}
    for index, file in enumerate(saved_files):
        extracted_data_single = await extract_document(file)
        # print(extracted_data_single)
        extracted_data_all[index + 1] = extracted_data_single  # Number from 1 instead of 0

    # Convert to a formatted string
    formatted_output = "\n\n".join(
        [f"--- Extracted Data from File {idx} ---\n{data}" for idx, data in extracted_data_all.items()]
    )
    print(formatted_output)  # Print for debugging

    # call llm here with extracted_data_all
    worklets =  await generate_worklets(extracted_data_all)

    # moving old files
    for filename in os.listdir(GENERATED_DIR):
        source_path = os.path.join(GENERATED_DIR, filename)
        destination_path = os.path.join(DESTINATION_DIR, filename)

        if os.path.isfile(source_path):
            shutil.move(source_path, destination_path)
    
    response = {"files":[]}
    for worklet in worklets["worklets"]:
        generatePdf(worklet)
        response["files"].append({"name": f'{worklet["Title"]}.pdf', "url": f"http://localhost:8000/download/{worklet['Title']}.pdf"})
        
    return response
    # return {worklets}
    # return extracted_data_all

@router.get('/download/{file_name}')
async def download(file_name: str):
    print(file_name)
    
    file_path = Path(GENERATED_DIR) / file_name  # Convert to Path object
    print(file_path)
    
    if file_path.exists():  # Now it works
        return FileResponse(file_path, media_type="application/pdf", filename=file_name)
    
    return {"error": "File not found"}

@router.post('/query')
async def create_query(query:Query):
    # will add db soon for authentication and saving llm output
    print(query.query)
    message = llm.invoke(query.query)
    print(message.content)
    return message.content