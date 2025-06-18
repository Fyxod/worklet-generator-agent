# Worklet Generator 
Worklet Generator is an AI-powered agent system designed to generate structured research project ideas from past work and web knowledge, and automatically convert those into presentable formats like PPTs and PDFs with relevant citations.

It combines the power of LLMs, web search, and scholarly references to help researchers, students, and innovation teams generate new project ideas quickly.

### What it does:
- Takes previous research ideas as context.
- Extracts keywords and domain concepts
- Performs web search to expand context using real-time info.
- Uses LLMs to generate structured new research ideas (in JSON format).
- Converts structured ideas into PPTs and PDFs.
- Scrapes relevant references from Google Scholar and GitHub.
  - Falls back to regular web search if Google Scholar fails.
  - All references are ranked by relevance using an LLM.

## Getting Started

### Clone the repo from GitHub 
```
git clone https://github.com/bedrockSp/Backend.git
```
### Create a virtual environment
Make sure Python is installed and added to your system PATH.
```
python -m venv my_env
```

Activate the virtual environment

```
.\my_env\Scripts\activate
```

Install required dependencies

```
pip install -r requirements.txt
```
  - If you are on linux use droplet-req.txt 
  - toml files are present if u use poetry as your venv manager(for windows)


### Setup .env file

copy the content of .env.example and past it into .env 
then fill it up 

### Install Tesseract OCR


``` 
https://github.com/tesseract-ocr/tesseract/releases
```

from the  link download latest model and install it 


### Run the Server
Run this command from the worklet-generator-agent root folder:

```
uvicorn app.main:app 
```

## File structure


```
└── 📁worklet-generator-agent
    └── 📁app
        └── __init__.py
        └── llm.py
        └── main.py
        └── 📁public
            └── icon.png
        └── 📁resources
            └── 📁archived_images
            └── 📁archived_worklets
            └── 📁extracted_images
            └── 📁generated_worklets
        └── 📁routers
            └── __init__.py
            └── root.py
        └── socket.py
        └── 📁utils
            └── generate_references.py
            └── generate_worklets.py
            └── make_files.py
            └── link_extractor.py
            └── llm_response_parser.py
            └── parser.py
            └── prompt_templates.py
            └── 📁reference_functions
                └── github.py
                └── google_scholar.py
                └── reference_sort.py
                └── 📁scholar_package
                    └── __init__.py
                    └── 📁custom_backend
                        └── author_info_all_articles.py
                        └── cite_results.py
                        └── google_scholar_cited_by_public_access_author.py
                        └── organic_search.py
                        └── profiles_results.py
                        └── top_mandates_metrics.py
                        └── top_publications_article_citation.py
                        └── top_publications_article.py
                        └── top_publications_metrics.py
            └── 📁search_functions
                └── duck.py
                └── google_search.py
                └── search.py
    └── 📁templates
        └── index.html
    └── .env.example
    └── droplet-req.txt
    └── poetry.lock
    └── pyproject.toml
    └── README.md
    └── requirements.txt
```
## Folder Descriptions
- **app**: Contains the main application code, including the FastAPI app, routers, and utility functions.
- **public**: Contains static files, such as icons and images.
- **resources**: Contains directories for archived images, archived worklets, extracted images, and generated worklets.
- **routers**: Contains the FastAPI routers for handling different API endpoints.
- **socket.py**: Contains the WebSocket implementation for real-time communication between the server and client.
- **utils**: Contains utility functions for generating references, worklets, PDFs, and parsing LLM responses.
- **templates**: Contains templates for rendering HTML pages.

## Developer Notes
- Start reading from app/routers/root.py to understand the flow.

- main.py is the app entrypoint.

- Worklet flow: Input → Context + Search → LLM → Structured Output → PPT/PDF + References.
