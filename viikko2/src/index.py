import requests
from player import Player
from rich.console import Console
from rich.table import Table
import re

class PlayerReader:
    def __init__(self, url):
        self.url = url

    def get_players(self):
        response = requests.get(self.url).json()
        players = []

        for p in response:
            player = Player(
                name=p.get("name"),
                nationality=p.get("nationality"),
                team=p.get("team"),
                goals=p.get("goals"),
                assists=p.get("assists")
            )
            players.append(player)

        return players

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        players = self.reader.get_players()
        filtered = [player for player in players if player.nationality == nationality]
        filtered.sort(key=lambda p: p.name)
        return filtered


if __name__ == "__main__":
    pattern_season = r"^\d{4}-\d{2}$"
    season = input("Choose season: ")
    if not re.match(pattern_season, season):
        print("Selected season is invalid.")

    pattern_nationality = r"^[A-Z]{3}$"
    nationality = input("Choose nationality: ")
    if not re.match(pattern_nationality, nationality):
        print("Selected nationality is invalid.")

    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(f"{nationality}")

    console = Console()
    table = Table(title=f"Season {season} players from {players[0].nationality}")

    table.add_column("Released", justify="left")
    table.add_column("Teams", justify="left")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right")



    print(f"\n\n")

    for player in players:
        table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.goals + player.assists))

    console.print(table)