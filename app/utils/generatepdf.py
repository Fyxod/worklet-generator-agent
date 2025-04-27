from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
from app.utils.reference_functions.reference_sort import inplace_sort, scholar_sort,index_sort
from app.socket import sio
# from reference_functions.reference_sort import Inplace_sort 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "./resources/generated_worklets")
print(UPLOAD_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)
pdf_path = os.path.join(PROJECT_ROOT, "resources/generated_worklets/")
CUSTOM_PAGE_SIZE = (700,900)  # Width x Height in points (1 point = 1/72 inch)


def pre_processing(json, index):
    model ="llama3.3:latest"
    # for idx, ref in enumerate(json["Reference Work"]):
    #     ref["index"] = idx  # Add new key "index" to each dictionary
    print("\n")
    print("inside Inplace_sort")
    print("\n")
    sio.emit("progress", {"message": "Comparing references and selecting the best suited references"})
    json=scholar_sort(json,model, index)
    return json

def generatePdf_unsafe(json,model):
    print("\n")
    print("----"*25+"Inside generate pdf"+"----"*25)
    print("\n")
    json = pre_processing(json)
    filename = os.path.join(pdf_path, f"{json['Title']}.pdf")
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

    # reference_limit = 15
    elements.append(Paragraph("<b>Reference Work:</b>", normal_style))
    for idx, ref in enumerate(json['Reference Work']):
      # if idx >= reference_limit:
      #     break
      print(idx," -------------------------------------------------- ",ref)
      link_paragraph = f'<a href="{ref["Link"]}">{ref["Title"]}</a>'
      elements.append(Paragraph(link_paragraph, bullet_style))

    frame.addFromList(elements, pdf)
    pdf.save()
    print("\n")
    print(f"PDF generated: {filename}")
    print("\n")
    print("\n")

def generatePdf(json, model, index):
    print("\n")
    print("----"*25+"Inside generate pdf"+"----"*25)
    print("\n")
    pre_processing(json, index)
    filename = os.path.join(pdf_path, f"{json['Title']}.pdf")
    pdf = canvas.Canvas(filename, pagesize=CUSTOM_PAGE_SIZE)
    width, height = CUSTOM_PAGE_SIZE

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle('header_style', parent=styles['Heading1'], fontSize=20, textColor=colors.darkblue)
    normal_style = ParagraphStyle('normal_style', parent=styles['BodyText'], fontSize=12, leading=15)
    bullet_style = ParagraphStyle('bullet_style', parent=styles['BodyText'], fontSize=12, leftIndent=20, bulletIndent=10)

    y = height - 50
    frame = Frame(40, 40, width - 80, height - 100, showBoundary=0)

    elements = []

    if 'Title' in json:
        elements.append(Paragraph(f"<b>Title:</b> {json['Title']}", header_style))
    if 'Problem Statement' in json:
        elements.append(Paragraph(f"<b>Problem Statement:</b> {json['Problem Statement']}", normal_style))
    if 'Description' in json:
        elements.append(Paragraph(f"<b>Description:</b> {json['Description']}", normal_style))
    if 'Challenge / Use Case' in json:
        elements.append(Paragraph(f"<b>Challenge / Use Case:</b> {json['Challenge / Use Case']}", normal_style))
    if 'Deliverables' in json:
        elements.append(Paragraph(f"<b>Deliverables:</b> {json['Deliverables']}", normal_style))

    if 'KPIs' in json and isinstance(json['KPIs'], list):
        elements.append(Paragraph("<b>KPIs:</b>", normal_style))
        for kpi in json['KPIs']:
            elements.append(Paragraph(f"• {kpi}", bullet_style))

    if 'Prerequisites' in json and isinstance(json['Prerequisites'], list):
        elements.append(Paragraph("<b>Prerequisites:</b>", normal_style))
        for prereq in json['Prerequisites']:
            elements.append(Paragraph(f"• {prereq}", bullet_style))

    if 'Infrastructure Requirements' in json:
        elements.append(Paragraph(f"<b>Infrastructure Requirements:</b> {json['Infrastructure Requirements']}", normal_style))
    if 'Tentative Tech Stack' in json:
        elements.append(Paragraph(f"<b>Tentative Tech Stack:</b> {json['Tentative Tech Stack']}", normal_style))

    if 'Milestones (6 months)' in json and isinstance(json['Milestones (6 months)'], dict):
        elements.append(Paragraph("<b>Milestones (6 months):</b>", normal_style))
        milestones = json['Milestones (6 months)']
        if 'M2' in milestones:
            elements.append(Paragraph(f"• M1: {milestones['M2']}", bullet_style))
        if 'M4' in milestones:
            elements.append(Paragraph(f"• M2: {milestones['M4']}", bullet_style))
        if 'M6' in milestones:
            elements.append(Paragraph(f"• M3: {milestones['M6']}", bullet_style))

    if 'Reference Work' in json and isinstance(json['Reference Work'], list):
        elements.append(Paragraph("<b>Reference Work:</b>", normal_style))
        for idx, ref in enumerate(json['Reference Work']):
            if isinstance(ref, dict) and 'Title' in ref and 'Link' in ref:
                print(idx, " -------------------------------------------------- ", ref)
                link_paragraph = f'<a href="{ref["Link"]}">{ref["Title"]}</a>'
                elements.append(Paragraph(link_paragraph, bullet_style))

    frame.addFromList(elements, pdf)
    pdf.save()
    print("\n")
    print(f"PDF generated: {filename}")
    print("\n")
    print("\n")

