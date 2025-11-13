from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# connected WebSocket clients
clients = []

@app.get("/")
def home():
    return {"message": "WebSocket chat server running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # data = {"user": "1", "text": "Hello!"}
            for client in clients:
                await client.send_json(data)  # broadcast to everyone
    except WebSocketDisconnect:
        clients.remove(websocket)
