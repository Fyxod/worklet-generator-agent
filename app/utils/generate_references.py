import requests
from langchain.prompts import ChatPromptTemplate
import xml.etree.ElementTree as ET
from app.llm import llm, invoke_llm
from langchain.schema.messages import HumanMessage

prompt_template = ChatPromptTemplate.from_template(
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
# prompt_template = ChatPromptTemplate.from_template(
#     """
#     I want you to strictly just give me a keyword to search in arxiv api to get me the research papers best suited for the following topic - {title}. Just give me the keyword as the answer and no other extra stuff
#     """
# )

def getReferenceWork(title, model):
    """
    Write a function description later
    """
    print("Inside reference work ", title)
    keyword = getKeyword(title, model);
    url = f"http://export.arxiv.org/api/query?search_query=all:{keyword}"
    response = requests.get(url)
    response.raise_for_status()
    
    root = ET.fromstring(response.content)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    reference_work = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text 
        pdf_link = None

        for link in entry.findall('atom:link', ns):
            if link.get('title') == 'pdf':
                pdf_link = link.get('href')
                break 

        if pdf_link:
            reference_work.append({"title": title, "link": pdf_link})
    
    return reference_work

def getKeyword(title, model):
    print("Inside getKeyword ", title)
    prompt = prompt_template.format(title=title)
    print("printing prompt", prompt)
    # prompt = prompt_template.format_prompt(title=title).to_string()
    response = invoke_llm(prompt, model)
    # response = llm.invoke([HumanMessage(content=prompt)])
    return response

# print(getKeyword("Job Scheduling with AWS DynamoDB and Spring Reactive Framework", "deepseek-r1:70b"))