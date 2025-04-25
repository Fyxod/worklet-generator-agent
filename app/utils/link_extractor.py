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

def extract_content_from_link(url):
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
            return " ".join(text.split()[:100])

        else:
            return f"Unsupported content type: {content_type}"

    except Exception as e:
        return f"Error occurred: {str(e)}"

links = [
"https://ml-ops.org/img/crisp-ml-process.jpg",
"https://github.com/microsoft/RD-Agent/",
"https://pypi.org/project/python-magic/",
"https://arxiv.org/pdf/2407.07506",
"https://arxiv.org/abs/2407.07506",
"https://cdn.prod.website-files.com/660ef16a9e0687d9cc27474a/662c3c84010d1a7f60040660_653fd7c778ef8ed0e9498e4a_model_monitoring11.png",
"https://viso.ai/wp-content/uploads/2021/01/confusion-matrix-ml-model-1.png",
"https://www.mygreatlearning.com/blog/wp-content/uploads/2023/07/select-right-ml-model.png"
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

# get_link_data(links)