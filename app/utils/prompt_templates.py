from langchain.prompts import ChatPromptTemplate


# This Prompt is meant to search for web only
def web_search_prompt():

    return ChatPromptTemplate.from_template(
        """
**ROLE & CONTEXT**

    You are an expert Technology and Innovation Advisor for Samsung PRISM (an industry-academia collaboration that engages Indian Tier 1 and Tier 2 engineering colleges).

    You are tasked with carefully examining the provided document set (PPT, PDF, Word, Excel files) and any prior information.

    1. **Internal Knowledge Generation**:
   If you find the provided material and your internal knowledge sufficient,  generate exactly {count_string} ({count}) feasible problem statements.
    2. **Web Search Assistance**:
   If you determine that additional external information is necessary to enhance the quality, relevance, or feasibility of the problem statements, you have the ability to request a web search.
   To do this, you must return a JSON object in the structure provided below:

   Use this option proactively whenever you suspect that external sources could improve accuracy, freshness, or richness of the problem statements give all the queries at once .
   **When unsure, prefer to request a web search rather than relying solely on internal knowledge.**
    Existing Worklets for Reference:
    {worklet_data}
    {links_data}
    Along with these references, here is a prompt provided by the user. Let us call it user prompt. Please make sure to follow it strictly.
    {custom_prompt}
    If you dont understand anything inside the custom prompt or you need more clarificationon the topic , add a search query for that too
---

**TWO OPTIONS AFTER ANALYSIS:**

1. **If you believe you have enough information** just retuern a json as follows 
```json
   {{
     "websearch": false
   }}
   ```

2. **If you believe additional external information is needed** to improve quality, relevance, or feasibility:
     retuen a json in this format 
     ```json
   {{
     "websearch": true,
     "search": [
       "<search query 1>",
       "<search query 2>",
       "<search query 3>"
     ]
   }}
   ```
**OUTPUT FORMAT** (Mandatory if proceeding without websearch):
Follow the format below to iniceate a web search:
   ```json
   {{
     "websearch": true,
     "search": [
       "<search query 1>",
       "<search query 2>",
       "<search query 3>"
     ]
   }}
   ```
Follow the format below if you think you have enough information to generate worklets  :

```json
   {{
     "websearch": false
   }}
```


**MANDATORY CONSTRAINTS**

1. **Domain focus**: Must involve at least one domain from {custom_topics}, and no other domains should be included.(cross-domain intersections are encouraged)
2. **Value proposition**: Every problem must enable at least one:
- Commercial PoC potential for Samsung
- Publishable research paper
- Viable patent filing
(more than one may apply)
3. **Feasibility**: Problems must match Tier 1-2 Indian college resources (open-source friendly, moderate infra).
4. **Web enrichment**: do NOT limit yourself to the provided documents; supplement with current public knowledge, standards, datasets, and best practices to keep the problems rich and relevant.
5. **Quantity**: Generate exactly {count} problem statements inside the array.
6. **KPIs**: Must be real, measurable targets (e.g., "Accuracy ≥ 92%", "Latency ≤ 200ms").
7. **Freshness**: Align with 2025(or latest) technology trends,frameworks,tools,libraries etc. If in doubt, initiate a web search. Ask as many questions you want to ask at once
8. If a user prompt is provided, ensure strict adherence to its instructions and constraints. Here is the user prompt {custom_prompt}
"""
    )

# this prompt will be used to extract keywords from the data
def keywords_from_worklets_custom_prompt(custom_prompt, worklet_data, links_data):
    return f"""
**ROLE & CONTEXT**

You are an expert Technology and Innovation Advisor for Samsung PRISM — an industry-academia collaboration that engages Indian Tier 1 and Tier 2 engineering colleges.

Your task is to carefully examine the provided set of documents (PPTs, PDFs, Word files, Excel sheets) and the extracted data from provided links. Based on this analysis, extract **relevant and high-impact keywords** from:

1. Existing Worklets
2. Data Extracted from Links
3. Custom User Prompt

---

**Guidelines and Constraints:**

- Focus on **technical themes**, **emerging technologies**, **problem domains**, **solution approaches**, and **application areas**.
- Keywords should be **concise**, preferably **one to three words** long.
- Avoid common stopwords or generic terms like "project", "engineering", "data", unless highly domain-specific.
- Do not repeat keywords across different sections unless necessary.
- Prioritize **novelty**, **relevance**, and **potential research directions**.

---

**Existing Worklets for Reference:**

{worklet_data}

---

**Data Extracted from Links:**

{links_data}

---

**Custom Prompt from User:**

{custom_prompt}

---

**Output Format (JSON):**

{{
    "worklet": ["keyword1", "keyword2", ...],
    "link": ["keyword1", "keyword2", ...],
    "custom_prompt": ["keyword1", "keyword2", ...]
}}
"""


