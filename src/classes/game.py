class Game:
    def __init__(self, team_stats_1, team_stats_2):
        self.team_stats_1 = team_stats_1
        self.team_stats_2 = team_stats_2
        self.id = int(team_stats_1["GAME_ID"])
        self.scoreline = (
            self.team_stats_1["TEAM_ABBREVIATION"]
            + " "
            + str(self.team_stats_1["PTS"])
            + " - "
            + str(self.team_stats_2["PTS"])
            + " "
            + self.team_stats_2["TEAM_ABBREVIATION"]
        )

    def __str__(self):
        return f"{self.id}: {self.scoreline}"
