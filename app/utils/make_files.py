import asyncio
import os
import re

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

from app.utils.reference_functions.reference_sort import index_sort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

ppt_path = os.path.join(PROJECT_ROOT, "resources/generated_worklets/ppt")
pdf_path = os.path.join(PROJECT_ROOT, "resources/generated_worklets/pdf")

os.makedirs(pdf_path, exist_ok=True)
os.makedirs(ppt_path, exist_ok=True)


CUSTOM_PAGE_SIZE = (750,900)  # Width x Height in points (1 point = 1/72 inch)  used by both ppt and pdf

async def generatePdf(json, model, index):
    print("\n")
    print("----" * 25 + "Inside make_file " + "----" * 25)
    print("\n")

    json_data = await pre_processing(json, index, model) # json after sorting
    
    safe_title = sanitize_filename(json.get("Title", "untitled"))
    
    filename_pdf = os.path.join(pdf_path, f"{safe_title}.pdf")
    filename_ppt = os.path.join(ppt_path, f"{safe_title}.pptx")

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, create_pdf, filename_pdf, json_data)
    await loop.run_in_executor(None, create_ppt, filename_ppt, json_data)
    

    print("\n")
    print(f"PDF generated: {filename_pdf}")
    print("\n")
    
    
    
async def pre_processing(json_data, index, model="gemma3:27b"):
    json_data = await index_sort(json_data, model, index)
    return json_data

def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '_', filename)


# Function to handle the actual blocking PDF generation using ReportLab
def create_pdf(filename, json_data):
    pdf = canvas.Canvas(filename, pagesize=CUSTOM_PAGE_SIZE)
    width, height = CUSTOM_PAGE_SIZE

    # Setup the styles for the PDF content
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle('header_style', parent=styles['Heading1'], fontSize=20, textColor=colors.darkblue)
    normal_style = ParagraphStyle('normal_style', parent=styles['BodyText'], fontSize=12, leading=15)
    bullet_style = ParagraphStyle('bullet_style', parent=styles['BodyText'], fontSize=12, leftIndent=20, bulletIndent=10)

    y = height - 50
    frame = Frame(40, 40, width - 80, height - 100, showBoundary=0)

    elements = []

    # Add Title and other fields from json_data
    if 'Title' in json_data:
        elements.append(Paragraph(f"<b>Title:</b> {json_data['Title']}", header_style))
    if 'Problem Statement' in json_data:
        elements.append(Paragraph(f"<b>Problem Statement:</b> {json_data['Problem Statement']}", normal_style))
    if 'Description' in json_data:
        elements.append(Paragraph(f"<b>Description:</b> {json_data['Description']}", normal_style))
    if 'Challenge / Use Case' in json_data:
        elements.append(Paragraph(f"<b>Challenge / Use Case:</b> {json_data['Challenge / Use Case']}", normal_style))
    if 'Deliverables' in json_data:
        elements.append(Paragraph(f"<b>Deliverables:</b> {json_data['Deliverables']}", normal_style))

    if 'KPIs' in json_data and isinstance(json_data['KPIs'], list):
        elements.append(Paragraph("<b>KPIs:</b>", normal_style))
        for kpi in json_data['KPIs']:
            elements.append(Paragraph(f"• {kpi}", bullet_style))

    if 'Prerequisites' in json_data and isinstance(json_data['Prerequisites'], list):
        elements.append(Paragraph("<b>Prerequisites:</b>", normal_style))
        for prereq in json_data['Prerequisites']:
            elements.append(Paragraph(f"• {prereq}", bullet_style))

    if 'Infrastructure Requirements' in json_data:
        elements.append(Paragraph(f"<b>Infrastructure Requirements:</b> {json_data['Infrastructure Requirements']}", normal_style))
    if 'Tentative Tech Stack' in json_data:
        elements.append(Paragraph(f"<b>Tentative Tech Stack:</b> {json_data['Tentative Tech Stack']}", normal_style))

    if 'Milestones (6 months)' in json_data and isinstance(json_data['Milestones (6 months)'], dict):
        elements.append(Paragraph("<b>Milestones (6 months):</b>", normal_style))
        milestones = json_data['Milestones (6 months)']
        if 'M2' in milestones:
            elements.append(Paragraph(f"• M2: {milestones['M2']}", bullet_style))
        if 'M4' in milestones:
            elements.append(Paragraph(f"• M4: {milestones['M4']}", bullet_style))
        if 'M6' in milestones:
            elements.append(Paragraph(f"• M6: {milestones['M6']}", bullet_style))

    if 'Reference Work' in json_data and isinstance(json_data['Reference Work'], list):
        elements.append(Paragraph("<b>Reference Work:</b>", normal_style))
        for idx, ref in enumerate(json_data['Reference Work']):
            if isinstance(ref, dict) and 'Title' in ref and 'Link' in ref:
                link_paragraph = f'<a href="{ref["Link"]}">{ref["Title"]}</a>'
                elements.append(Paragraph(link_paragraph, bullet_style))

    frame.addFromList(elements, pdf)
    pdf.save()

    print(f"PDF generated: {filename}")


