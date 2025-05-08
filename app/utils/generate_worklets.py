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

    count = 10
    count_string = "ten"

    # if not custom_topics:
    #     custom_topics = "Generative AI, Vision AI, Voice AI, On-device AI, Classical ML, IoT"
    if not custom_prompt:
        custom_prompt = " no custom prompt was provide by user please continue"

    domains = {
        "worklet_domains":[
            "Generative AI",
            "Vision AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            ],
        "link_domains":[
            "link 1",
            "link 2",
            "link 3",],
        "custom_prompt_domains":[
            "custom prompt 1",
            "custom prompt 2",
            "custom prompt 3",],
    }
    
    keywords =  {
        "worklet_keywords":[
            "Generative AI",
            "Vision AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            "Voice AI",
            ],
        "link_keywords":[
            "link 1",
            "link 2",
            "link 3",],
        "custom_prompt_keywords":[
            "custom prompt 1",
            "custom prompt 2",
            "custom prompt 3",],
    }
    
    domains, keywords = await get_approved_content(domains=domains, keywords=keywords, sid=sid)
    return;
    loop = asyncio.get_running_loop()
    # New order
    # keywords -> websearch -> frontend ->  update keywords and web search -> do websearch -> Final worklet generation prompt 
    await sio.emit("progress", {"message": "Extracting keywords..."}, to=sid)
    
    # key words
    keyword_domain_prompt =keywords_from_worklets_custom_prompt(custom_prompt,worklet_data,links_data)
    try:
        topics=await invoke_llm(prompt=keyword_domain_prompt,model=model)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: LLM is not responding. Please try again."}, to=sid)
        return
    
    try:
        topics = extract_dicts_smart(topics)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: Wrong output returned by LLM. Please try again."}, to=sid)
        return    
#------------------------------------------------------------------------------------------------------------
    prompt_template = web_search_prompt()

    prompt = prompt_template.format(
        worklet_data=worklet_data,
        links_data=links_data,
        count=count,
        custom_prompt=custom_prompt,
        # custom_topics=custom_topics,
        count_string=count_string,
    )

    await sio.emit("progress", {"message": "Asking LLM for Web queries..."}, to=sid)
    
    try:
        generated_worklets = await invoke_llm(prompt, model)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: LLM is not responding. Please try again."}, to=sid)
        return

    try:
        extracted_worklets = extract_dicts_smart(generated_worklets)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: Wrong output returned by LLM. Please try again."}, to=sid)
        return

    if not is_client_connected(sid):
        print(f"Client {sid} is not connected. Skipping web search. Exiting...")
        return

    if extracted_worklets.get("websearch"):
        show_message = "LLM requested for web search. Queries: "
        queries = extracted_worklets["websearch"]
        
    else:
        show_message = "LLM refused web search. Add any queries if needed: "
        queries = []
        
    queries = await get_approved_queries(queries=queries, sid=sid, show_message=show_message)

    # await sio.emit("progress", {"message": "LLM requested for web search..."}, to=sid)
    # await asyncio.sleep(0.7)
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
    
    return;
    
    socket_message = "Generating worklets..."
    if queries != []:
        await sio.emit("progress", {"message": "Searching the web..."}, to=sid)

        try:
            search_data = await loop.run_in_executor(executor, search, extracted_worklets["search"], 10)
        except Exception as e:
            await sio.emit("error", {"message": "ERROR: Web search failed. Please try again."}, to=sid)
            return
        socket_message = "Generating worklets with web search results..."

    # keywords = 

    await sio.emit("progress", {"message": socket_message}, to=sid)

    prompt = worklet_gen_prompt_with_web_searches(
        json=search_data,
        worklet_data=worklet_data,
        links_data=links_data,
        count=count,
        custom_prompt=custom_prompt,
        # custom_topics=custom_topics,
        count_string=count_string,
    )

    if not is_client_connected(sid):
        print(f"Client {sid} is not connected. Skipping 2nd prompt generation. Exiting...")
        return

    try:
        generated_worklets = await invoke_llm(prompt, model)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: LLM is not responding (after web search). Please try again."}, to=sid)
        return

    try:
        extracted_worklets = extract_dicts_smart(generated_worklets)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: Wrong output from LLM after web search. Please try again."}, to=sid)
        return

    return extracted_worklets
