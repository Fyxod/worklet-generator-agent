json_string1= {
    "worklets": [
        {
            "Problem Statement": "Existing object detection models struggle with low-light conditions, resulting in poor accuracy and unreliable performance for security cameras or autonomous vehicle night vision.",
            "Goal": "Develop a robust object detection model that maintains high accuracy in low-light environments using image enhancement and data augmentation techniques.",
            "Expectations": "Participants will generate a dataset of low-light images, implement image enhancement algorithms, train an object detection model, and evaluate its performance against a baseline model in low-light scenarios.",
            "Training/Prerequisite": "Basic understanding of object detection algorithms (e.g., YOLO, SSD), image processing techniques, and experience with deep learning frameworks like TensorFlow or PyTorch.",
            "Difficulty": 7,
            "Reference Work": "“Deep Learning for Object Detection: A Comprehensive Review” - Zhao et al. (2019)"
        },
        {
            "Problem Statement": "Collecting and labeling large datasets for training machine learning models is time-consuming and expensive. Generating synthetic data can accelerate the process but often lacks realism.",
            "Goal": "Investigate and implement generative adversarial networks (GANs) to create realistic synthetic data for a specific task (e.g., image classification, object detection) to augment a smaller real-world dataset.",
            "Expectations": "Participants will choose a suitable GAN architecture, train it on a real-world dataset, generate synthetic data, combine it with the real data, and evaluate the performance of a model trained on the augmented dataset compared to a model trained solely on the real data.",
            "Training/Prerequisite": "Familiarity with GANs, deep learning concepts, and experience using deep learning frameworks.",
            "Difficulty": 6,
            "Reference Work": "“Generative Adversarial Nets” - Goodfellow et al. (2014)"
        },
        {
            "Problem Statement": "Edge devices have limited computational resources, making it challenging to deploy complex machine learning models for real-time applications.",
            "Goal": "Optimize an existing machine learning model (e.g., image classification, object detection) for deployment on an edge device by applying techniques such as model quantization, pruning, and knowledge distillation.",
            "Expectations": "Participants will select a pre-trained model, apply optimization techniques to reduce its size and computational complexity, deploy it on an edge device (e.g., Raspberry Pi), and evaluate its performance in terms of inference speed and accuracy.",
            "Training/Prerequisite": "Experience with machine learning model deployment, knowledge of model optimization techniques, and familiarity with edge computing platforms.",
            "Difficulty": 8,
            "Reference Work": "“Model Compression and Acceleration for Deep Learning: A Survey” - Cheng et al. (2017)"
        },
        {
            "Problem Statement": "Data bias in training datasets can lead to unfair or discriminatory outcomes in machine learning models.",
            "Goal": "Identify and mitigate bias in a given dataset used for a classification task by employing techniques such as data re-sampling, feature selection, and adversarial debiasing.",
            "Expectations": "Participants will analyze a dataset for potential biases, implement bias mitigation techniques, train a classification model, and evaluate its performance across different demographic groups to assess fairness.",
            "Training/Prerequisite": "Understanding of data bias, fairness metrics, and machine learning classification algorithms.",
            "Difficulty": 7,
            "Reference Work": "“Fairness and Machine Learning: Limitations and Opportunities” - Hardt et al. (2016)"
        },
        {
            "Problem Statement": "Time series data often contains anomalies or outliers that can significantly impact the performance of predictive models. Identifying these anomalies is crucial for various applications.",
            "Goal": "Develop a robust anomaly detection system for time series data using a combination of statistical methods and machine learning techniques.",
            "Expectations": "Participants will explore different anomaly detection algorithms (e.g., ARIMA, LSTM autoencoders), implement them on a real-world time series dataset, and evaluate their performance in terms of precision, recall, and F1-score.",
            "Training/Prerequisite": "Knowledge of time series analysis, statistical modeling, and machine learning techniques. Familiarity with libraries such as Statsmodels and scikit-learn is helpful.",
            "Difficulty": 9,
            "Reference Work": "“Anomaly Detection: A Survey” - Chandola et al. (2009)"
        }
    ]
}

json_string2={
            "Title":"samsung prism workelet title",
            "Problem Statement": "Time series data often contains anomalies or outliers that can significantly impact the performance of predictive models. Identifying these anomalies is crucial for various applications.",
            "Goal": "Develop a robust anomaly detection system for time series data using a combination of statistical methods and machine learning techniques.",
            "Expectations": "Participants will explore different anomaly detection algorithms (e.g., ARIMA, LSTM autoencoders), implement them on a real-world time series dataset, and evaluate their performance in terms of precision, recall, and F1-score.",
            "Training/Prerequisite": "Knowledge of time series analysis, statistical modeling, and machine learning techniques. Familiarity with libraries such as Statsmodels and scikit-learn is helpful.",
            "Difficulty": 1,
            "Reference Work": "“Anomaly Detection: A Survey” - Chandola et al. (2009)"
        }

