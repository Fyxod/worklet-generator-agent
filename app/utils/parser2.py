from pathlib import Path
from kreuzberg import extract_file
from kreuzberg import ExtractionResult
# from kreuzberg import PSMMode
async def extract_document(name):
    # Extract from a PDF file with default settings
    pdf_result: ExtractionResult = await extract_file(name)
    print(f"Content: {pdf_result.content}")

    # use this library to run it asyncrousnly
# import asyncio
# name="d.pdf"
# asyncio.run(extract_document(name))


#before using it runcmd as admin and run      choco install -y tesseract pandoc
#  then install pip install kreuzberg