def create_ppt(output_filename, json_data):
    prs = Presentation()
    # Set slide dimensions to 16:9 (typical widescreen)
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    
    # --- Title Slide ---
    # Use a blank layout so we control every element
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)
    
    # Title Text Box (centered)
    title_left = Inches(1)
    title_top = Inches(1)
    title_width = prs.slide_width - Inches(2)
    title_height = Inches(1.5)
    title_box = slide.shapes.add_textbox(title_left, title_top, title_width, title_height)
    title_tf = title_box.text_frame
    title_paragraph = title_tf.paragraphs[0]
    title_paragraph.text = json_data.get("Title", "Untitled Project")
    title_paragraph.font.size = Pt(44)
    title_paragraph.font.bold = True
    title_paragraph.alignment = PP_ALIGN.CENTER

    # Subtitle / Problem Statement Text Box (below the title)
    subtitle_left = Inches(1)
    subtitle_top = Inches(2.7)
    subtitle_width = prs.slide_width - Inches(2)
    subtitle_height = Inches(1)
    subtitle_box = slide.shapes.add_textbox(subtitle_left, subtitle_top, subtitle_width, subtitle_height)
    subtitle_tf = subtitle_box.text_frame
    subtitle_paragraph = subtitle_tf.paragraphs[0]
    subtitle_paragraph.text = json_data.get("Problem Statement", "")
    subtitle_paragraph.font.size = Pt(28)
    subtitle_paragraph.alignment = PP_ALIGN.CENTER

    # --- Content Slide Function ---
    def add_content_slide(slide_title, content_lines):
        slide = prs.slides.add_slide(blank_slide_layout)
        # Title area for the content slide
        t_left = Inches(0.5)
        t_top = Inches(0.5)
        t_width = prs.slide_width - Inches(1)
        t_height = Inches(1)
        title_box = slide.shapes.add_textbox(t_left, t_top, t_width, t_height)
        title_tf = title_box.text_frame
        title_par = title_tf.paragraphs[0]
        title_par.text = slide_title
        title_par.font.size = Pt(32)
        title_par.font.bold = True

        # Content Text Box (for bullet points or paragraphs)
        c_left = Inches(0.5)
        c_top = Inches(1.5)
        c_width = prs.slide_width - Inches(1)
        c_height = prs.slide_height - Inches(2)
        content_box = slide.shapes.add_textbox(c_left, c_top, c_width, c_height)
        content_tf = content_box.text_frame
        content_tf.word_wrap = True

        # For each content line, create a bullet
        for line in content_lines:
            p = content_tf.add_paragraph()
            p.text = line
            p.font.size = Pt(24)
            p.level = 0

    # --- Generate Slides from JSON ---
    # One-line text fields: show as a single bullet (or paragraph)
    for key in ["Description", "Challenge / Use Case", "Deliverables", 
                "Infrastructure Requirements", "Tentative Tech Stack"]:
        if key in json_data:
            add_content_slide(key, [json_data[key]])

    # List-based fields (e.g. KPIs, Prerequisites)
    for key in ["KPIs", "Prerequisites"]:
        if key in json_data and isinstance(json_data[key], list):
            add_content_slide(key, json_data[key])

    # Milestones: Key-value pairs; combine each into a single line
    if "Milestones (6 months)" in json_data:
        milestones = json_data["Milestones (6 months)"]
        milestone_lines = [f"{k}: {v}" for k, v in milestones.items()]
        add_content_slide("Milestones (6 months)", milestone_lines)

    # Reference Work: Each reference as a line with title and link
    if "Reference Work" in json_data:
        refs = json_data["Reference Work"]
        links = [f"{ref['Title']} - {ref['Link']}" for ref in refs if isinstance(ref, dict)]
        add_content_slide("Reference Work", links)

    prs.save(output_filename)
    print(f"Saved presentation to {output_filename}")

