from pydantic import BaseModel

class GameConfigModel(BaseModel):
    points_both_cooperate: int = 7
    points_defect_against_cooperate: int = 10
    points_cooperate_against_defect: int = 0
    points_both_defect: int = 1

    allow_chat: bool = True
    anonymous_play: bool = True
    round_time_limit: int = 60
    number_of_rounds: int = 10
    show_round_count: bool = False
