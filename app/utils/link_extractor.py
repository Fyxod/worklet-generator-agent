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
    """
    Extracts text from an image provided as byte content.
    This function takes the byte content of an image, processes it using the 
    Python Imaging Library (Pillow) to open the image, and then uses Tesseract 
    OCR (via pytesseract) to extract text from the image.
    Args:
        content_bytes (bytes): The byte content of the image to be processed.
    Returns:
        str: The text extracted from the image.
    Raises:
        IOError: If the image cannot be opened or processed.
        pytesseract.TesseractError: If Tesseract OCR encounters an error.
    """

    image = Image.open(io.BytesIO(content_bytes))
    text = pytesseract.image_to_string(image)
    return text


def extract_visible_text(html):
    """
    Extracts and returns the first 100 words of visible text from the given HTML content.
    This function processes the HTML content to remove non-visible elements such as 
    <script>, <style>, and <noscript> tags. It also extracts the title and meta 
    description (if available) and combines them with the visible body text. The 
    resulting text is trimmed to the first 100 words.
    Args:
        html (str): The HTML content as a string.
    Returns:
        str: A string containing the first 100 words of the visible text extracted 
        from the HTML, including the title and meta description if present.
    """

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
                if len(text.split()) >= word_limit:
                    break
            return " ".join(text.split()[:word_limit])

        elif "image" in content_type:
            return re.sub(r'\s+', ' ', extract_text_from_image(response.content)).strip()

        elif "html" in content_type:
            return extract_visible_text(response.text)

        elif "json" in content_type:
            try:
                data = response.json()
                flat_text = json.dumps(data, indent=2)
                return " ".join(flat_text.split()[:word_limit])
            except json.JSONDecodeError:
                return "Invalid JSON content."

        elif "plain" in content_type or "markdown" in content_type:
            text = response.text
            return " ".join(text.split()[:word_limit])

        else:
            return f"Unsupported content type: {content_type}"

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""


def get_links_data(links: list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(extract_content_from_link, links))
    obj = {};
    for url, result in zip(links, results):
        obj[url] = result
    print(obj)
    return obj