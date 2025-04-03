import requests
from langchain.prompts import ChatPromptTemplate
import xml.etree.ElementTree as ET
from llm import llm

prompt_template = ChatPromptTemplate.from_template(
    "I want you to give me a keyword to search in arxiv api to get me the research papers best suited for the following topic - {title}. Just give me the keyword as the answer, no extra stuff"
)

def getReferenceWork(title):
    """
    Write a function description later
    """
    keyword = getKeyword(title);
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

def getKeyword(title):
    prompt = prompt_template.format_prompt(title=title)
    response = llm.invoke(prompt)
    print(response.content.strip())
    return response.content.strip()