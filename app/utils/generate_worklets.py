import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.llm import invoke_llm
from app.socket import is_client_connected, sio
from app.utils.llm_response_parser import extract_dicts_smart
from app.utils.prompt_templates import (
    web_search_prompt,  
    worklet_gen_prompt_with_web_searches,
    keywords_from_worklets_custom_prompt
)
from app.utils.search_functions.search import search
from app.utils.search_functions.modify_websearch_queries import get_approved_queries
from app.utils.search_functions.modify_keywords_domains import get_approved_content
executor = ThreadPoolExecutor(max_workers=5)

async def generate_worklets(worklet_data, links_data, model, sid, custom_prompt):
    count = 5
    count_string = "five"

    loop = asyncio.get_running_loop()
    # New order
    # keywords -> websearch -> frontend ->  update keywords and web search -> do websearch -> Final worklet generation prompt 
    await sio.emit("progress", {"message": "Extracting keywords and domains..."}, to=sid)
    
    # extracting keywords and domains from worklet_data, links_data and custom_prompt
    keyword_domain_prompt =keywords_from_worklets_custom_prompt(custom_prompt,worklet_data,links_data)
    try:
        topics=await invoke_llm(prompt=keyword_domain_prompt,model=model)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: LLM is not responding. Please try again."}, to=sid)
        return
    
    try:
        topics = extract_dicts_smart(topics,True)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: Wrong output returned by LLM. Please try again."}, to=sid)
        return    

    # seperating domains and keywords from the topics
    domains = {
    "worklet_domains": topics.get("worklet", {}).get("domains", []),
    "link_domains": topics.get("link", {}).get("domains", []),
    "custom_prompt_domains": topics.get("custom_prompt", {}).get("domains", []),
    }
    
    keywords = {
    "worklet_keywords": topics.get("worklet", {}).get("keywords", []),
    "link_keywords": topics.get("link", {}).get("keywords", []),
    "custom_prompt_keywords": topics.get("custom_prompt", {}).get("keywords", []),
    }

    # Prompting the user to approve the domains and keywords and add any new ones
    domains, keywords = await get_approved_content(domains=domains, keywords=keywords, sid=sid)
    
    web_search_prompt_template = web_search_prompt(
        worklet_data=worklet_data,
        links_data=links_data,
        count=count,
        custom_prompt=custom_prompt,
        count_string=count_string,
        keywords=keywords,
        domains=domains
    )

    await sio.emit("progress", {"message": "Prompting LLM for web search decision..."}, to=sid)

    # Asking the LLM if it wants to do a web search or not
    try:
        web_search_output = await invoke_llm(web_search_prompt_template, model)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: LLM is not responding. Please try again."}, to=sid)
        return

    try:
        web_search_output = extract_dicts_smart(web_search_output,True)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: Wrong output returned by LLM. Please try again."}, to=sid)
        return

    if not is_client_connected(sid):
        print(f"Client {sid} is not connected. Skipping web search. Exiting...")
        return

    if web_search_output.get("websearch",False):
        show_message = "LLM requested for web search. Queries: "
        queries = web_search_output.get("search", [])  
    else:
        show_message = "LLM refused web search. Add any queries if needed: "
        queries = []

    # prompting the user to approve the web queries and add any new ones
    queries = await get_approved_queries(queries=queries, sid=sid, show_message=show_message)
    print("printing updated queriies")
    print(queries)
    socket_message = "Generating worklets..."
    search_data=''
    if queries != []:
        await sio.emit("progress", {"message": "Searching the web..."}, to=sid)
        try:
            search_data = await loop.run_in_executor(executor, search, queries, 10,500)
        except Exception as e:
            await sio.emit("error", {"message": "ERROR: Web search failed. Please try again."}, to=sid)
            return
        socket_message = "Generating worklets with web search results..."

    await sio.emit("progress", {"message": socket_message}, to=sid)

    worklet_prompt = worklet_gen_prompt_with_web_searches(
        json=search_data,
        worklet_data=worklet_data,
        links_data=links_data,
        count=count,
        custom_prompt=custom_prompt,
        count_string=count_string,
        domains=domains,
        keywords=keywords
    )

    if not is_client_connected(sid):
        print(f"Client {sid} is not connected. Skipping 2nd prompt generation. Exiting...")
        return

    # Prompting the LLM for worklet generation with web search results
    try:
        generated_worklets = await invoke_llm(worklet_prompt, model)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: LLM is not responding (after web search). Please try again."}, to=sid)
        return

    try:
        extracted_worklets = extract_dicts_smart(generated_worklets,False)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: Wrong output from LLM after web search. Please try again."}, to=sid)
        return

    return extracted_worklets
