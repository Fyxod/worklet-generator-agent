from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.colors import lightgrey, blueviolet, HexColor
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate, Frame
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
import json


# from reportlab.lib.colors import HexColor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "./resources/generated_worklets")
print(UPLOAD_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Define the page size in points (1 inch = 72 points)
page_width = 20 * 72  # 1440 points
page_height = 11.25 * 72  # 810 points

# used in initial desining of pdf
def draw_ruler(pdf, width, height):
    """Draws a ruler along the top and left edges of the page."""
    pdf.setStrokeColorRGB(0, 0, 0)  # Black color
    pdf.setFont("Helvetica", 10)

    # X-Axis (Horizontal Ruler, bottom edge)
    for i in range(0, int(width), 72):  # 1 inch = 72 points
        pdf.line(i, 0, i, 10)  # Small tick marks on the bottom
        pdf.drawString(i + 2, 12, str(i))  # Labels above tick marks

    # Y-Axis (Vertical Ruler, left edge)
    for i in range(0, int(height), 72):
        pdf.line(0, i, 10, i)  # Small tick marks on the left
        pdf.drawString(15, i - 3, str(i))  # Labels to the right of tick marks

pdf_path = os.path.join(PROJECT_ROOT, "resources/generated_worklets/")


def generatePdfold(json):

    print(json)
    pdf_filename = pdf_path+json["Title"]+".pdf"
    pdf = canvas.Canvas(pdf_filename, pagesize=(page_width, page_height))
    # draw_ruler(pdf, page_width,page_height)
    pdf.setTitle(pdf_filename)
    pdf.setTitle(pdf_filename)

# samsung logo
    # pdf.drawImage(f"{PROJECT_ROOT}/resources/Samsung_Orig_Wordmark_BLUE_RGB.png", 1190,720, width=250, height=90, mask='auto')
    
# rectangles

    # small blue
    pdf.setFillColorRGB(20/255, 60/255, 140/255)
    pdf.rect(0, 730, 17, 792-730,  fill=1, stroke=0)

    # small grey
    pdf.setFillColor(lightgrey)
    pdf.rect(30, 730, 10, 792-730,  fill=1, stroke=0)

    # big grey
    pdf.setFillColor(lightgrey)
    pdf.rect(0,  0, 720, 720, fill=1, stroke=0)    # remove 50 and do zero

    # Complexity
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Times-Bold", 20)
    a = 190
    y=-20
    pdf.drawString(767 + 6+a, 85+y, "2")
    pdf.drawString(794 + 6+a, 85+y, "3")
    pdf.drawString(821 + 6+a, 85+y, "4")
    pdf.drawString(848 + 6+a, 85+y, "5")
    pdf.drawString(740 + 6+a, 85+y, "1")
    pdf.drawString(875 + 6+a, 85+y, "6")
    pdf.drawString(902 + 6+a, 85+y, "7")
    pdf.drawString(929 + 6+a, 85+y, "8")
    pdf.drawString(956 + 6+a, 85+y, "9")
    pdf.drawString(978 + 6+a, 85+y, "10")

    pdf.setFillColor(HexColor("#5ab43b"))
    pdf.rect(740+a, 72+y, 20, 10, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#6fcb3b"))
    pdf.rect(767+a, 72+y, 20, 10, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#93e041"))
    pdf.rect(794+a, 72+y, 20, 10, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#cad442"))
    pdf.rect(821+a, 72+y, 20, 10, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#fbc430"))
    pdf.rect(848+a, 72+y, 20, 10, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#fcb120"))
    pdf.rect(875+a, 72+y, 20, 10, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#ff932c"))
    pdf.rect(902+a, 72+y, 20, 10, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#f47c1d"))
    pdf.rect(929+a, 72+y, 20, 10, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#e64817"))
    pdf.rect(956+a, 72+y, 20, 10, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#da2927"))
    pdf.rect(983+a, 72+y, 20, 10, fill=1, stroke=0)

    x=26
    arrX = [928, 928+x, 929+2*x, 930+3*x, 932+4*x, 934+5*x, 934+6*x, 936+7*x, 938+8*x ,938+9*x]
    arrowYPosition = 30

    # arrow - png
    pdf.drawImage(f"{PROJECT_ROOT}/resources/arrow.png", arrX[json["Difficulty"]-1], arrowYPosition, width=25,height=25, mask='auto')
    # pdf.drawImage(f"{PROJECT_ROOT}/resources/arrow.png", arrX[9], arrowYPosition, width=25,height=25, mask='auto')
# title
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Times-Bold", 48)
    pdf.drawString(52, 753, json["Title"].capitalize())

    #problem statement
    pdf.setFillColorRGB(20/255, 60/255, 140/255)
    pdf.setFont("Times-Bold", 40)
    pdf.drawString(220, 670, "Problem Statement")

    # expecctation
    pdf.drawString(1010, 670, "Expectation")

    #Goal
    pdf.drawString(1010, 400, "Goal")

    #Worklet
    pdf.drawString(220, 400, "Worklet Details")

    # prereq
    pdf.setFont("Times-Bold", 20)
    pdf.drawString(50, 150, "Training/Prerequisite")
    pdf.drawString(770, 60, "Complexity")
    pdf.drawString(770, 150, "Reference Work")
# normal black headings
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(114, 200, "Duration")
    pdf.drawString(350, 200, "Members")
    pdf.drawString(350, 180, "Count  ")
    pdf.drawString(572, 200, "Mentors")

    pdf.drawImage(f"{PROJECT_ROOT}/resources/Samsung_Orig_Wordmark_BLUE_RGB.png", 1190,720,width=250, height=90, mask='auto')
# Paragaphs


    problem_style = ParagraphStyle(
        name="ProblemStyle",
        fontName="Times-Roman",
        fontSize=28,
        textColor=colors.black,
        leading=28,# Line spacing
        alignment=0    # Left-aligned
    )
    ref_style = ParagraphStyle(
        fontName="Times-Roman",
        fontSize=16,
        textColor=colors.blue,  # Set text color to blue
        leading=18,  # Line spacing
        alignment=0,  # Left-aligned
        underline=True,
        name="refStyle"
    )
    training_style = ParagraphStyle(
        name="refStyle",
        fontName="Times-Roman",
        fontSize=19,
        textColor=colors.black,
        leading=21,# Line spacing
        alignment=0    # Left-aligned
    )
    problem_paragraph = Paragraph(json["Problem Statement"], problem_style)
    goal_paragraph = Paragraph(json["Goal"], problem_style)
    Expectation_paragraph = Paragraph(json["Expectations"], problem_style)
    Training_Prerequisite_paragraph = Paragraph(json["Training/Prerequisite"], training_style)
    # "Reference Work": [
    #     {
    #         "title": "Matrix Expression of Bayesian Game",
    #         "link": "http://arxiv.org/pdf/2106.12161v1"
    #     },
    json["Reference Work"]=filter_references(json["Reference Work"])
    if len(json["Reference Work"]) == 1:
        ref_text = f'''
        <ul>
            <li><u><a href="{json["Reference Work"][0]["link"]}">{json["Reference Work"][0]["title"]}</a></u></li>
        </ul>
        '''
    else:
        ref_text = f'''
        <ul>
            <li><u><a href="{json["Reference Work"][0]["link"]}">{json["Reference Work"][0]["title"]}</a></u></li><br/>
            <li><u><a href="{json["Reference Work"][1]["link"]}">{json["Reference Work"][1]["title"]}</a></u></li>
        </ul>
        '''

    ref_paragraph = Paragraph(ref_text, ref_style)
    # frames
    frame_problem =                       Frame(50, 432, 620, 216, showBoundary=0)
    frame_expectations =                  Frame(770, 432, 620, 216, showBoundary=0)
    frame_goal =                          Frame(770, 180, 620, 216, showBoundary=0)
    frame_Prerequisite_paragraph=         Frame(50, 0, 620, 140, showBoundary=0)
    frame_ref=         Frame(770, 80, 620, 60, showBoundary=0)

    frame_problem.addFromList([problem_paragraph], pdf)
    frame_expectations.addFromList([Expectation_paragraph], pdf)
    frame_goal.addFromList([goal_paragraph], pdf)
    frame_Prerequisite_paragraph.addFromList([Training_Prerequisite_paragraph], pdf)
    frame_ref.addFromList([ref_paragraph], pdf)

    # Get style for paragraph
    # styles = getSampleStyleSheet()
    # ref_style = styles["Normal"]

    # # Generate reference string with embedded links
    # ref_text = "<b>References:</b><br/>"
    # for idx, ref in enumerate(json["Reference Work"], start=1):
    #     ref_text += f'{idx}. <a href="{ref["link"]}">{ref["title"]}</a><br/>'
    #
    # # Create paragraph
    # ref_paragraph = Paragraph(ref_text, ref_style)
    #
    # # Define the frame (adjust position and size as needed)
    # frame_ref = Frame(770, 80, 620, 100, showBoundary=0)
    #
    # # Add to PDF
    # frame_ref.addFromList([ref_paragraph], pdf)
    pdf.save()
    print(f"PDF generated: {pdf_filename}")
def filter_references(ref):
    for r in ref:
        r["title"]=r["title"].replace("\n"," ")
    ref = sorted(ref, key=lambda r: len(r["title"]))
    return ref

def generatePdf(json):
    filename= pdf_path+json["Title"]+".pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    title_style = styles['Heading1']
    section_title_style = styles['Heading2']
    normal_style = styles['BodyText']
    bullet_style = ParagraphStyle(name='Bullet', parent=styles['BodyText'], leftIndent=20, bulletIndent=10)

    # Title
    story.append(Paragraph(data['Title'], title_style))
    story.append(Spacer(1, 12))

    # Sections
    sections = ['Problem Statement', 'Description', 'Challenge / Use Case', 'Deliverables', 'Infrastructure Requirements', 'Tentative Tech Stack']
    for key in sections:
        story.append(Paragraph(key, section_title_style))
        story.append(Paragraph(data[key], normal_style))
        story.append(Spacer(1, 10))

    # KPIs
    story.append(Paragraph('Key Performance Indicators (KPIs)', section_title_style))
    kpi_items = [ListItem(Paragraph(f"- {kpi}", bullet_style)) for kpi in data['KPIs']]
    story.append(ListFlowable(kpi_items, bulletType='bullet'))
    story.append(Spacer(1, 10))

    # Prerequisites
    story.append(Paragraph('Prerequisites', section_title_style))
    prereq_items = [ListItem(Paragraph(f"- {item}", bullet_style)) for item in data['Prerequisites']]
    story.append(ListFlowable(prereq_items, bulletType='bullet'))
    story.append(Spacer(1, 10))

    # Milestones
    story.append(Paragraph('Milestones (6 months)', section_title_style))
    for milestone, desc in data['Milestones (6 months)'].items():
        story.append(Paragraph(f"<b>{milestone}</b>: {desc}", normal_style))
    story.append(Spacer(1, 12))

    # Build PDF
    doc.build(story)


json_string5={
      "Title": "Vision AI for Enhanced Object Recognition in AR Environments",
      "Problem Statement": "Design and implement a robust Vision AI system for real-time object recognition in augmented reality applications on Samsung devices, improving accuracy and reducing latency for seamless AR experiences.",
      "Description": "This project focuses on developing an efficient object recognition system for AR applications. By leveraging vision AI techniques, the system will identify and track objects in real-time, enabling users to interact with virtual elements overlaid on the real world. The key goal is to optimize the system for performance on Samsung devices to provide smooth and responsive AR experiences.",
      "Challenge / Use Case": "Addresses the need for accurate and fast object recognition in AR, enabling compelling user experiences for gaming, education, and e-commerce.",
      "Deliverables": "Android application demonstrating object recognition in AR, a fine-tuned object detection model, a performance analysis report, and integration with ARCore or similar AR framework.",
      "KPIs": [
        "Object recognition accuracy (mAP)",
        "Inference time (FPS)",
        "Memory usage of the model",
        "Power consumption on mobile devices"
      ],
      "Prerequisites": [
        "https://developers.google.com/ar/develop/java/object-recognition",
        "Computer vision fundamentals",
        "Object detection algorithms (e.g., YOLO, SSD)",
        "TensorFlow Lite or CoreML",app/utils/d.py
        "ARCore or ARKit",
        "COCO dataset or similar object detection datasets",
        "Blog on model quantization",
        "Paper on federated learning for object detection",
        "MOOC on deep learning for computer vision",
        "Android NDK (optional)"
      ],
      "Infrastructure Requirements": "Minimum: Laptop with GPU (NVIDIA or AMD), Android smartphone with ARCore support. Recommended: Cloud GPU for training.",
      "Tentative Tech Stack": "Python, TensorFlow/PyTorch, OpenCV, ARCore/ARKit, Android NDK (optional).",
      "Milestones (6 months)": {
        "M2": "Data collection and augmentation, baseline object detection model implementation.",
        "M4": "Model training and optimization for mobile devices, AR integration.",
        "M6": "Performance evaluation, user testing, and final report."
      }
    }
generatePdf(json_string5)