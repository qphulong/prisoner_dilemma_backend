from fastapi import WebSocket
from typing import Dict, Optional

class WebSocketManager:
    def __init__(self):
        self.host_connection: Optional[WebSocket] = None
        self.players_connections: Dict[str, WebSocket] = {}

    async def connect_host(self, websocket: WebSocket):
        # Remove await websocket.accept() ← THIS WAS THE BUG
        self.host_connection = websocket
        print("[WS] Host registered in manager")

        # Safe to send now (accept already happened in main.py)
        await websocket.send_json({
            "type": "current_players",
            "players": list(self.players_connections.keys())
        })

    async def connect_player(self, websocket: WebSocket, player_id: str):
        # Remove accept() here too
        self.players_connections[player_id] = websocket
        print(f"[WS] Player {player_id} connected")

        if self.host_connection:
            await self.host_connection.send_json({
                "type": "player_joined",
                "player_id": player_id
            })

    async def disconnect(self, websocket: WebSocket):
        if self.host_connection == websocket:
            self.host_connection = None
            print("[WS] Host disconnected")
            return

        player_id = next((pid for pid, ws in self.players_connections.items() if ws == websocket), None)
        if player_id:
            del self.players_connections[player_id]
            print(f"[WS] Player {player_id} left")
            if self.host_connection:
                await self.host_connection.send_json({
                    "type": "player_left",
                    "player_id": player_id
                })

    async def broadcast_to_players(self, msg: dict):
        for ws in self.players_connections.values():
            try:
                await ws.send_json(msg)
            except:
                pass  # will be cleaned on next disconnect