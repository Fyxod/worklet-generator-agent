from langchain.prompts import ChatPromptTemplate

# this prompt will be used to extract keywords from the data
def keywords_from_worklets_custom_prompt(custom_prompt, worklet_data, links_data):
    return f""" ROLE & CONTEXT

You are an expert Technology and Innovation Advisor for Samsung PRISM — an industry-academia collaboration that engages Indian Tier 1 and Tier 2 engineering colleges.

Your task is to analyze the provided documents and extracted data and identify high-impact keywords and relevant domains from the following sources:

1. Existing Worklets
2. Data Extracted from Links
3. Custom User Prompt

Extraction Goals
 A. Keywords
Extract concise keywords focusing on:

 Technical concepts
 Emerging technologies
 Problem domains
 Solution approaches
 Application areas
 
Keyword Rules:
 1 to 3 words max
 Avoid generic terms like "project" or "engineering" unless domain-specific
 No repetition across sections unless essential
 Prioritize novelty and relevance
 
B. Domains
Identify broad application or research domains, such as(therse are just examples do not limit your self to these only):
Healthcare,
Smart Cities,
AgriTech,
FinTech,
Cybersecurity,
Automotive,
EdTech,
IoT
Energ
Do not limit to this list — include any domain that is:
Clearly stated or strongly implied
Relevant to the context of innovation or research
Specific enough to categorize the project's purpose or area of application

---

Input Sections

 Existing Worklets for Reference:

{worklet_data}

---

 Data Extracted from Links:

{links_data}

---

 Custom Prompt from User:

{custom_prompt}

---

  Output Format (JSON)

```json
{{
  "worklet": {{
    "keywords": ["keyword1", "keyword2", "..."],
    "domains": ["domain1", "domain2", "..."]
  }},
  "link": {{
    "keywords": ["keyword1", "keyword2", "..."],
    "domains": ["domain1", "domain2", "..."]
  }},
  "custom_prompt": {{
    "keywords": ["keyword1", "keyword2", "..."],
    "domains": ["domain1", "domain2", "..."]
  }}
}}
```

Mandatory constraints 
Strictly adhere to the specified output format. Your response must be a valid JSON object exactly as defined above — no additional text, explanations, markdown, or disclaimers are allowed. Any deviation from this format will be considered an invalid submission.


"""

#  This Prompt is meant to search for web only
def web_search_prompt(count,count_string,worklet_data,links_data,custom_prompt,keywords,domains,):

    return f"""ROLE & CONTEXT
You are an expert Technology and Innovation Advisor for Samsung PRISM — an industry-academia collaboration that engages Tier 1 and Tier 2 engineering colleges across India.

You are tasked with analyzing:

 A set of internal documents (PPTs, PDFs, Word, Excel files)
 Extracted content from provided links
 Previously extracted keywords and domains
 A custom user prompt (see below)

---

Inputs Provided
Worklet References:
{worklet_data}

Extracted Data from External Links:
{links_data}
Custom User Prompt (must follow strictly):
{custom_prompt}
Keywords:
{keywords}
Domains:
{domains}

INFORMATION GATHERING
You may use internal knowledge and provided material to generate problems.
However, if you suspect any gap in your understanding, you MUST initiate a web search for clarification or enrichment.

If clarification is needed for any keyword, domain, or part of the user prompt, add it to the web queries.
Default bias: When unsure, prefer to trigger a web search.
---
TWO PATHWAYS (Web Search Decision)
Option 1: You have enough information
Return:
```json
{{
  "websearch": false
}}
```

 Option 2: You need external information
Return:
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
You may ask about:

Gaps in understanding the user prompt
Missing context about keywords
Deeper insight into domains
New technology trends or datasets

MANDATORY CONSTRAINTS

1 Value Proposition
    Each problem should enable at least one of the following:
    A Commercial PoC potential for Samsung
    A Publishable research paper
    A Viable patent filing
    
2 Feasibility
    Must be achievable by Tier 1-2 Indian colleges
    Should use moderate infrastructure (e.g., open-source tools, cloud credits, public datasets)

3 Web Enrichment
    Supplement provided data with 2025 (or latest) tools, benchmarks, standards, and best practices
    If unsure about a topic, tool, or trend, trigger web search
    
    
4 Freshness
    Ensure alignment with 2025-era trends, tech stacks, models, APIs, frameworks, etc.
    Do not use outdated standards unless explicitly asked
    
5. desigh your web querries keeping the above  points in mind and ask for as much querries as you want 

6. ctly adhere to the specified output format. Your response must be a valid JSON object exactly as defined above — no additional text, explanations, markdown, or disclaimers are allowed. Any deviation from this format will be considered an invalid submission.
"""

