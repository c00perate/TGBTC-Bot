import csv
from typing import List, Dict

class TeamDatabase:
    
    def __init__(self, csv_path: str = 'csv/teams.csv'):
        self.teams: List[Dict] = []
        self._load_teams(csv_path)
    

    def _load_teams(self, csv_path: str):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.teams = list(reader)
    
    
    def get_teams_by_faction(self, faction: str) -> List[Dict]:
        faction_lower = faction.lower()
        return [team for team in self.teams if team['faction'].lower() == faction_lower]
