import asyncio
from app.socket import is_client_connected, sio

pending_responses = {}

@sio.on('domain_response')
async def handle_query_response(something, data):
    print(f"Received query response: {data}")
    print("printing something", something)
    sid = data.get("sid")
    if sid in pending_responses:
        pending_responses[sid].set_result(data)

async def get_approved_content(domains: list, keywords: list, sid: str):
    if not is_client_connected(sid):
        print(f"Client {sid} is not connected. Cannot proceed with query approval.")
        return []

    future = asyncio.get_event_loop().create_future()
    pending_responses[sid] = future

    print(f"Sending queries to client {sid} for approval: {queries}")

    await sio.emit("query_approval", {"queries": queries}, to=sid)

    try:
        response = await asyncio.wait_for(future, timeout=600)  
        approved_queries = response.get("queries", [])
        print(f"Received approved queries from client {sid}: {approved_queries}")
    except asyncio.TimeoutError:
        print(f"Timeout waiting for response from client {sid}")
        approved_queries = []
    finally:
        pending_responses.pop(sid, None)

    return approved_queries
