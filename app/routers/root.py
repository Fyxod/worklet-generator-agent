from app.llm import llm
from typing import Annotated
from fastapi import  UploadFile, File
import os
import aiofiles
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from app.utils.parser import extract_tables_from_pdf

class Query(BaseModel):
    query: str

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "../worklets")

os.makedirs(UPLOAD_DIR, exist_ok=True)

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
        extracted_data_single = extract_tables_from_pdf(file)
        print(extracted_data_single)
        extracted_data_all[index] = extracted_data_single
    return extracted_data_all
    # return {"saved_files": saved_files}

@router.post('/query')
async def create_query(query:Query):
    # will add db soon for authentication and saving llm output
    print(query.query)
    message = llm.invoke(query.query)
    print(message.content)
    return message.content