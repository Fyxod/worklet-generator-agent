from app.llm import llm
from typing import Annotated
from fastapi import  UploadFile, File, Query, Form
import os
import aiofiles
from datetime import datetime
from fastapi import APIRouter
import traceback
import shutil
from pathlib import Path
from pydantic import BaseModel
from fastapi.responses import RedirectResponse, FileResponse
from app.utils.parser import extract_document
from app.utils.generate_worklets import generate_worklets
from app.utils.generatepdf import generatePdf
from app.utils.generate_references import getReferenceWork
import tempfile
import concurrent.futures
from langchain.schema.messages import HumanMessage
from concurrent.futures import ThreadPoolExecutor
import asyncio
from app.utils.link_extractor import get_links_data
import json
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import time
from app.socket import sio
import zipfile
import re

class Query1(BaseModel):
    query: str

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "../worklets")
os.makedirs(UPLOAD_DIR, exist_ok=True)

GENERATED_DIR = os.path.join(PROJECT_ROOT, "./resources/generated_worklets")
DESTINATION_DIR = os.path.join(PROJECT_ROOT, "./resources/archived_worklets")
os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(DESTINATION_DIR, exist_ok=True)
os.makedirs("templates", exist_ok=True)

router=APIRouter(
    prefix='',
    tags=['root']
)

templates = Jinja2Templates(directory="templates")

# @router.get('/')
# def read_root():
#     return{ "response": "API IS UP AND RUNNING"}

def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '_', filename)

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/home")
def frontend_redirect():
    return RedirectResponse(url="http://localhost:8501")

# Generate worklets is hitting this endpoint althe function alss happen here
@router.post('/upload')
async def upload_multiple(
    model: Annotated[str, Query()],
    sid: Annotated[str, Form()],
    links: Annotated[str, Form()],  # expecting JSON string from frontend
    files: Annotated[list[UploadFile], File()] = None,
):
    saved_files = []
    extracted_data_all = {}


    # 1. Save uploaded files
    if files:
        await sio.emit("progress", {"message": "Extracting data from files..."}, to=sid)
        print("Files have been uploaded")
        for file in files:
            timestamp = int(datetime.now().timestamp() * 1000)
            filename, ext = os.path.splitext(file.filename)
            new_filename = f"{filename}-{timestamp}{ext}"
            file_path = os.path.join(UPLOAD_DIR, new_filename)

            async with aiofiles.open(file_path, "wb") as buffer:
                content = await file.read()
                await buffer.write(content)

            saved_files.append(new_filename)

        # 2. Extract data from files concurrently
        extracted_data_tasks = [
            extract_document(file, sid) for file in saved_files
        ]
        extracted_results = await asyncio.gather(*extracted_data_tasks)

        extracted_data_all = {i + 1: data for i, data in enumerate(extracted_results)}
    else:
        print("No files uploaded")

    # 3. Handle links
    linksData = {}
    try:
        parsed_links = json.loads(links)
        print(f"Received {len(parsed_links)} links.")
        print("HEERE ARE LINKS")
        print(parsed_links)
        
        if parsed_links:
            await sio.emit("progress", {"message": "Extracting data from links..."}, to=sid)
            # Assuming get_links_data is sync, offload it
            loop = asyncio.get_running_loop()
            linksData = await loop.run_in_executor(None, get_links_data, parsed_links)
    except json.JSONDecodeError as e:
        print("Error decoding links JSON:", e)

    #Summarise extracted data into worklets


    # 4. generating worklets here
    await sio.emit("progress", {"message": "Generating worklets..."}, to=sid)
    worklets = await generate_worklets(extracted_data_all, linksData, model, sid)

    # loop = asyncio.get_running_loop()
    # worklets = await loop.run_in_executor(None, generate_worklets, extracted_data_all, linksData, model)

    # 5. Move old generated files
    loop = asyncio.get_running_loop()

    for filename in os.listdir(GENERATED_DIR):
        source_path = os.path.join(GENERATED_DIR, filename)
        destination_path = os.path.join(DESTINATION_DIR, filename)
        if os.path.isfile(source_path):
            await loop.run_in_executor(None, shutil.move, source_path, destination_path)

    # 6. Generate references concurrently
    async def process_worklet(worklet):
        print(f"-----------Generating reference for: {worklet['Title']}------------------")
        loop = asyncio.get_running_loop()
        reference = await loop.run_in_executor(None, getReferenceWork, worklet["Title"], model)
        worklet["Reference Work"] = reference

    await sio.emit("progress", {"message": "Fetching references..."}, to=sid)
    for worklet in worklets:
        print("fertchign refrences for ",worklet["Title"])
        await process_worklet(worklet)
    
    # await asyncio.gather(*(process_worklet(worklet) for worklet in worklets))

    # 7. Save latest generated worklets and give index to references
    for worklet in worklets:
        idx = 12
        for idx, ref in enumerate(worklet["Reference Work"]):
            ref["reference_id"] = idx 
    async with aiofiles.open("latest_generated.json", "w") as file:
        await file.write(json.dumps(worklets, indent=4))

    print("\n" + "-------" * 25 + "FINAL" + "---------" * 25 + "\n")
    print(worklets)
    
    # 8. Generate PDFs
    response = {"files": []}

    await sio.emit("progress", {"message": "Generating PDFs..."}, to=sid)
    for index, worklet in enumerate(worklets):
        try:
            print(f"Generating PDF for: {worklet['Title']}")
            await sio.emit("progress", {"message": f"Generating PDF for {index + 1}. {worklet['Title']}..."}, to=sid)
            file_name = sanitize_filename(worklet['Title'])
            await sio.emit("fileReceived", {"file_name": f"{file_name}.pdf"}, to=sid)
            await sio.emit("progress", {"message": f"Comparing references for {index + 1}. {worklet['Title']}..."},to=sid)
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, generatePdf, worklet, model, index)

            filename = f"{worklet['Title']}.pdf"
        except Exception as e:
            print(f"Error generating PDF for {worklet['Title']}: {e}")
            traceback.print_exc()
            filename = "error.pdf"

        response["files"].append({
            "name": filename,
        })

        await sio.emit("pdf_generated", {"file_name": filename}, to=sid)

    await asyncio.sleep(1)
    return response


