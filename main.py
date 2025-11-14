from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from classes.games_manager import PrisonerDilemmaGamesManager

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
def create_game():
    try:
        game_id = games_manager.create_game()
        return {"game_id": game_id}
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
