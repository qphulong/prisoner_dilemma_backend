class Player:
    def __init__(
        self,
        game_id: str,
        player_name: str,
        player_id: str,
        player_password: str
        ):
        self.game_id=game_id
        self.player_name = player_name
        self.player_id = player_id
        self.player_password = player_password