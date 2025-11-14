class GameConfig:
    def __init__(
        self,
        points_both_cooperate: int = 7,
        points_defect_against_cooperate: int = 10,
        points_cooperate_against_defect: int = 0,
        points_both_defect: int = 1,
        allow_chat: bool = True,
        anonymous_play: bool = True,
        round_time_limit: int = 60,
        number_of_rounds: int = 10,
        show_round_count: bool = False,
        allow_player_to_join: bool = True
    ):
        self.points_both_cooperate = points_both_cooperate
        self.points_defect_against_cooperate = points_defect_against_cooperate
        self.points_cooperate_against_defect = points_cooperate_against_defect
        self.points_both_defect = points_both_defect

        self.allow_chat = allow_chat
        self.anonymous_play = anonymous_play
        self.round_time_limit = round_time_limit
        self.number_of_rounds = number_of_rounds
        self.show_round_count = show_round_count
        self.allow_player_to_join = allow_player_to_join
