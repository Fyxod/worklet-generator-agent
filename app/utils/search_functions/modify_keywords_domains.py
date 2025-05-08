import asyncio
from app.socket import is_client_connected, sio

pending_responses = {}

@sio.on('topic_response')
async def handle_query_response(sid, data):
    print(f"Received query response: {data}")
    print("printing something", sid)
    if sid in pending_responses:
        pending_responses[sid].set_result(data)

async def get_approved_content(domains, keywords, sid: str):
    # if not is_client_connected(sid):
    #     print(f"Client {sid} is not connected. Cannot proceed with query approval.")
    #     return [], [] modify this to return a obined list of all

    future = asyncio.get_event_loop().create_future()
    pending_responses[sid] = future

    print(f"Sending domains and keywords to client {sid} for approval: Domains: {domains}, Keywords: {keywords}")

    await sio.emit("topic_approval", {"domains": domains, "keywords": keywords}, to=sid)

    try:
        response = await asyncio.wait_for(future, timeout=600)  
        approved_domains = response.get("domains")
        approved_keywords = response.get("keywords")
        print(f"Received approved domains and keywords from client {sid}: Domains: {approved_domains}, Keywords: {approved_keywords}")
    except asyncio.TimeoutError:
        print(f"Timeout waiting for response from client {sid}")
        approved_domains = {}
        approved_keywords = {}
    finally:
        pending_responses.pop(sid, None)

    final_domains = [
        domain for domain_list in approved_domains.values() for domain in domain_list
    ]