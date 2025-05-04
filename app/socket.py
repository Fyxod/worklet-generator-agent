import socketio
import asyncio

active_connections = set()
# Create the Socket.IO server
# sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    ping_timeout=400,  # 5 minutes timeout
    ping_interval=20,  # keep sending ping every 20s
)

# Dictionary to track heartbeat tasks for each client
heartbeat_tasks = {}

@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")
    active_connections.add(sid)

    async def send_heartbeat():
        try:
            while True:
                await sio.emit('heartbeat', {'status': 'processing...'}, to=sid)
                await asyncio.sleep(20)  # send heartbeat every 20 seconds
        except asyncio.CancelledError:
            pass  # when cancelled, just exit

    # Start heartbeat task for this client
    heartbeat_tasks[sid] = asyncio.create_task(send_heartbeat())

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")
    active_connections.discard(sid)
    # Stop heartbeat task when client disconnects
    task = heartbeat_tasks.pop(sid, None)
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

def is_client_connected(sid):
    """Check if a client is connected."""
    return sid in active_connections