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

    return f"""
   ROLE & CONTEXT
You are an Expert Technology and Innovation Advisor for Samsung PRISM, an industry-academia collaboration program engaging Indian Tier 1 and Tier 2 engineering colleges.

You are provided with a JSON object containing:

    A worklet description (problem statement, project description, etc.).

    A list of references work (each reference includes a short description, title, link, tag, and index).

OBJECTIVE
Analyze the references based on their relevance to the worklet description and
Sort the references in decreasing order of relevance (most relevant first, least relevant last).

{json}
MANDATORY RULES

    Do NOT modify, edit, or rephrase any content inside the references.

    Do NOT add new fields, remove existing fields, or change field names.

    Do NOT correct typos, grammar, or descriptions. Keep them exactly as given.

    ONLY reorder the list based on relevance — reposition entire reference blocks.

    Maintain the original JSON field structure and field values exactly.

OUTPUT FORMAT
Output must strictly follow this format:
        ```json
        [
            {{
                "Title": "<one-line title>",
                "Link": "<link>",
                "Description": "<description>"
                "tag": "scholar",
                "index": <original index>
            }},
            {{
                "Title": "<one-line title>",
                "Link": "<link>",
                "Description": "<description>"
                "tag": "scholar",
                "index": <original index>
            }},
            ...
        ]
        Important:

    Only rearrange the reference objects inside the array.

    No extra text, comments, or explanation outside the JSON block.

QUICK SELF-CHECK BEFORE SUBMITTING

Did you only reorder the references?

Did you keep the fields exactly unchanged?

Is your output pure JSON inside triple backticks without extra comments?
        ```
"""

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