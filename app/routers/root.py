import aiofiles
import asyncio
import json
import os
import re
import shutil
import tempfile
import time
import traceback
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, Form, Query, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.llm import llm
from app.socket import is_client_connected, sio
from app.utils.generate_references import getReferenceWork
from app.utils.generate_worklets import generate_worklets
from app.utils.generatepdf import generatePdf
from app.utils.link_extractor import get_links_data
from app.utils.document_parser import extract_document

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

def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '_', filename)

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post('/upload')
async def upload_multiple(
    model: Annotated[str, Query()],
    sid: Annotated[str, Form()],
    links: Annotated[str, Form()],
    custom_prompt: Annotated[str, Form()],
    custom_topics: Annotated[str, Form()],
    files: Annotated[list[UploadFile], File()] = None,
):
    """
    The main route that handles the upload of multiple files and links, processes the data, generates worklets, 
    fetches references, and creates PDFs.
    Args:
        model (str): The model to be used for processing.
        sid (str): The session ID for the client.
        links (str): A JSON string containing links to be processed.
        custom_prompt (str): An optional custom prompt for processing.
        custom_topics (str): An optional JSON string containing custom topics as an array.
        files (list[UploadFile], optional): A list of files uploaded by the user.
    Returns:
        dict: A response containing the generated files or an error message if the client is not connected.
    Raises:
        json.JSONDecodeError: If the `links` or `custom_topics` JSON strings cannot be parsed.
        Exception: If an error occurs during PDF generation or other processing steps.
    Workflow:
        1. Saves uploaded files to the server.
        2. Extracts data from the uploaded files concurrently.
        3. Processes the provided links and extracts data.
        4. Generates worklets based on the extracted data, links, and custom inputs.
        5. Moves old generated files to a backup directory.
        6. Fetches references for each generated worklet.
        7. Saves the latest generated worklets to a JSON file.
        8. Generates PDFs for each worklet and sends progress updates to the client.
    Notes:
        - Emits progress updates to the client using Socket.IO.
        - Checks if the client is connected at various stages and halts processing if disconnected.
    """

    parsed_custom_topics = json.loads(custom_topics) if custom_topics else []
    start_time = time.time()
    saved_files = []
    extracted_data_all = {}

    # 1. Save uploaded files
    if files:
        await sio.emit("progress", {"message": "Extracting data from files..."}, to=sid)
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

    # 3. Handle links
    links_data = {}
    try:
        parsed_links = json.loads(links)

        if parsed_links:
            await sio.emit("progress", {"message": "Extracting data from links..."}, to=sid)
            loop = asyncio.get_running_loop()
            links_data = await loop.run_in_executor(None, get_links_data, parsed_links)
    except json.JSONDecodeError as e:
        print("Error decoding links JSON:", e)

    # Summarise extracted data into worklets

    # 4. generating worklets here

    if not is_client_connected(sid):
        print(f"Client {sid} is not connected. Skipping worklet generation. Returning error.")
        return {"error": "Client not connected."}

    worklets = await generate_worklets(
        extracted_data_all, links_data, model, sid, custom_prompt, parsed_custom_topics
    )
    print("returning")
    return;
    if not is_client_connected(sid):
        print(f"Client {sid} is not connected. Skipping fetching references. Returning error.")
        return {"error": "Client not connected."}

    # 5. Move old generated files
    loop = asyncio.get_running_loop()

    for filename in os.listdir(GENERATED_DIR):
        source_path = os.path.join(GENERATED_DIR, filename)
        destination_path = os.path.join(DESTINATION_DIR, filename)
        if os.path.isfile(source_path):
            await loop.run_in_executor(None, shutil.move, source_path, destination_path)

    # 6. Generate references concurrently
    async def process_worklet(worklet):
        reference = await getReferenceWork(worklet["Problem Statement"], worklet["Title"], model)
        worklet["Reference Work"] = reference

    for worklet in worklets:
        await sio.emit("progress", {"message": f"Fetching references for {worklet['Title']}"}, to=sid)
        await process_worklet(worklet)

    # 7. Save latest generated worklets and give index to references
    for worklet in worklets:
        idx = 12
        for idx, ref in enumerate(worklet["Reference Work"]):
            ref["reference_id"] = idx 
    async with aiofiles.open("latest_generated.json", "w") as file:
        await file.write(json.dumps(worklets, indent=4))

    # 8. Generate PDFs
    response = {"files": []}

    if not is_client_connected(sid):
        print(f"Client {sid} is not connected. Skipping PDF generation. Returning error.")
        return {"error": "Client not connected."}

    await sio.emit("progress", {"message": "Generating PDFs..."}, to=sid)
    for index, worklet in enumerate(worklets):
        try:
            await sio.emit("progress", {"message": f"Generating PDF for {index + 1}. {worklet['Title']}..."}, to=sid)
            file_name = sanitize_filename(worklet['Title'])
            await sio.emit("fileReceived", {"file_name": f"{file_name}.pdf"}, to=sid)
            await sio.emit("progress", {"message": f"Comparing references for {index + 1}. {worklet['Title']}..."},to=sid)
            await generatePdf(worklet, model, index)

            filename = f"{worklet['Title']}.pdf"
        except Exception as e:
            traceback.print_exc()
            filename = "error.pdf"

        response["files"].append({
            "name": filename,
        })

        await sio.emit("pdf_generated", {"file_name": filename}, to=sid)
        if not is_client_connected(sid):
            print(f"Client {sid} is not connected. Skipping next file. Returning error.")
            return {"error": "Client not connected."}

    end_time = time.time()
    elapsed_time = end_time - start_time
    await sio.emit("progress", {"message": f"{elapsed_time}"}, to=sid)
    await asyncio.sleep(1)
    return response

@router.get('/download/{file_name}')
async def download(file_name: str):
    new_file_name = sanitize_filename(file_name)
    file_path = Path(GENERATED_DIR) / new_file_name

    if not file_path.exists():
        file_path = Path(DESTINATION_DIR) / new_file_name

    safe_filename = file_name.replace(":", " -")
    if file_path.exists():
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=safe_filename 
        )
    return {"error": "File not found"}
class FilesRequest(BaseModel):
    files: list[str] 

@router.post("/download_all")
def download_selected(filesss: FilesRequest):
    """
    Handles the creation of a downloadable ZIP file containing the specified files.
    Args:
        filesss (FilesRequest): An object containing a list of file names to be included in the ZIP file.
    Returns:
        FileResponse: A response object containing the generated ZIP file for download.
        dict: An error message if no files are provided.
    Workflow:
        1. Validates the input to ensure files are provided.
        2. Creates a temporary ZIP file.
        3. Searches for the specified files in the `GENERATED_DIR` directory and adds them to the ZIP file.
        4. Searches for any remaining files in the `DESTINATION_DIR` directory and adds them to the ZIP file.
        5. Returns the ZIP file as a downloadable response.
    Notes:
        - The function assumes the existence of `GENERATED_DIR` and `DESTINATION_DIR` directories.
        - If a file is not found in either directory, it will be skipped without raising an error.
        - The temporary ZIP file is not automatically deleted after the response is sent.
    """

    files = filesss.files 
    if not files:
        return {"error": "No files provided."}

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
    message = llm.invoke(query.query)
    return message.content
