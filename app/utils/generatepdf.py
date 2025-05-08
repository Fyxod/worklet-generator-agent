import asyncio
import os
import re

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph

from app.utils.reference_functions.reference_sort import index_sort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "./resources/generated_worklets")
print(UPLOAD_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)
pdf_path = os.path.join(PROJECT_ROOT, "resources/generated_worklets/")
CUSTOM_PAGE_SIZE = (750,900)  # Width x Height in points (1 point = 1/72 inch)

async def pre_processing(json_data, index, model="gemma3:27b"):
    print("\n")
    json_data = await index_sort(json_data, model, index)
    return json_data

def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '_', filename)

# Function to handle the actual blocking PDF generation using ReportLab
def create_pdf(filename, json_data):
    """Blocking function for creating PDF with ReportLab."""
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

async def generatePdf(json, model, index):
    print("\n")
    print("----" * 25 + "Inside generate pdf" + "----" * 25)
    print("\n")

    json_data = await pre_processing(json, index, model)
    safe_title = sanitize_filename(json['Title'])
    filename = os.path.join(pdf_path, f"{safe_title}.pdf")

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, create_pdf, filename, json_data)

    print("\n")
    print(f"PDF generated: {filename}")
    print("\n")


json={
        "Title": "Optimized Integer Sequence Generation using Parallel Processing",
        "Problem Problem": "Design and implement a novel algorithm to create large sets of ordered number sets. Focus on accelerating time-to-output for complex formulas of numbers such as fibonacci, triangular, prime and quadratic numbers. ",
        "Description": "Number sequence generation is useful in creating large sets of numbers used in algorithms. Computation of this can be very slow, and parallelization offers a considerable efficiency increase. ",
        "Challenge / Use Case": "Use parallel computing to reduce the time it takes to compute sequences of numbers.",
        "Deliverables": "A Multi-threading C++ implementation of the algorithms, and a comparison of performance to sequential versions",
        "KPIs": [
            "Time to generate 1 million numbers: < 5 seconds",
            "CPU utilization: >=80%",
            "Memory footprint: <2GB",
            "Correctness: All generated values match reference implementation.",
        ],
        "Prerequisites": [
            "C++",
            "Multi-thread programming",
            "Number theory",
            "Algorithmic optimization",
            "Parallel computing concepts",
        ],
        "Infrastructure Requirements": "8 cores, 16 GB RAM, SSD storage, a modern compiler (g++), and a good code editor",
        "Tentative Tech Stack": "C++20, g++, OpenMP, parallel STL",
        "Milestones (6 months)": {
            "M2": "Implement and test basic prime number generation",
            "M4": "Integrate other algorithms using to achieve significant speedups.",
            "M6": "Create a comprehensive performance benchmark",
        },
    }
create_pdf("test.pdf",json)