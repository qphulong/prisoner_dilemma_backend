from typing import Optional, Dict
from classes.GameConfig import GameConfig
from models.HostAuth import HostAuth
from classes.Player import Player
from classes.WebSocketManager import WebSocketManager
from utils.utils_func import generate_4_char_code
import time

class Game:
    """
    A Game class, the host able to control this class
    """
    INACTIVITY_TIMEOUT = 300 
    
    def __init__(
        self, 
        game_id: str,
        game_config: GameConfig,
        game_password: str,
        ):
        self.game_id = game_id
        self.game_config = game_config
        self.game_password = game_password
        
        self.players: Dict[str, Player] = {}
        
        self.last_update_ts = time.time()
        
        self.current_round = 1
        
        self.web_socket_manager = WebSocketManager()
        
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
    
    def touch(self):
        """IMPORTANT: Call this every time update the Game object"""
        self.last_update_ts = time.time()

    def is_expired(self) -> bool:
        """Check if the game should be auto-removed."""
        return (time.time() - self.last_update_ts) > self.INACTIVITY_TIMEOUT
