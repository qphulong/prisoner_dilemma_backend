from fastapi import FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from classes.GamesManager import PrisonerDilemmaGamesManager
from models.GameConfig import GameConfigModel
from models.HostAuth import HostAuth
from models.PlayerRegister import PlayerRegisterModel
from classes.Player import Player
import json
import asyncio

app = FastAPI(title="Prisoner's Dilemma API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

loop = None

@app.on_event("startup")
async def startup_event():
    global loop
    loop = asyncio.get_running_loop()
    print(f"[STARTUP] Event loop stored: {loop}")

games_manager = PrisonerDilemmaGamesManager()

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    game = games_manager.games.get(game_id)
    if not game:
        await websocket.close(code=1011, reason="Game not found")
        return

    ws_manager = game.web_socket_manager

    await websocket.accept()
    print(f"[WS] Connection accepted for game {game_id}")

    try:
        first_msg = await websocket.receive_json()
    except:
        await websocket.close(code=1008)
        return

    role = first_msg.get("role")

    if role == "host":
        await ws_manager.connect_host(websocket)

    elif role == "player":
        player_id = first_msg.get("player_id")
        player_name = first_msg.get("player_name")
        # if not player_id or player_id not in game.players:
        #     await websocket.close(code=1008)
        #     return
        await ws_manager.connect_player(websocket, player_id, player_name)

    else:
        await websocket.close(code=1008)
        return

    # Main loop
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)

@app.get("/")
def home():
    return {"message": "Prisoner's Dilemma backend is running."}

@app.post("/create-game")
def create_game(config: GameConfigModel):
    try:
        game_id, game_password = games_manager.create_game(config)
        return {
            "game_id": game_id,
            "game_password": game_password
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@app.get("/get-all-games-id")
def get_all_game_id():
    try:
        resutls = games_manager.list_all_games_id()
        return {"results": resutls}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# DO NOT Release
@app.delete("/remove-all-games")
def remove_all_games():
    try:
        games_manager.remove_all_games()
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.patch("/close-game-entry")
def close_game_entry(hostAuth: HostAuth):
    """
    Host API to close game entry.
    After this, no additional players can join.
    """
    try:
        game = games_manager.host_auth(
            game_id=hostAuth.game_id,
            game_password=hostAuth.game_password
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid game password"
        )

    success = game.close_entry(hostAuth)
    if not success:
        return {"status": "fail"}

    return {"status": "success"}
    
@app.post("/register-player")
def register_player(player_register_model: PlayerRegisterModel):
    # 1. Game not found → 404
    game = games_manager.get_game_by_id(player_register_model.game_id)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {player_register_model.game_id} not found"
        )

    # 2. Player ID already taken → 400
    if any(p.player_id == player_register_model.player_id for p in game.players.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Player ID '{player_register_model.player_id}' existed."
        )

    # Game is closed for new players?
    if not game.game_config.allow_player_to_join:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Host has closed game entry"
        )

    # Create and register the new player (password generated inside Game)
    new_player = Player(
        game_id=player_register_model.game_id,
        player_name=player_register_model.player_name,
        player_id=player_register_model.player_id,
        player_password=None  # will be set by Game.register_new_player
    )

    player_password = game.register_new_player(new_player)

    return {"player_password": player_password}
    
# DO NOT Release
@app.post("/creat-sample-data")
def create_sample_data():
    try:
        new_game_id, new_game_password = games_manager._create_sample_data()
        return {
            "game_id": new_game_id,
            "game_password": new_game_password,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/list-all-players-by-game-id")
def list_all_players_by_game_id(hostAuth: HostAuth):
    """This should be a GET but GET does not have a body and i am lazy this part"""
    try:
        game = games_manager.host_auth(
            game_id=hostAuth.game_id,
            game_password=hostAuth.game_password
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid game password"
        )
    
    players_list = [
        {"player_name": player.player_name, "player_id": player.player_id}
        for player in game.players.values()
    ]
    return {"players": players_list}
    
