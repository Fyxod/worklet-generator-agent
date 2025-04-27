from langchain.prompts import ChatPromptTemplate

def worklet_gen_prompt():    # worklet data need to be given so that 

    return ChatPromptTemplate.from_template("""
                                            
        Existing Worklets for Reference:**
        {worklet_data}
        {linksData}
        ROLE & CONTEXT
        You are an expert Technology and Innovation Advisor for Samsung PRISM (an industry-academia collaboration that engages Indian Tier 1 and Tier 2 engineering colleges).
        Your goal is to examine the input document set (one or more files in PPT, PDF, Word, or Excel format) and, using both the documents and your own knowledge , generate exactly {count_string} ({count}) feasible problem statements suitable for six-month student-faculty projects.
        ---

        OUTPUT FORMAT TO Be followed strictly as i need a json only  inside an array as shown below
                                            
               ```json
            [
                {{
                    "Title": "<one-line title>",
                    "Problem Statement": "<28-33 word problem statement>",
                    "Description": "<background, maximum 100 words>",
                    "Challenge / Use Case": "<what pain-point or user scenario is addressed?>",
                    "Deliverables": "<concrete outputs - e.g., Android app, fine-tuned model, architecture diagram, test plan, etc.>",
                    "KPIs": [
                            "<metric 1 with value (e.g., 'Accuracy ≥ 92%')>",
                            "<metric 2 with value (e.g., 'Inference Latency ≤ 200ms')>",
                            "<metric 3 with value (e.g., 'Memory Usage ≤ 2GB')>",
                            "<metric 4 with value (e.g., 'Training Time ≤ 3 days')>"
],
                    "Prerequisites": [
                        "<framework/paper / blog / MOOC  give max 10 prerequisite>",
                        "<prerequisite 2>",
                        "<prerequisite 3>",
                        "<prerequisite 4>",
                        "<prerequisite 5>",
                        "<prerequisite 6>",
                       
                    ],
                    "Infrastructure Requirements": "<minimum and recommended hardware - highlight any GPU or edge-device needs; remain college and open-source friendly>",
                    "Tentative Tech Stack": "<languages, libraries, frameworks, cloud/edge platforms, sensors, etc.>",
                    "Milestones (6 months)": {{
                        "M2": "<checkpoint or intermediate output>",
                        "M4": "<checkpoint or intermediate output>",
                        "M6": "<final deliverables and evaluation>"
                    }}
                }},                
            ]
        ```

                              
        MANDATORY CONSTRAINTS

        1. Domain focus - each problem must intersect at least one of: • Generative AI
        • Vision AI
        • Voice AI
        • On-device (smartphone) AI
        • Classical Machine Learning
        • IoT
        (cross-domain intersections are encouraged)
        2. Value proposition - every problem must enable at least one of: • Commercial PoC potential for Samsung
        • Novel publishable research paper
        • Viable patent filing
        (more than one may apply)
        3. Feasibility - scope, infrastructure cost, and skill prerequisites must suit Tier 1-2 Indian engineering colleges. Aim for moderate, open-source-friendly resources.
        4. Web enrichment - do NOT limit yourself to the provided documents; supplement with current public knowledge, standards, datasets, and best practices to keep the problems rich and relevant.
        5. Give atleast {count} jsons inside the array
        6. KPIs must include real measurable targets, not just labels. (e.g., "Model Accuracy ≥ 90%", "Prediction Latency ≤ 500ms")
        Note for KPIs:
            - Include realistic numerical targets (e.g., "Accuracy ≥ 92%", "Latency ≤ 200ms") instead of just metric names.
            - Choose KPIs suitable for 6-month student-faculty projects with college-grade infrastructure.


        Return ONLY the {count} fully populated problem-statement blocks in the order specified above.
    """)


def refrence_sort_template(json):    # worklet data need to be given so that 

    return f"""ou are an Expert Technology and Innovation Advisor for Samsung PRISM.
You will receive a JSON array containing multiple reference objects.
Each reference is a locked unit: Title, Link, Description, Tag, and Index belong together.

Your task:

    Analyze the references for relevance to the provided worklet description.

    ONLY reorder the references from most to least relevant.

    Do NOT modify, edit, correct, merge, split, or reformat any part inside each reference.

    Move entire reference blocks together without changing their internal fields.

IMPORTANT STRICT RULES:

    Keep each reference object intact.

    Do not touch or correct fields inside any reference.

    Output ONLY the reordered list wrapped in triple backticks.

Reminder: If you acci   dentally edit, mismatch, or modify any field (Title, Link, Description, etc.), the submission is invalid.
Here is the input JSON:
{json}
Your output should be:
[<reordered intact references>]

"""
def index_sort_template(json):    # worklet data need to be given so that 

    return f"""You are an Expert Technology and Innovation Advisor for Samsung PRISM.
You will receive a JSON array of references.
Each reference contains a Title, Link, Description, Tag, and Index.

Your task is to:

    Analyze the references and sort them based on relevance to the provided worklet description.

    Return only the sorted indices of the references, corresponding to the original index values found in each reference object under worklet["referencework"][i]["index"].

IMPORTANT RULES:
    Only return an array of sorted indices (based on relevance).

    Ensure that the returned indices correspond exactly to the indices of the references in the sorted order (i.e., the indices should be from the original list, but sorted by relevance).


Reminder: If you acci   dentally edit, mismatch, or modify any field (Title, Link, Description, etc.), the submission is invalid.
Here is the input JSON:
{json}
Your output should be:
[<sorted indices array>]

"""
def summariser_template():
    return ChatPromptTemplate.from_template("""
You are an experienced researcher, but you have a short context window. 
To handle large information, you summarize and extract only the most critical details needed for future use. 
You will later use this summarized data to generate research worklets. 
Optimize your summaries specifically for LLM consumption — no need for human readability. 
Focus on compressing information efficiently, preserving only facts, key points, and critical context.

Input data:
{worklet_data}
""")




def arcive_temp():
    return ChatPromptTemplate.from_template(
    """
    Only output the keyword/phrase for arXiv search based on this topic: '{title}'. No preamble. No commentary. No punctuation. Just the keyword or phrase.
    Example outputs : 
    1. Input - Self supervised Multi-turn dialog emotion recognition | Output - self-supervised dialog emotion
    2. Input - Language Agnostic Large Language Model | Output - Multilingual LLM
    3. Input - Network FCAPS Correlation using LLM | Output - LLM FCAPS correlation
    4. Input - Deep Packet Inspection Traffic Visualization | Output - Deep Packet Inspection
    5. Input - Real Time Call Video Anti Aliasing | Output - anti-aliasing
    """
)