
# Worklet Generator 

## Create a virtual environment
Make sure Python is installed and added to your system PATH.
```
python -m venv venv
```

Activate the virtual environment

```
venv\Scripts\activate
```

Install required dependencies

```
pip install -r requirements.txt
```
 - It you are on linux use droplet-req.txt 
  - toml files are present if u use poetry as your venv manager(for windows)


## Make env file

copy the content of env.example  and past it into .env 
then fill it up 

## Download TeseractOCR


``` 
https://github.com/tesseract-ocr/tesseract/releases
```

from the  link download latest model and install it 

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
            └── generatepdf.py
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
