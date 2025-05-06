import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.llm import invoke_llm
from app.socket import is_client_connected, sio
from app.utils.llm_response_parser import extract_dicts_smart
from app.utils.prompt_templates import worklet_gen_prompt, worklet_gen_prompt_with_web_searches
from app.utils.search_functions.search import search
import random

executor = ThreadPoolExecutor(max_workers=5)

async def generate_worklets(worklet_data, linksData, model, sid, custom_prompt, custom_topics):
    """
    Asynchronously generates worklets based on provided data, model, and optional customizations.
    This function interacts with a language model (LLM) to generate worklets using the provided 
    data and parameters. It also supports web search integration if requested by the LLM.
    Args:
        worklet_data (str): The primary data to be used for generating worklets.
        linksData (str): Additional link-related data to be included in the prompt.
        model (str): The name of the LLM model to be used (e.g., "gemini-flash-2.0").
        sid (str): The session ID of the client, used for emitting progress and error messages.
        custom_prompt (str): A custom prompt provided by the user. Defaults to a fallback message if not provided.
        custom_topics (str): Custom topics provided by the user. Defaults to a predefined set of topics if not provided.
    Returns:
        dict: A dictionary containing the extracted worklets, or None if an error occurs.
    Raises:
        Exception: Emits error messages to the client in case of issues with LLM invocation, 
                   output extraction, or web search.
    Notes:
        - If the LLM requests a web search, the function performs the search and re-generates 
          worklets using the search results.
        - The function ensures that the client is connected before performing operations that 
          require client interaction.
        - Emits progress updates and error messages to the client via Socket.IO.
    """

    count = 6
    count_string = "six"
    
    if model == "gemini-flash-2.0":
        count = 5
        count_string = "five"
        
    if not custom_topics:
        custom_topics = "Generative AI, Vision AI, Voice AI, On-device AI, Classical ML, IoT. Cross-domain intersections are encouraged"
    if not custom_prompt:
        custom_prompt = " no custom prompt was provide by user please continue"
        
    prompt_template = worklet_gen_prompt()
    
    prompt = prompt_template.format(
        worklet_data=worklet_data,
        linksData=linksData,
        count=count,
        custom_prompt=custom_prompt,
        custom_topics=custom_topics,
        count_string=count_string,
    )


    random_int = random.randint(1, 1000)
    
    try:
        with open(f"saved_prompt1_{random_int}.txt", "w", encoding="utf-8") as file:
            file.write(prompt)
    except Exception as e:
        print(f"Failed to write prompt to file. Error: {e}")

    loop = asyncio.get_running_loop()

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
            linksData=linksData,
            count=count,
            custom_prompt=custom_prompt,
            custom_topics=custom_topics,
            count_string=count_string,
        )

        if not is_client_connected(sid):
            print(f"Client {sid} is not connected. Skipping 2nd prompt generation. Exiting...")
            return

        try:
            with open(f"saved_prompt2_{random_int}.txt", "w", encoding="utf-8") as file:
                file.write(prompt)
        except Exception as e:
            print(f"Failed to write prompt to file. Error: {e}")

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
