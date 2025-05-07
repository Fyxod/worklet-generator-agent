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

executor = ThreadPoolExecutor(max_workers=5)


async def generate_worklets(worklet_data, links_data, model, sid, custom_prompt, custom_topics):

    count = 10
    count_string = "ten"

    if not custom_topics:
        custom_topics = "Generative AI, Vision AI, Voice AI, On-device AI, Classical ML, IoT"
    if not custom_prompt:
        custom_prompt = " no custom prompt was provide by user please continue"

  

    loop = asyncio.get_running_loop()
    # New order
    # keywords -> websearch -> frontend ->  update keywords and web search -> do websearch -> Final worklet generation prompt 
    
    # key words
    keyword_prompt =keywords_from_worklets_custom_prompt(custom_prompt,worklet_data,links_data)
    try:
        keywords=await invoke_llm(prompt=keyword_prompt,model=model)
    except Exception as e:
        await sio.emit("error", {"message": "ERROR: LLM is not responding. Please try again."}, to=sid)
        return
    
    try:
        keywords = extract_dicts_smart(keywords)
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
        custom_topics=custom_topics,
        count_string=count_string,
    )


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
        await sio.emit("progress", {"message": "LLM requested for web search..."}, to=sid)
        await asyncio.sleep(0.7)
        await sio.emit("progress", {"message": "Searching the web..."}, to=sid)

        try:
            s = await loop.run_in_executor(executor, search, extracted_worklets["search"], 10)
        except Exception as e:
            await sio.emit("error", {"message": "ERROR: Web search failed. Please try again."}, to=sid)
            return

        await sio.emit("progress", {"message": "Generating worklets with web search results..."}, to=sid)

        if not custom_topics:
            custom_topics = "Generative AI, Vision AI, Voice AI, On-device AI, Classical ML, IoT. Cross-domain intersections are encouraged"
        if not custom_prompt:
            custom_prompt = " no custon prompt was provide by user please continue"

        prompt = worklet_gen_prompt_with_web_searches(
            json=s,
            worklet_data=worklet_data,
            links_data=links_data,
            count=count,
            custom_prompt=custom_prompt,
            custom_topics=custom_topics,
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
