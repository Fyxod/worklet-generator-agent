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
            "Difficulty": 9,
            "Reference Work": "“Anomaly Detection: A Survey” - Chandola et al. (2009)"
        }
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.colors import lightgrey, blueviolet
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate, Frame

# might need to use when the json is passed from different dunction
# import json
# json2 = json.loads(json_string2)
# print(json2)

# Define the page size in points (1 inch = 72 points)
page_width = 20 * 72  # 1440 points
page_height = 11.25 * 72  # 810 points


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



def generatePdf(json):
    pdf_filename = "../resources/generatedPdf/"+json["Title"]+".pdf"
    pdf = canvas.Canvas(pdf_filename, pagesize=(page_width, page_height))
    draw_ruler(pdf, page_width, page_height)
    pdf.setTitle(pdf_filename)

# pdf.drawString(0,0,"hi")
    x=740
    pdf.line(0,x,1440,x)
    y = 792
    pdf.line(0, y, 1440, y)

    q = 720
    pdf.line(0, q, 1440, q)
    a = 648
    pdf.line(0, a, 1440, a)
    # a = 1440
    pdf.line(360, 0,360, 810)
    pdf.line(360*3 ,0,360*3 , 810)

# samsung logo
    pdf.drawImage("../resources/Samsung_Orig_Wordmark_BLUE_RGB.png", 1190,720,
                 width=250, height=90, mask='auto')
# rectangles

 # small blue
    pdf.setFillColorRGB(18, 40, 140)
    pdf.rect(0, 730, 17, 792-730,  fill=1, stroke=0)

# small grey
    pdf.setFillColor(lightgrey)
    pdf.rect(30, 730, 10, 792-730,  fill=1, stroke=0)

# big grey
    pdf.setFillColor(lightgrey)
    pdf.rect(50,  50, 720-50, 720-50, fill=1, stroke=0)    # remove 50 and do zero

# title
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Times-Bold", 48)
    pdf.drawString(52, 753, json["Title"].capitalize())

    #problem statement
    pdf.setFillColorRGB(20/255, 60/255, 140/255)
    pdf.setFont("Times-Bold", 40)
    pdf.drawString(220, 648, "Problem Statement")

    # expecctation
    pdf.drawString(1010, 670, "Expectation")

# Paragaphs



    problem_style = ParagraphStyle(
        name="ProblemStyle",
        fontName="Times-Roman",
        fontSize=25,
        textColor=colors.black,
        leading=25,# Line spacing
        alignment=0    # Left-aligned
    )
    problem_paragraph = Paragraph(json["Problem Statement"], problem_style)
    goal_paragraph = Paragraph(json["Goal"], problem_style)
    Expectation_paragraph = Paragraph(json["Expectations"], problem_style)
    Training_Prerequisite_paragraph = Paragraph(json["Training/Prerequisite"], problem_style)

    # frames
    frame_problem = Frame(50, 432, 620, 216, showBoundary=1)
    frame_problem.addFromList([problem_paragraph], pdf)


    pdf.save()
    print(f"PDF generated: {pdf_filename}")
generatePdf(json_string2)