# This Prompt is meant to Generate The Final Worklets
def worklet_gen_prompt_with_web_searches(
    count_string,
    links_data,
    json,
    worklet_data,
    custom_topics,
    custom_prompt,
    count: int = 6,
):

    return f"""
**ROLE & CONTEXT**

    You are an expert Technology and Innovation Advisor for Samsung PRISM (an industry-academia collaboration that engages Indian Tier 1 and Tier 2 engineering colleges).
    You are tasked with carefully examining the provided document set (PPT, PDF, Word, Excel files) and any prior information.
    Existing Worklets for Reference:
    {worklet_data}
    {links_data}
    

    In one of our previous conversation you requested son=me information from the web i have attached it below 
    {json}   
    
** USER PROMPT (STRICTLY FOLLOW THIS):**  
Please use the following prompt as the definitive guide. All outputs must directly address this prompt. In case of any conflict with general instructions, the custom prompt takes precedence.  

**User Prompt:**  
{custom_prompt}
    
generate exactly {count_string} ({count}) feasible problem statements, following the output format described below
**OUTPUT FORMAT** :

```json
[
    {{
        "Title": "<one-line title>",
        "Problem Statement": "<28-33 word problem statement>",
        "Description": "<background, maximum 100 words>",
        "Challenge / Use Case": "<pain-point or user scenario>",
        "Deliverables": "<outputs - e.g., app, model, diagram, etc.>",
        "KPIs": [
            "<metric 1 with value>",
            "<metric 2 with value>",
            "<metric 3 with value>",
            "<metric 4 with value>"
        ],
        "Prerequisites": [
            "<prerequisite 1>",
            "<prerequisite 2>",
            "<prerequisite 3>",
            "<prerequisite 4>",
            "<prerequisite 5>",
            "<prerequisite 6>"
        ],
        "Infrastructure Requirements": "<minimum and recommended hardware>",
        "Tentative Tech Stack": "<languages, libraries, platforms, etc.>",
        "Milestones (6 months)": {{
            "M2": "<checkpoint>",
            "M4": "<checkpoint>",
            "M6": "<final deliverable>"
        }}
    }},
    ...
]
```


**MANDATORY CONSTRAINTS**


1. **Domain focus**: Must involve at least one domain from {custom_topics}, and no other domains should be included.(cross-domain intersections are encouraged)
2. **Value proposition**: Every problem must enable at least one:
- Commercial PoC potential for Samsung
- Publishable research paper
- Viable patent filing
(more than one may apply)
3. **Feasibility**: Problems must match Tier 1-2 Indian college resources (open-source friendly, moderate infra).
4. **Web enrichment**: do NOT limit yourself to the provided documents; supplement with current public knowledge, standards, datasets, and best practices to keep the problems rich and relevant.
5. **Quantity**: Generate exactly {count} problem statements inside the array.
6. **KPIs**: Must be real, measurable targets (e.g., "Accuracy ≥ 92%", "Latency ≤ 200ms").
7. **Freshness**: Align with 2025(or latest) technology trends,frameworks,tools,libraries etc. If in doubt, initiate a web search. Ask as many questions you want to ask at once
8. If a user prompt is provided, ensure strict adherence to its instructions and constraints. Here is the user prompt {custom_prompt}
"""


def refrence_sort_template(json):

    return f"""you are an Expert Technology and Innovation Advisor for Samsung PRISM.
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

Reminder: If you accidentally edit, mismatch, or modify any field (Title, Link, Description, etc.), the submission is invalid.
Here is the input JSON:
{json}
Your output should be:
[<reordered intact references>]

"""


def index_sort_template(json):  # worklet data need to be given so that

    return f"""You are an Expert Technology and Innovation Advisor for Samsung PRISM.
You will receive a python dictionary with a list  of Reference Work.
Each reference contains a Title, Link, Description, Tag, and reference_id.

Your task is to:

    Analyze the references and sort them based on relevance to the provided worklet description.

    Return only the sorted reference_id of the references, corresponding to the original reference_id values found in each reference object under worklet["referencework"][i]["index"].

IMPORTANT RULES:
    Only return an array of sorted indices (based on relevance).

    Ensure that the returned indices correspond exactly to the indices of the references in the sorted order (i.e., the indices should be from the original list, but sorted by relevance).
    Sometimes you return extra text please make sure that does not happen i just need a alist of reference_id sorted in order of relevance

Reminder: If you acci   dentally edit, mismatch, or modify any field (Title, Link, Description, etc.), the submission is invalid.
Here is the input JSON:
{json}
**OUTPUT FORMAT** :
[<sorted indices array>]
Mandatory Constraints 
- follow the output constraints, example OUTPUT =[1,6,2,3,9,8,10]
-do not return anything else except the output asked for no extra text and formatting
- sort then in eccreasing order of relevance to the current worklet (most important constraint)

"""


def summariser_template():
    return ChatPromptTemplate.from_template(
        """
You are an experienced researcher, but you have a short context window. 
To handle large information, you summarize and extract only the most critical details needed for future use. 
You will later use this summarized data to generate research worklets. 
Optimize your summaries specifically for LLM consumption — no need for human readability. 
Focus on compressing information efficiently, preserving only facts, key points, and critical context.

Input data:
{worklet_data}
"""
    )


def keyword_prompt():
    return ChatPromptTemplate.from_template(
        """
    Only output the keyword/phrase for google scholar search based on this problem statement: '{title}'. No preamble. No commentary. No punctuation. Just the keyword or phrase.
    Example outputs : 
    1. Output - self-supervised dialog emotion
    2. Output - Multilingual LLM
    3. Output - LLM FCAPS correlation
    4. Output - Deep Packet Inspection
    5. Output - anti-aliasing
    6. Output - LLM for code generation and debugging
    """
    )
