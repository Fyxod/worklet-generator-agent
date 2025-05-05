from app.utils.llm_response_parser import extract_dicts_smart
from app.llm import invoke_llm
from app.utils.prompt_templates import worklet_gen_prompt,worklet_gen_prompt_with_web_searches   # all the prompts used in this projects were moved to prompt_templates
from app.socket import sio
from app.utils.search_functions.search import search 
from app.socket import is_client_connected
import asyncio

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)

async def generate_worklets(worklet_data, linksData, model, sid, custom_prompt, custom_topics):
    count = 6
    count_string = "six"
    if model == "gemini-flash-2.0":
        count = 5
        count_string = "five"
    if not custom_topics:
        custom_topics = "Generative AI, Vision AI, Voice AI, On-device AI, Classical ML, IoT. Cross-domain intersections are encouraged"
    if not custom_prompt:
        custom_prompt = " no custon prompt was provide by user please continue"
    prompt_template = worklet_gen_prompt()
    prompt = prompt_template.format(
        worklet_data=worklet_data,
        linksData=linksData,
        count=count,
        custom_prompt=custom_prompt,
        custom_topics=custom_topics,
        count_string=count_string,
    )

    try:
        with open("saved_prompt1.txt", "w", encoding="utf-8") as file:
            file.write(prompt)
    except Exception as e:
        print(f"Failed to write prompt to file. Error: {e}")

    loop = asyncio.get_running_loop()

    try:
        generated_worklets = await invoke_llm(prompt, model)
    except Exception as e:
        print("Error in generating worklets:", e)
        await sio.emit("error", {"message": "ERROR: LLM is not responding. Please try again."}, to=sid)
        return

    try:
        extracted_worklets = extract_dicts_smart(generated_worklets)
    except Exception as e:
        print("Error in extracting worklets:", e)
        await sio.emit("error", {"message": "ERROR: Wrong output returned by LLM. Please try again."}, to=sid)
        return

    print("Extracted worklets:", extracted_worklets)

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
            print("Error in web search:", e)
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
        print("\n\n","--------this is the biggest prompt------"*10,"\n\n",prompt)

        if not is_client_connected(sid):
            print(f"Client {sid} is not connected. Skipping 2nd prompt generation. Exiting...")
            return

        try:
            with open("saved_prompt2.txt", "w", encoding="utf-8") as file:
                file.write(prompt)
        except Exception as e:
            print(f"Failed to write prompt to file. Error: {e}")

        try:
            generated_worklets = await invoke_llm(prompt, model)
        except Exception as e:
            print("Error in generating worklets (with web):", e)
            await sio.emit("error", {"message": "ERROR: LLM is not responding (after web search). Please try again."}, to=sid)
            return

        try:
            extracted_worklets = extract_dicts_smart(generated_worklets)
        except Exception as e:
            print("Error in extracting worklets (with web):", e)
            await sio.emit("error", {"message": "ERROR: Wrong output from LLM after web search. Please try again."}, to=sid)
            return

    return extracted_worklets
