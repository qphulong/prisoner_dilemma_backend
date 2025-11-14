import random
from classes.Game import Game
from classes.GameConfig import GameConfig
from models.GameConfig import GameConfigModel
import string
from utils.utils_func import generate_4_char_code

class PrisonerDilemmaGamesManager:
    """
    Singleton manager that tracks all active games in memory.
    """

    _instance = None
    MAX_GAMES = 5
    games = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.games = {}
        return cls._instance

    def _generate_game_id(self) -> str:
        """Generate a unique 4-digit game code."""
        while True:
            code = generate_4_char_code()
            if code not in self.games:
                return code

    def create_game(self, game_config: GameConfigModel) -> tuple[str, str]:
        """Create a new game and return (game_id, game_password)."""
        if len(self.games) >= self.MAX_GAMES:
            raise Exception("Maximum number of games reached")

        game_id = self._generate_game_id()
        game_password = generate_4_char_code()
        
        new_game_config = GameConfig(
            points_both_cooperate = game_config.points_both_cooperate,
            points_defect_against_cooperate = game_config.points_defect_against_cooperate,
            points_cooperate_against_defect = game_config.points_cooperate_against_defect,
            points_both_defect = game_config.points_both_defect,
            allow_chat = game_config.allow_chat,
            anonymous_play = game_config.anonymous_play,
            round_time_limit = game_config.round_time_limit,
            number_of_rounds = game_config.number_of_rounds,
            show_round_count = game_config.show_round_count,
        )

        self.games[game_id] = Game(
            game_id=game_id,
            game_config=new_game_config,
            game_password=game_password,
        )

        return game_id, game_password

    def get_game_by_id(self, game_id: str) -> Game:
        if game_id not in self.games:
            raise KeyError(f"Game {game_id} not found")
        return self.games[game_id]

    def remove_game_by_id(self, game_id: str):
        """Remove a game from memory."""
        if game_id in self.games:
            del self.games[game_id]
            
    def list_all_games_id(self) -> list[str]:
        return list(self.games.keys())
    
    def remove_all_games(self):
        self.games.clear()
