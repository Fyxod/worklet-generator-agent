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
                        "<metric 1>",
                        "<metric 2>",
                        "<metric 3>",
                        "<metric 4>"
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

        Return ONLY the {count} fully populated problem-statement blocks in the order specified above.
    """)


def refrence_sort_template(json):    # worklet data need to be given so that 
    return f"""
    ROLE & CONTEXT
        You are an expert Technology and Innovation Advisor for Samsung PRISM (an industry-academia collaboration that engages Indian Tier 1 and Tier 2 engineering colleges).
        Your goal is to understanf the json of a worklet being provided and understand the references given a short description of the reference work is provided to inside the reference json 
        {json}
    Goal 
        you need to sort these references in order of the decreasing relevance id u thing one reference is better than other put the better first
                                                                               
    MANDATORY CONSTRAINTS
        do not add or remove content just change the positioning i.e sort reference and do not change in input format
        Output format:
        ```json
        [
            {{
                "Title": "<one-line title>",
                "Link": "<link>",
                "Description": "<description>"
            }},
            {{
                "Title": "<one-line title>",
                "Link": "<link>",
                "Description": "<description>"
            }},
            ...
        ]
        ```
"""