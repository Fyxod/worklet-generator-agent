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
    Args:
        content_bytes (bytes): The byte content of the image file.
    Returns:
        str: The text extracted from the image.
    Note:
        This function uses the PIL library to open the image and the pytesseract library
        to perform Optical Character Recognition (OCR) on the image.
    """
    
    image = Image.open(io.BytesIO(content_bytes))
    text = pytesseract.image_to_string(image)
    return text

def extract_visible_text(html):
    """
    Extracts and returns a trimmed version of visible text from the given HTML content.
    This function removes non-visible elements such as <script>, <style>, and <noscript> tags,
    extracts the title, meta description, and visible body text, and combines them into a single
    string. The resulting text is limited to the first 100 words.
    Args:
        html (str): The HTML content as a string.
    Returns:
        str: A string containing the first 100 words of the visible text extracted from the HTML.
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
    """
        Extracts content from a given URL based on its content type, with an optional word limit.
        Args:
            url (str): The URL to fetch and extract content from.
            word_limit (int, optional): The maximum number of words to extract. Defaults to 100.
        Returns:
            str: Extracted content from the URL, truncated to the specified word limit. 
                 Returns an error message or empty string if extraction fails or the content type is unsupported.
        Supported Content Types:
            - PDF: Extracts text from PDF files.
            - Image: Extracts text from images using OCR.
            - HTML: Extracts visible text from HTML pages.
            - JSON: Flattens and extracts text from JSON responses.
            - Plain Text/Markdown: Extracts plain text or markdown content.
        Notes:
            - Requires external libraries such as `requests`, `magic`, `fitz` (PyMuPDF), and `re`.
            - Handles exceptions and returns an empty string in case of errors.
        """
    
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
    """
    Extracts and processes content from a list of URLs concurrently.
    This function uses a ThreadPoolExecutor to fetch and process the content
    of each URL in the provided list of links. The results are returned as a
    dictionary where each URL is mapped to its corresponding processed content.
    Args:
        links (list): A list of URLs (strings) to extract and process content from.
    Returns:
        dict: A dictionary where the keys are the URLs from the input list and
              the values are the processed content extracted from each URL.
    """
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(extract_content_from_link, links))
    obj = {};
    for url, result in zip(links, results):
        obj[url] = result
    return obj
