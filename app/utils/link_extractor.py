import requests
import magic
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import time
from PIL import Image
import pytesseract
import io
import re
import json
import concurrent.futures

start_time = time.time()


def extract_text_from_image(content_bytes):
    image = Image.open(io.BytesIO(content_bytes))
    text = pytesseract.image_to_string(image)
    print("image done")
    return text

def extract_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title else ""
    meta_desc = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        meta_desc = desc_tag["content"].strip()

    body_text = soup.get_text(separator=' ', strip=True)

    full_text = f"{title}. {meta_desc}. {body_text}".strip()
    words = full_text.split()
    trimmed = " ".join(words[:100])
    print("html done")
    return trimmed

def extract_content_from_link(url,word_limit: int =100):
    try:
        response = requests.get(url, timeout=10)
        content_type = magic.from_buffer(response.content, mime=True).lower()

        if "pdf" in content_type:
            doc = fitz.open(stream=response.content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
                if len(text.split()) >= 100:
                    break
            print("pdf done")
            return " ".join(text.split()[:100])

        elif "image" in content_type:
            return re.sub(r'\s+', ' ', extract_text_from_image(response.content)).strip()

        elif "html" in content_type:
            return extract_visible_text(response.text)

        elif "json" in content_type:
            try:
                data = response.json()
                flat_text = json.dumps(data, indent=2)
                print("json done")
                return " ".join(flat_text.split()[:100])
            except json.JSONDecodeError:
                return "Invalid JSON content."

        elif "plain" in content_type or "markdown" in content_type:
            text = response.text
            print("plain/markdown done")
            return " ".join(text.split()[:word_limit])

        else:
            return f"Unsupported content type: {content_type}"

    except Exception as e:
        return f"Error occurred: {str(e)}"

links = [
"https://www.techtarget.com/searchmobilecomputing/definition/wearable-technology",
"https://builtin.com/wearables",
"https://pypi.org/project/python-magic/",
"https://hubtechinfo.com/10-examples-of-wearable-technology/",

]
# end_time = time.time()
# print(f"Execution time: {end_time - start_time:.2f} seconds")

def get_links_data(links: list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(extract_content_from_link, links))
    obj = {};
    for url, result in zip(links, results):
        obj[url] = result
    print("printing LINKS DATA")
    print(obj)
    print("ENDING LINKS DATA")
    return obj
# print("ssssssssssssssssssssssssssssssssssss")
# print(get_links_data(links))