# This Prompt is meant to Generate The Final Worklets
def worklet_gen_prompt_with_web_searches(
    count_string,
    links_data,
    json,
    worklet_data,
    domains,
    custom_prompt,
    keywords,
    count: int = 6,
):

    return f"""
ROLE & CONTEXT

You are an expert Technology and Innovation Advisor for Samsung PRISM — an industry-academia collaboration that engages Indian Tier 1 and Tier 2 engineering colleges.

You are tasked with carefully examining the provided document set (PPT, PDF, Word, Excel files), as well as any prior extracted information or links.

Included:
Existing Worklets for Reference:
{worklet_data}
Data Extracted from External Links:
{links_data}
Web search results previously requested in one of our previous interactions:
{json}

USER PROMPT (STRICTLY FOLLOW THIS):

Please use the following prompt as the definitive guide. All outputs must directly address this prompt. In case of any conflict with general instructions, the user prompt takes precedence.
User Prompt:  
{custom_prompt}

Your objective is to generate exactly {count_string} ({count}) feasible problem statements, following the format below.

KEY DIFFERENTIATION: KEYWORDS vs DOMAINS

Keywords: Specific technologies, methods, models, or terms.  
Examples: "federated learning", "quantization", "LLM fine-tuning", "YOLOv8", "LoRaWAN", "diffusion models".
Domains: Broad areas of application or research.  
Examples: "Healthcare", "Cybersecurity", "AgriTech", "Smart Cities", "Climate Tech", "EdTech", "SpaceTech", "AR/VR".

Each problem must be grounded in a valid domain and include relevant, cutting-edge keywords.

---

MANDATORY CONSTRAINTS

1. Domain Focus:  
   Each problem must involve at least one domain from {domains}.  
   Cross-domain intersections are allowed and encouraged.  
   No unrelated domains should be included.
2. Keyword Focus  
   Keywords must be the central focus of the problem statement.  
   Use keywords {keywords}to define the technical approach, methods, and technologies involved.  
   Do not stray from the provided keywords, avoid generic or unrelated terms.

3. Value Proposition:  
    Each problem must target at least one of:
    Commercial PoC potential for Samsung
    Publishable academic research
    Patentable novelty

4. Feasibility:  
   Must be realistic for Tier 1 or Tier 2 Indian engineering colleges  
   Infrastructure must be moderate (cloud credits, GPUs, open data, etc.
5. Web Enrichment:  
    Do not rely only on internal material  
    Supplement with 2025 (or latest) benchmarks, tools, APIs, datasets, literature, etc.
6. Quantity:  
   Generate exactly {count} problem statements

7. KPIs:  
   Include 3-4 real, measurable targets per problem (e.g., “Accuracy ≥ 92%”, “Latency ≤ 200ms”)

8. Freshness:  
   Use the latest frameworks, methods, or libraries.  
   When in doubt or encountering ambiguity, initiate a web search.  
   Ask multiple queries at once to clarify technology, problem scope, or domain gaps.

9. Prompt Adherence:  
   - All generated content must strictly follow the User Prompt:  
    {custom_prompt}
    
10 Strictly adhere to the specified output format. Your response must be a valid JSON object exactly as defined above — no additional text, explanations, markdown, or disclaimers are allowed. Any deviation from this format will be considered an invalid submission.

---

OUTPUT FORMAT


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

Reminder: If you accidentally edit, mismatch, or modify any field (Title, Link, Description, etc.), the submission is invalid.
Here is the input JSON:
{json}
OUTPUT FORMAT :
[<sorted indices array>]

Mandatory Constraints 
follow the output constraints, example OUTPUT =[1,6,2,3,9,8,10]
do not return anything else except the output asked for no extra text and formatting
sort then in eccreasing order of relevance to the current worklet (most important constraint)
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