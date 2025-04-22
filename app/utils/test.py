import fitz  # PyMuPDF
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import io

def clean_text(text):
    return ' '.join(text.lower().strip().split())

def extract_text_combined(pdf_path):
    doc = fitz.open(pdf_path)
    full_output = []

    for i, page in enumerate(doc):
        print(f"\n--- Page {i+1} ---")

        # Step 1: Native Text
        native_text = page.get_text().strip()
        native_clean = clean_text(native_text)
        print("[Native Text]")
        print(native_text if native_text else "(None found)")

        # Step 2: OCR Text
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        ocr_text = pytesseract.image_to_string(img).strip()
        ocr_lines = [line for line in ocr_text.splitlines() if line.strip()]
        print("\n[OCR Raw Text]")
        print('\n'.join(ocr_lines) if ocr_lines else "(None found)")

        # Step 3: Filter OCR lines not already in native
        merged_lines = []
        for line in ocr_lines:
            if clean_text(line) not in native_clean:
                merged_lines.append(line)

        # Step 4: Final merge
        combined_text = native_text + "\n\n[Extra OCR Text]\n" + "\n".join(merged_lines) if merged_lines else native_text
        full_output.append(combined_text)

    # Join all pages
    return "\n\n".join(full_output)

# Example usage:
final_text = extract_text_combined("hello.pdf")
print("\n\n=== Final Combined Text ===\n")
print(final_text)
