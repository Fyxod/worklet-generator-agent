import asyncio
from app.llm import invoke_llm
from app.utils.reference_functions.github import get_github_references
from app.utils.reference_functions.google_scholar import get_google_scholar_references
from app.utils.search_functions.search import search_references
from concurrent.futures import ThreadPoolExecutor
from app.utils.prompt_templates import keyword_prompt

async def getReferenceWork(title, model="gemma3:27b"):
    """
    Asynchronously generates a list of references related to a given title by querying 
    GitHub, Google Scholar, and other sources.
    Args:
        title (str): The title or topic for which references are to be generated.
        model (str, optional): The model to use for generating keywords. Defaults to "gemma3:27b".
    Returns:
        list: A list of references obtained from GitHub, Google Scholar, and other sources.
    Raises:
        Exception: If an error occurs while generating the keyword.
    Notes:
        - The function uses a ThreadPoolExecutor to run blocking I/O operations in separate threads.
        - If Google Scholar references are not found initially, the function retries after a delay.
        - Additional references are fetched using a fallback search if Google Scholar references remain unavailable.
    """

    keyword = ""
    try:
        keyword = await getKeyword(title, model)
    except Exception as e:
        keyword = title

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        github_future = loop.run_in_executor(None, get_github_references, keyword)
        scholar_future = loop.run_in_executor(None, get_google_scholar_references, keyword)

        githubReferences, googleScholarReferences = await asyncio.gather(github_future, scholar_future)
        googleReferences = []

        if len(googleScholarReferences) == 0:
            await asyncio.sleep(5)
            googleScholarReferences = get_google_scholar_references(keyword)

        if len(googleScholarReferences) == 0:
            googleReferences = search_references(keyword, max_results=10)

    response = []
    response.extend(googleScholarReferences)
    response.extend(githubReferences)
    response.extend(googleReferences)

    return response

async def getKeyword(title, model):
    """
    Asynchronously generates a keyword based on the given title using a specified language model.
    Args:
        title (str): The title or text input for which a keyword needs to be generated.
        model (Any): The language model to be used for generating the keyword.
    Returns:
        Any: The response from the language model containing the generated keyword.
    """

    prompt = keyword_prompt().format(title=title)
    response = await invoke_llm(prompt, model)
    return response
