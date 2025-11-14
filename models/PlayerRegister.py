from pydantic import BaseModel

class PlayerRegisterModel(BaseModel):
    game_id: str
    player_name: str
    player_id: str