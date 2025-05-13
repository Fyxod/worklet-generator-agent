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

# Blocking PPT creation function
def create_ppt(filename, json_data):
    # print("insideppt")
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    bullet_slide_layout = prs.slide_layouts[1]

    def add_title_slide(title, subtitle=""):
        slide = prs.slides.add_slide(title_slide_layout)
        slide.shapes.title.text = title
        slide.placeholders[1].text = subtitle

    def add_bullet_slide(title, bullets):
        slide = prs.slides.add_slide(bullet_slide_layout)
        shapes = slide.shapes
        shapes.title.text = title
        body_shape = shapes.placeholders[1]
        tf = body_shape.text_frame
        tf.clear()
        for bullet in bullets:
            p = tf.add_paragraph()
            p.text = bullet
            p.level = 0

    add_title_slide(json_data.get("Title", "Worklet"), json_data.get("Problem Statement", ""))

    # Normal text fields
    for key in ["Description", "Challenge / Use Case", "Deliverables", "Infrastructure Requirements", "Tentative Tech Stack"]:
        if key in json_data:
            add_bullet_slide(key, [json_data[key]])

    # List fields
    for key in ["KPIs", "Prerequisites"]:
        if key in json_data and isinstance(json_data[key], list):
            add_bullet_slide(key, json_data[key])

    # Milestones
    if "Milestones (6 months)" in json_data:
        milestones = json_data["Milestones (6 months)"]
        bullets = [f"{k}: {v}" for k, v in milestones.items()]
        add_bullet_slide("Milestones (6 months)", bullets)

    # Reference Work
    if "Reference Work" in json_data:
        refs = json_data["Reference Work"]
        links = [f"{ref['Title']} - {ref['Link']}" for ref in refs if isinstance(ref, dict)]
        add_bullet_slide("Reference Work", links)

    prs.save(filename)
    print(filename)

