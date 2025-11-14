import random
from classes.game import Game
import string

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
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
            if code not in self.games:
                return code

    def create_game(self) -> str:
        """Create a new game and return its ID."""
        if len(self.games) >= self.MAX_GAMES:
            raise Exception("Maximum number of games reached")

        game_id = self._generate_game_id()
        self.games[game_id] = Game(game_id)
        return game_id

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
