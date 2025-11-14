from pydantic import BaseModel

class HostAuth(BaseModel):
    game_id: str
    game_password: str