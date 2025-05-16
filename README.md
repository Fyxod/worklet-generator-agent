
# Worklet Generator 
## Clone the repo from GitHub 
```
git clone https://github.com/bedrockSp/Backend.git
```
## Create a virtual environment
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
 - It you are on linux use droplet-req.txt 
  - toml files are present if u use poetry as your venv manager(for windows)


## Make env file

copy the content of env.example and past it into .env 
then fill it up 

## Download TeseractOCR


``` 
https://github.com/tesseract-ocr/tesseract/releases
```

from the  link download latest model and install it 


## Test it out
Your are all set to go!
Run the following **command from the Worklet Generator Folder** to start the server

```
uvicorn app.main:app 
```

## File structure


```
└── 📁worklet-generator
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

#### Start reading from app/routers/root.py and follow the imports to understand the flow of the code.
#### The main.py file is the entry point of the application, where the FastAPI app is created and configured.
#### The app is run using Uvicorn, which is an ASGI server for running FastAPI applications.