json_string3={
    "Title":"Predictive Maintenance for Smart Home Devices Using Time Series Anomaly Detection",
    "Problem Statement":"Smart home devices generate vast amounts of time-series data. Identifying anomalies in this data can enable predictive maintenance, preventing device failures and improving user experience. Traditional anomaly detection methods may not be suitable for the complex and dynamic patterns exhibited by smart home device data.",
    "Goal":"Develop a time-series anomaly detection model to predict potential failures in smart home devices based on their historical sensor data. The model should be robust to noise and seasonality and capable of detecting subtle anomalies that precede device failures.",
    "Expectations":"Participants will collect or simulate time-series data from smart home devices, implement and evaluate various anomaly detection algorithms (e.g., LSTM-based autoencoders, isolation forests), and develop a system for visualizing and alerting users about potential device failures. A working demo showing predicted device state would be ideal.",
    "Training/Prerequisite":"Knowledge of time-series analysis, anomaly detection techniques, and machine learning algorithms. Familiarity with Python and relevant libraries like TensorFlow or PyTorch.",
    "Difficulty":6,
    "Reference Work":"Deep Learning for Anomaly Detection: A Review (https://www.researchgate.net/publication/344028491_Deep_Learning_for_Anomaly_Detection_A_Review)"}

json_string4 = {
    "Title": "Merging Deep Learning Models for Improved Performance",
    "Problem Statement": "Develop a method to merge multiple deep learning models to improve their performance and reduce computational cost.",
    "Goal": "Create an efficient algorithm that combines the strengths of various deep learning models while minimizing their weaknesses.",
    "Expectations": "Implement the algorithm in popular deep learning frameworks like TensorFlow or PyTorch, benchmark it against existing methods, and demonstrate improved performance and reduced computational cost.",
    "Training/Prerequisite": "Strong understanding of deep learning concepts, experience with popular deep learning libraries, knowledge of model pruning techniques.",
    "Difficulty": 7,
    "Reference Work": [
        {
            "title": "Matrix Expression of Bayesian Game",
            "link": "http://arxiv.org/pdf/2106.12161v1"
        },
        {
            "title": "Bayesian Distributionally Robust Optimization",
            "link": "http://arxiv.org/pdf/2112.08625v2"
        },
        {
            "title": "Bayesian Optimization with Shape Constraints",
            "link": "http://arxiv.org/pdf/1612.08915v1"
        },
        {
            "title": "Optimistic Optimization of Gaussian Process Samples",
            "link": "http://arxiv.org/pdf/2209.00895v1"
        },
        {
            "title": "On Batch Bayesian Optimization",
            "link": "http://arxiv.org/pdf/1911.01032v1"
        },
        {
            "title": "Cost-aware Bayesian Optimization via the Pandora's Box Gittins Index",
            "link": "http://arxiv.org/pdf/2406.20062v3"
        },
        {
            "title": "Local Nonstationarity for Efficient Bayesian Optimization",
            "link": "http://arxiv.org/pdf/1506.02080v1"
        },
        {
            "title": "Bayesian Optimization for Multi-objective Optimization and Multi-point Search",
            "link": "http://arxiv.org/pdf/1905.02370v1"
        },
        {
            "title": "Bayesian Hyperparameter Optimization with BoTorch, GPyTorch and Ax",
            "link": "http://arxiv.org/pdf/1912.05686v2"
        },
        {
            "title": "Topological Bayesian Optimization with Persistence Diagrams",
            "link": "http://arxiv.org/pdf/1902.09722v1"
        }
    ]

}
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.colors import lightgrey, blueviolet, HexColor
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate, Frame
import os

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


def generatePdf(json):
    pdf_filename = pdf_path+json["Title"]+".pdf"
    pdf = canvas.Canvas(pdf_filename, pagesize=(page_width, page_height))
    # draw_ruler(pdf, page_width,page_height)
    pdf.setTitle(pdf_filename)
    pdf.setTitle(pdf_filename)

# samsung logo
    pdf.drawImage(f"{PROJECT_ROOT}/resources/Samsung_Orig_Wordmark_BLUE_RGB.png", 1190,720, width=250, height=90, mask='auto')
    
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
# generatePdf(json_string4)