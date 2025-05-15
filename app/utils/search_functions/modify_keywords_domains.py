import asyncio
from app.socket import is_client_connected, sio

pending_responses = {}


@sio.on("topic_response")
async def handle_query_response(sid, data):
    if sid in pending_responses:
        pending_responses[sid].set_result(data)


async def get_approved_content(domains, keywords, sid: str):

    if not is_client_connected(sid):
        print(f"Client {sid} is not connected. Cannot proceed with query approval.")
        return [], []

    future = asyncio.get_event_loop().create_future()
    pending_responses[sid] = future

    await sio.emit("topic_approval", {"domains": domains, "keywords": keywords}, to=sid)

    try:
        response = await asyncio.wait_for(future, timeout=1800)  # 30 minutes timeout
        approved_domains = response.get("domains")
        approved_keywords = response.get("keywords")
    except asyncio.TimeoutError:
        approved_domains = {}
        approved_keywords = {}
    except Exception as e:
        print(f"An error occurred while waiting for response from client {sid}: {e}")
        approved_domains = {}
        approved_keywords = {}
    finally:
        pending_responses.pop(sid, None)

    final_domains = [
        domain
        for domain_list in approved_domains.values()
        for domain in domain_list
        if domain not in ["", " "]
    ]
    final_keywords = [
        keyword
        for keyword_list in approved_keywords.values()
        for keyword in keyword_list
        if keyword not in ["", " "]
    ]

    return final_domains, final_keywords
