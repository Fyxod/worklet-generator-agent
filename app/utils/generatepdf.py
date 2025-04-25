from reportlab.lib.pagesizes import A3
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "./resources/generated_worklets")
print(UPLOAD_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)
pdf_path = os.path.join(PROJECT_ROOT, "resources/generated_worklets/")
CUSTOM_PAGE_SIZE = (700, 800)  # Width x Height in points (1 point = 1/72 inch)
def generatePdf(json,):
    filename = os.path.join(pdf_path, f"{json['Title'].replace(' ', '_')}.pdf")
    pdf = canvas.Canvas(filename, pagesize=CUSTOM_PAGE_SIZE)
    width, height = CUSTOM_PAGE_SIZE

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle('header_style', parent=styles['Heading1'], fontSize=20, textColor=colors.darkblue)
    normal_style = ParagraphStyle('normal_style', parent=styles['BodyText'], fontSize=12, leading=15)
    bullet_style = ParagraphStyle('bullet_style', parent=styles['BodyText'], fontSize=12, leftIndent=20, bulletIndent=10)

    y = height - 50
    frame = Frame(40, 40, width - 80, height - 100, showBoundary=0)

    elements = []
    elements.append(Paragraph(f"<b>Title:</b> {json['Title']}", header_style))
    elements.append(Paragraph(f"<b>Problem Statement:</b> {json['Problem Statement']}", normal_style))
    elements.append(Paragraph(f"<b>Description:</b> {json['Description']}", normal_style))
    elements.append(Paragraph(f"<b>Challenge / Use Case:</b> {json['Challenge / Use Case']}", normal_style))
    elements.append(Paragraph(f"<b>Deliverables:</b> {json['Deliverables']}", normal_style))

  
    elements.append(Paragraph("<b>KPIs:</b>", normal_style))
    for kpi in json['KPIs']:
        elements.append(Paragraph(f"• {kpi}", bullet_style))

    
    elements.append(Paragraph("<b>Prerequisites:</b>", normal_style))
    for prereq in json['Prerequisites']:
        elements.append(Paragraph(f"• {prereq}", bullet_style))

    elements.append(Paragraph(f"<b>Infrastructure Requirements:</b> {json['Infrastructure Requirements']}", normal_style))
    elements.append(Paragraph(f"<b>Tentative Tech Stack:</b> {json['Tentative Tech Stack']}", normal_style))

    elements.append(Paragraph("<b>Milestones (6 months):</b>", normal_style))
    elements.append(Paragraph(f"• M1: {json['Milestones (6 months)']["M2"]}", bullet_style))
    elements.append(Paragraph(f"• M2: {json['Milestones (6 months)']["M4"]}", bullet_style))
    elements.append(Paragraph(f"• M3: {json['Milestones (6 months)']["M6"]}", bullet_style))

    frame.addFromList(elements, pdf)
    pdf.save()
    print(f"PDF generated: {filename}")

JSON={
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
        "TensorFlow Lite or CoreML",
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
# generatePdf(JSON)
