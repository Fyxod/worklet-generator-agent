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


# # # #
# i want you to create a single page html page that does the following thins - 

# gives you option to upload files of any format among pdf, docx, ppt, text file and image with size limit of 100 mb. send these under the field "files". Also give the option to cancel any or all files if needed.

# give a dropdown to choose among the following ml models - 

# {
#     "Gemini Flash 2.0": "gemini-flash-2.0",
#     "DeepSeek R1 (70B)": "deepseek-r1:70b",
#     "LLaMA 3.3": "llama3.3:latest",
#     "Gemma 3 (27B)": "gemma3:27b",
#     "Command A": "command-a:latest"
# }

# show the proper name on the frontend but send the value on the backend under the name "model"

# also give a option to add any number of links and send them as an array under "links".

# then give a button "Generate worklets". when it is clicked, it will show a loading icon just below it. 

# you will then receive 5 files from backend. give option to download them individually or all of them combined as a zip. this is how i was doing it earlier 
#     if "files" in data:
#         st.success("Files successfully generated! 🎉")
#         st.write("### Download Generated PDFs:")
#         for file in data["files"]:
#             file_name_encoded = urllib.parse.quote(file["name"])
#             download_url = f"{FASTAPI_URL}/download/{file_name_encoded}"
#             st.markdown(f"[📄 {file['name']}]({download_url})")

# The heading of the page will be "Worklet generator agent"
# # # #