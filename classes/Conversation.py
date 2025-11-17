from typing import List, Dict, TypedDict

class Message(TypedDict):
    player_password: str
    text: str

class Conversation:
    def __init__(
        self,
        player_1_password: str,
        player_2_password: str,
    ):
        self.player_1_password = player_1_password
        self.player_2_password = player_2_password
        self.conversation: List[Message] = []
