from llm import llm
from typing import Annotated
from fastapi import  UploadFile, File
import os
import aiofiles
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

class Query(BaseModel):
    query: str

UPLOAD_DIR="../worklets"
os.makedirs(UPLOAD_DIR, exist_ok=True)


router=APIRouter(
    prefix='/',
    tags=['root']
)

@router.get('/')
def read_root():
    print("here")
    return {
        4:"yo"
    }
    
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

        saved_files.append(file_path)

    return {"saved_files": saved_files}

@router.post('/query')
async def create_query(query:Query):
    # will add db soon for authentication and saving llm output
    print(query.query)
    message = llm.invoke(query.query)
    print(message.content)
    return message.content