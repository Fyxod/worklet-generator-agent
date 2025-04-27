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

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/home")
def frontend_redirect():
    return RedirectResponse(url="http://localhost:8501")

# Generate worklets is hitting this endpoint althe function alss happen here
@router.post('/upload')
async def upload_multiple(
    files: Annotated[list[UploadFile], File()],
    model: Annotated[str, Query()],
    links: Annotated[str, Form()]  # expecting JSON string from frontend
):
    # print("Model selected:", model)
    # print("Uploaded files:", files)
    # your processing logic
    
    saved_files = []
    extracted_data_all = {}
    # print("printing files", files)
    
    if files:
    # Save each file with a timestamp
        print("files have been uploaded")
        for file in files:
            timestamp = int(datetime.now().timestamp() * 1000)  

            filename, ext = os.path.splitext(file.filename)

            new_filename = f"{filename}-{timestamp}{ext}"  
            file_path = os.path.join(UPLOAD_DIR, new_filename)

            async with aiofiles.open(file_path, "wb") as buffer:
                content = await file.read() 
                await buffer.write(content)

            saved_files.append(new_filename)

        for index, file in enumerate(saved_files):
            extracted_data_single = await extract_document(file)
            extracted_data_all[index + 1] = extracted_data_single  # Number from 1 instead of 0
    else:
        print("No files uploaded")
    
    linksData = {}
    try:
        parsed_links = json.loads(links) 
        print("print length of links", len(parsed_links))
        print("HEERE ARE LINKS")
        print(parsed_links)
        if parsed_links:
            linksData = get_links_data(parsed_links)
    except json.JSONDecodeError as e:
        print("Error decoding links JSON:", e)

    #Summarise extracted data

    # generate worklet content 
    worklets =  await generate_worklets(extracted_data_all,linksData, model)

    # moving old files
    for filename in os.listdir(GENERATED_DIR):
        source_path = os.path.join(GENERATED_DIR, filename)
        destination_path = os.path.join(DESTINATION_DIR, filename)

        if os.path.isfile(source_path):
            shutil.move(source_path, destination_path)

    #get references
    def process_worklet(worklet):
        print("\n")
        print("--------------------------------------------------------Generating referances-----------------------------------------------------------")
        print("\n")

        reference = getReferenceWork(worklet["Title"], model)
        # print(reference)
        # print("8"*200)
        if reference:
            worklet["Reference Work"] = reference


    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(executor.map(process_worklet, worklets))

    # for worklet in worklets:
    #     # print("DEUBGGING HERE DEBIGGING HERE DEBUGGING HERE DEBBUGING HERE")
    #     # print(worklet)
    #     print("fertchign refrences for ",worklet["Title"])
    #     process_worklet(worklet)
    
######## Indication 2###########
    with open("latest_generated.json", "w") as file:
        json.dump(worklets, file, indent=4)

    print("\n")    
    print("-------"*25+"final"+"---------"*25) #printing final here
    print("\n")
    print(worklets)

    # for loop one
    response = {"files":[]}
    # for worklet in worklets:
    #     generatePdf(worklet, model)
    #     response["files"].append({"name": f'{worklet["Title"]}.pdf', "url": f"http://localhost:8000/download/{worklet['Title']}.pdf"})

    for index, worklet in enumerate(worklets):
        try:
            print("Generating PDF for:", worklet["Title"])
            generatePdf(worklet, model, index)
            filename = f'{worklet["Title"]}.pdf'
        except Exception as e:
            print(f"Error generating PDF for {worklet['Title']}: {e}")
            traceback.print_exc()   
            filename = f'error.pdf'
        response["files"].append({
            "name": filename,
            "url": f"http://localhost:8000/download/{filename}"
        })
        await sio.emit("pdf_generated", {"file_name": filename})
        time.sleep(2) 
    
    return response
    #thread one
    # response = {"files": []}

    # def generate(worklet):
    #     generatePdf(worklet, model)
    #     return {
    #         "name": f'{worklet["Title"]}.pdf',
    #         "url": f"http://localhost:8000/download/{worklet["Title"]}.pdf"
    #     }

    # with ThreadPoolExecutor() as executor:
    #     loop = asyncio.get_running_loop()
    #     results = await asyncio.gather(
    #         *[loop.run_in_executor(executor, generate, worklet)
    #         for worklet in worklets]
    #     )

    # response["files"] = results

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

@router.get("/download_all")
def download_all():
    """Zips all files in the specified directory and returns the zip file."""
    if not os.path.exists(GENERATED_DIR):
        return {"error": "Directory not found"}
    
    # Create a temporary zip file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
        zip_path = temp_zip.name
    
    shutil.make_archive(zip_path[:-4], 'zip', GENERATED_DIR)
    
    return FileResponse(zip_path, filename="worklets.zip", media_type="application/zip")


@router.post('/query')
async def create_query(query:Query1):
    # will add db soon for authentication and saving llm output
    print(query.query)
    message = llm.invoke(query.query)
    # message = llm.invoke([HumanMessage(content=query.query)])
    print(message.content)
    return message.content