JSON={
        "Title": "Personalized Product Recommendation using Generative AI and Classical Machine Learning",
        "Problem Statement": "Develop a personalized product recommendation system that leverages generative AI and classical machine learning to suggest relevant products based on user preferences.",
        "Description": "Utilize generative models, such as GANs or transformers, along with collaborative filtering algorithms to develop a system capable of generating personalized product recommendations for users.",
        "Challenge / Use Case": "Enhance e-commerce platforms by providing users with relevant and engaging product suggestions, increasing conversion rates and customer satisfaction.",
        "Deliverables": [
            "Trained generative AI model",
            "Integration with e-commerce platforms"
        ],
        "KPIs": [
            "Recommendation accuracy",
            "User engagement metrics"
        ],
        "Prerequisites": [
            "Familiarity with deep learning frameworks such as TensorFlow or PyTorch",
            "Knowledge of classical machine learning algorithms and collaborative filtering"
        ],
        "Infrastructure Requirements": "Moderate computational resources, including a dedicated server for training the model.",
        "Milestones (6 months)": {
            "M2": "Develop a baseline generative AI model using GANs or transformers",
            "M4": "Integrate the generative AI model with classical machine learning algorithms and collaborative filtering",
            "M6": "Conduct user testing and refine the final system, including error handling and feedback mechanisms"
        },
        "Reference Work": [
            {
                "title": "Hyperpersonalisation-and-X-Sell-for-Indian-Financial-Sector",
                "description": "A machine learning and Generative AI solution for personalized financial recommendations. Features include dynamic pricing (loan predictions), product recommendations, and actionable insights using KingNish/Qwen2.5 LLM. Integrated with a Flask app for real-time deployment on AWS.",
                "link": "https://github.com/Gaurang-Sonkavde/Hyperpersonalisation-and-X-Sell-for-Indian-Financial-Sector",
                "tag": "github"
            },
            {
                "title": "[PDF][PDF] Revolutionizing Product Recommendations with Generative AI: Context-Aware Personalization at Scale",
                "link": "https://www.researchgate.net/profile/Sai-Kiran-Reddy-Malikireddy-3/publication/387741873_Revolutionizing_Product_Recommendations_with_Generative_AI_Context-Aware_Personalization_at_Scale/links/677ad4fe117f340ec3f60fd6/Revolutionizing-Product-Recommendations-with-Generative-AI-Context-Aware-Personalization-at-Scale.pdf",
                "description": "\u2026 By reimagining product discovery as a generative process, \u2026 hyper-personalized, interactive, \nand engaging recommendation \u2026 Reinforcement learning integrated with generative models \u2026",
                "tag": "scholar"
            },
            {
                "title": "AI-Driven Personalization: Generative Models in E-Commerce",
                "link": "https://hal.science/hal-04925157/",
                "description": "\u2026 [11] The discussion has covered the topic of deep learning-based e-\u2026 a recommendation \nsystem that employs various deep learning and machine learning algorithms to suggest products \u2026",
                "tag": "scholar"
            },
            {
                "title": "[PDF][PDF] USING GENERATIVE MODELS FOR PERSONALIZED RECOMMENDATIONS IN E-COMMERCE",
                "link": "https://www.researchgate.net/profile/Pradeep-Sharma-64/publication/387098741_USING_GENERATIVE_MODELS_FOR_PERSONALIZED_RECOMMENDATIONS_IN_E-COMMERCE/links/67608714e9b25e24af5656dd/USING-GENERATIVE-MODELS-FOR-PERSONALIZED-RECOMMENDATIONS-IN-E-COMMERCE.pdf",
                "description": "\u2026 data and algorithms to provide customized product and service suggestions based on user \n\u2026 of generating personalized recommendations. Deep learning algorithms called generative \u2026",
                "tag": "scholar"
            },
            {
                "title": "Analysis of recommender system using generative artificial intelligence: A systematic literature review",
                "link": "https://ieeexplore.ieee.org/abstract/document/10565860/",
                "description": "\u2026 , videos, audios, goods, and services to their customers/users or to personalize experiences \nfor their \u2026 explores the use of deep learning and generative adversarial networks (GANs) in \u2026",
                "tag": "scholar"
            },
            {
                "title": "Generative AI Recommender System in E-Commerce.",
                "link": "https://search.ebscohost.com/login.aspx?direct=true&profile=ehost&scope=site&authtype=crawler&jrnl=20885334&AN=182563287&h=6%2BAI5or%2FlDPWQKOwm1do76wUvjdHf2tXJbPCIn9S%2BSffNkz6cMQEkQsbnW2KVxBjWyR4lIC43B7rWnxc2jvPcA%3D%3D&crl=c",
                "description": "\u2026 customized product recommendations. One creative way to get beyond the constraints of \ne-commerce services is using recommendation \u2026 of robotics, AI, and machine learning. Then, the \u2026",
                "tag": "scholar"
            },
            {
                "title": "[HTML][HTML] Harnessing generative AI for personalized E-commerce product descriptions: A framework and practical insights",
                "link": "https://www.sciencedirect.com/science/article/pii/S0920548925000418",
                "description": "\u2026 of artificial intelligence (AI) and machine learning is \u2026 of large language models to personalize \nuser interactions throughout the \u2026 of generative AI to create customized e-commerce product \u2026",
                "tag": "scholar"
            },
            {
                "title": "Personalized Marketing and Recommendation Systems",
                "link": "https://www.taylorfrancis.com/chapters/edit/10.1201/9781003472544-7/personalized-marketing-recommendation-systems-mani-teja-chowdary-maniteja-vallepu-naga-sai-purushotham-neelam-kumari",
                "description": "\u2026 deep learning techniques may be opaque. How many things and users must you man\u2011 age? \nDeep learning \u2026 Personalized filters that sug\u2011 gest products we may enjoy based on our prior \u2026",
                "tag": "scholar"
            },
            {
                "title": "Generative AI for Revolutionizing Personal Style",
                "link": "https://ieeexplore.ieee.org/abstract/document/10932201/",
                "description": "\u2026 Recommendation engines play a huge role in shopping customized product by suggesting \n\u2026 deep learning methodologies and the advances achieved by GANs in intelligent fashion \u2026",
                "tag": "scholar"
            },
            {
                "title": "[PDF][PDF] Harnessing the power of generative artificial intelligence for dynamic content personalization in customer relationship management systems: A data-driven\u00a0\u2026",
                "link": "https://www.researchgate.net/profile/Sai-Ganesh-Reddy-Bojja-2/publication/389689415_Harnessing_the_Power_of_Generative_Artificial_Intelligence_for_Dynamic_Content_Personalization_in_Customer_Relationship_Management_Systems_A_Data-Driven_Framework_for_Optimizing_Customer_Engagement_an/links/67cdb161bab3d32d84405238/Harnessing-the-Power-of-Generative-Artificial-Intelligence-for-Dynamic-Content-Personalization-in-Customer-Relationship-Management-Systems-A-Data-Driven-Framework-for-Optimizing-Customer-Engagement-an.pdf",
                "description": "\u2026 Generative AI encompasses a range of machine learning \u2026 of generative AI for crafting \npersonalized product descriptions, \u2026 after clicking on a product recommendation or the number of \u2026",
                "tag": "scholar"
            },
            {
                "title": "Practical Recommendation of Using Generative AI in Business",
                "link": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4851637",
                "description": "\u2026 economic benefits, balancing customization and control with \u2026 applications of generative AI \nin software product management, \u2026 By leveraging advanced machine learning models, GenAI \u2026",
                "tag": "scholar"
            }
        ]
    }
# generatePdf(JSON)
# pre_processing(