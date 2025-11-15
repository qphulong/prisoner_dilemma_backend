from typing import Optional
from classes.GameConfig import GameConfig
from models.HostAuth import HostAuth
from classes.Player import Player
from utils.utils_func import generate_4_char_code

class Game:
    """
    A Game class, the host able to control this class
    """

    def __init__(
        self, 
        game_id: str,
        game_config: GameConfig,
        game_password: str,
        ):
        self.game_id = game_id
        self.game_config = game_config
        self.game_password = game_password # simple password for host to orchestra the game
        
        self.players = {}
        
    def close_entry(self, auth: HostAuth) -> bool:
        """
        Host closes the game entry so no new players can join.

        Returns:
            True if closed successfully, False if authentication failed.
        """
        if auth.game_id != self.game_id or auth.game_password != self.game_password:
            return False

        self.game_config.allow_player_to_join = False
        return True
    
    def register_new_player(self,new_player: Player):
        """
        Register new player, force to try if password existed.
        """
        if not self.game_config.allow_player_to_join: # cannot enter closed game
            return False
        while True:
            player_password = generate_4_char_code()
            if player_password not in self.players:
                break
        new_player.player_password = player_password
        self.players[new_player.player_password] = new_player
        return True
