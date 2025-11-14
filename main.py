from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from classes.GamesManager import PrisonerDilemmaGamesManager
from models.GameConfig import GameConfigModel
from models.HostAuth import HostAuth
from models.PlayerRegister import PlayerRegisterModel
from classes.Player import Player

app = FastAPI(title="Prisoner's Dilemma API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

games_manager = PrisonerDilemmaGamesManager()

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

    game = games_manager.get_game_by_id(hostAuth.game_id)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )

    # 2. Attempt to close entry → any failure returns fail
    success = game.close_entry(hostAuth)

    if not success:
        return {"status": "fail"}

    return {"status": "success"}
    
@app.post("/register-player")
def register_player(player_register_model: PlayerRegisterModel):
    game = games_manager.get_game_by_id(player_register_model.game_id)
    
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {player_register_model.game_id} not found"
        )
    
    new_player = Player(
        game_id=player_register_model.game_id,
        player_name=player_register_model.player_name,
        player_id=player_register_model.player_id,
        player_password="temp"
    )
    
    register_status = game.register_new_player(new_player)
    
    if register_status:
        return {
            "player_password": new_player.player_password
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register the player"
        )
    
