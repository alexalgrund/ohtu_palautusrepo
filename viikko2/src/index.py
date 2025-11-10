import re
import requests
from rich.console import Console
from rich.table import Table
from player import Player


class PlayerReader:
    def __init__(self, url: str):
        self.url = url

    def get_players(self) -> list[Player]:
        response = requests.get(self.url, timeout=10).json()
        players_list = []

        for p in response:
            pl = Player(
                name=p.get("name"),
                nationality=p.get("nationality"),
                team=p.get("team"),
                goals=p.get("goals"),
                assists=p.get("assists")
            )
            players_list.append(pl)

        return players_list


class PlayerStats:
    def __init__(self, reader: PlayerReader):
        self.reader = reader

    def top_scorers_by_nationality(self, nation: str) -> list[Player]:
        all_players = self.reader.get_players()
        filtered = [p for p in all_players if p.nationality == nation]
        filtered.sort(key=lambda p: p.name)
        return filtered


if __name__ == "__main__":
    PATTERN_SEASON = r"^\d{4}-\d{2}$"
    selected_season = input("Choose season: ")
    if not re.match(PATTERN_SEASON, selected_season):
        print("Selected season is invalid.")

    PATTERN_NATIONALITY = r"^[A-Z]{3}$"
    selected_nationality = input("Choose nationality: ")
    if not re.match(PATTERN_NATIONALITY, selected_nationality):
        print("Selected nationality is invalid.")

    reader_instance = PlayerReader(
        f"https://studies.cs.helsinki.fi/nhlstats/{selected_season}/players"
    )
    stats_instance = PlayerStats(reader_instance)
    nation_players = stats_instance.top_scorers_by_nationality(selected_nationality)

    console = Console()
    table = Table(title=f"Season {selected_season} players from {nation_players[0].nationality}")

    table.add_column("Released", justify="left")
    table.add_column("Teams", justify="left")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right")

    for pl in nation_players:
        table.add_row(
            pl.name,
            pl.team,
            str(pl.goals),
            str(pl.assists),
            str(pl.goals + pl.assists)
        )

    console.print(table)