# --- Example Usage ---

sample_json = {
        "Title": "Federated Learning for Personalized Healthcare in Rural India",
        "Problem Statement": "Develop a federated learning framework leveraging edge devices to train a personalized disease prediction model for rural Indian patients, addressing data privacy and limited internet connectivity.",
        "Description": "Healthcare access in rural India is limited by data silos and privacy concerns. This project aims to create a distributed AI model using federated learning, enabling healthcare providers to learn from patient data without direct data sharing, improving diagnostic accuracy and treatment planning.",
        "Challenge / Use Case": "Limited access to specialized healthcare and challenges in data sharing due to privacy regulations in rural Indian clinics.",
        "Deliverables": "A federated learning framework, a trained disease prediction model, a secure data aggregation mechanism, and a detailed performance report.",
        "KPIs": [
            "Accuracy ≥ 10% improvement over centralized model",
            "Communication Rounds ≤ 15",
            "Data Privacy: Differential Privacy budget (ε) ≤ 1.0",
            "Model Convergence: Achieve convergence within 30 epochs"
        ],
        "Prerequisites": [
            "Understanding of federated learning principles",
            "Familiarity with machine learning algorithms (e.g., logistic regression, SVM)",
            "Knowledge of privacy-preserving techniques (e.g., differential privacy)",
            "Experience with Python and TensorFlow/PyTorch",
            "Basic networking concepts",
            "Familiarity with Indian healthcare data formats (if available)"
        ],
        "Infrastructure Requirements": "Cloud credits (Google Cloud/AWS) for model training and edge device simulation; 2-4 GPUs recommended for accelerated training.",
        "Tentative Tech Stack": "Python, TensorFlow/PyTorch, Federated Learning Framework (Flower/FedML), Differential Privacy library (Opacus), Scikit-learn",
        "Milestones (6 months)": {
            "M2": "Implement basic federated learning setup with synthetic data",
            "M4": "Integrate with a simulated rural healthcare dataset and implement privacy budget",
            "M6": "Develop and deploy the federated learning model with a final performance report"
        },
        "Reference Work": [
            {
                "Title": "Case Studies in Federated Learning for Healthcare",
                "Link": "https://www.igi-global.com/viewtitle.aspx?titleid=346276"
            },
            {
                "Title": "Federated Learning: Advancing Healthcare through Collaborative Artificial Intelligence",
                "Link": "https://journals.lww.com/ijcn/fulltext/2024/01000/federated_learning__advancing_healthcare_through.15.aspx"
            },
            {
                "Title": "Federated Learning for Diabetic Retinopathy Diagnosis: Enhancing Accuracy and Generalizability in Under-Resourced Regions",
                "Link": "https://arxiv.org/abs/2411.00869"
            },
            {
                "Title": "Federated Learning: The much-needed intervention in Healthcare Informatics.",
                "Link": "https://search.ebscohost.com/login.aspx?direct=true&profile=ehost&scope=site&authtype=crawler&jrnl=26767104&AN=184661859"
            },
            {
                "Title": "Federated learning framework for consumer IoMT-edge resource recommendation under telemedicine services",
                "Link": "https://ieeexplore.ieee.org/abstract/document/10793078/"
            },
            {
                "Title": "Federated learning for the internet-of-medical-things: A survey",
                "Link": "https://www.mdpi.com/2227-7390/11/1/151"
            }
        ]
    }

create_ppt("GeneratedPresentation.pptx", sample_json)