@router.get('/download/{file_name}')
async def download(file_name: str):
    print(file_name)

    # Search in GENERATED_DIR first
    file_path = Path(GENERATED_DIR) / file_name
    print(file_path)

    if not file_path.exists():  # If not found in GENERATED_DIR, search in DESTINATION_DIR
        print(f"File not found in {GENERATED_DIR}. Searching in {DESTINATION_DIR}.")
        file_path = Path(DESTINATION_DIR) / file_name

    if file_path.exists():
        return FileResponse(file_path, media_type="application/pdf", filename=file_name)

    return {"error": "File not found"}
class FilesRequest(BaseModel):
    files: list[str]  # Array of strings (filenames)

@router.post("/download_all")
def download_selected(
    filesss: FilesRequest
    ):
    """Zips specified files from GENERATED_DIR or ARCHIVED_DIR and returns the zip file."""
    files = filesss.files  # Extract the list of filenames from the request body
    print(files)
    if not files:
        return {"error": "No files provided."}
    print(files)

    # Create a temporary zip file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
        zip_path = temp_zip.name

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # Make a copy so we can modify files safely
        remaining_files = files.copy()

        # First, search and add files from GENERATED_DIR
        for file_name in files:
            file_path = os.path.join(GENERATED_DIR, file_name)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=file_name)
                remaining_files.remove(file_name)

        # Then, search remaining files in ARCHIVED_DIR
        for file_name in remaining_files:
            file_path = os.path.join(DESTINATION_DIR, file_name)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=file_name)

    return FileResponse(zip_path, filename="worklets.zip", media_type="application/zip")


@router.post('/query')
async def create_query(query:Query1):
    # will add db soon for authentication and saving llm output
    print(query.query)
    message = llm.invoke(query.query)
    # message = llm.invoke([HumanMessage(content=query.query)])
    print(message.content)
    return message.content

