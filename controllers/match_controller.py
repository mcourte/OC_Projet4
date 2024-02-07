class MatchController:
    def __init__(self):
        pass

    def update_player_scores(player, match_result):
        player_score = player.get("score_tournament")
        player_score_match = match_result.get(player["player_ID"], 0)
        player["score_tournament "] = player_score + player_score_match
