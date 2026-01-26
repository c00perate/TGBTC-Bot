import csv
from collections import defaultdict
from typing import Optional, List, Dict

class CharacterDatabase:
    
    def __init__(self):
        self.characters: List[Dict] = []
        self.char_index: Dict[tuple, List[Dict]] = defaultdict(list)
        self.char_name: Dict[str, List[Dict]] = defaultdict(list)
        self.cells: List[Dict] = []
        self.cells_list: Dict[tuple, List[Dict]] = defaultdict(list)
        self.cells_index: Dict[tuple, List[Dict]] = defaultdict(list)
        self.rankings: Dict[str, List[Dict]] = {}
        self._load_characters('characters.csv')
        self._load_cells('cells.csv')
        self._build_character_index()
        self._build_cells_index()
        self._calculate_rankings()
    
    def _load_characters(self, csv_path: str):
        int_fields = ['Base CP', '3x Cell CP', '4x Cell CP', 'Base ATK', 'Base DEF', 'Base HP']
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                for field in int_fields:
                    row[field] = int(row[field])
                row['Nicknames'] = str(row.get('Nicknames', ''))
                self.characters.append(row)
    
    def _build_character_index(self):
        for char in self.characters:
            character_name = char['Character'].lower()
            attribute = char['Attribute']
            
            key = (character_name, attribute)
            self.char_index[key].append(char)

            name_parts = character_name.split()
            if len(name_parts) == 1:
                self.char_name[character_name].append(char)
            
            if len(name_parts) > 1:
                for part in name_parts:
                    self.char_index[(part, attribute)].append(char)
                    self.char_name[part].append(char)  

            if char['Nicknames']:
                for nickname in char['Nicknames'].lower().split(';'):
                    nickname = nickname.strip()
                    if nickname:
                        self.char_index[(nickname, attribute)].append(char)
                        self.char_name[nickname].append(char)

    def _load_cells(self, csv_path: str):
        int_fields = ['Base Stat']
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                for field in int_fields:
                    row[field] = int(row[field])
                row['Nicknames'] = str(row.get('Nicknames', ''))
                self.cells.append(row)

    def _build_cells_index(self):
        for cell in self.cells:
            cell_name = cell['Character'].lower()
            attribute = cell['Attribute']
            cellType = cell['Type']
            
            key = (cell_name, attribute, cellType)
            key2 = (cell_name, attribute) 
            self.cells_index[key].append(cell)

            name_parts = cell_name.split()

            if len(name_parts) == 1:
                self.cells_list[key2].append(cell) 
            
            if len(name_parts) > 1:
                for part in name_parts:
                    self.cells_index[(part, attribute, cellType)].append(cell)
                    self.cells_list[(part, attribute)].append(cell)

            if cell['Nicknames']:
                for nickname in cell['Nicknames'].lower().split(';'):
                    nickname = nickname.strip()
                    if nickname:
                        self.cells_index[(nickname, attribute, cellType)].append(cell)
                        self.cells_list[(nickname, attribute)].append(cell)
    
    def _calculate_rankings(self):
        stats = ['Base CP', 'Base ATK', 'Base DEF', 'Base HP', '3x Cell CP', '4x Cell CP']
        
        for stat in stats:
            sorted_chars = sorted(self.characters, key=lambda x: x[stat], reverse=True)
            self.rankings[stat] = sorted_chars
            for rank, char in enumerate(sorted_chars, start=1):
                char[f'{stat}_rank'] = rank
    
    #for teams.py, to display title
    def find_character(self, name: str, attribute: str, title: Optional[str] = None) -> Optional[Dict]:
        key = (name.lower(), attribute.upper())
        matches = self.char_index.get(key, [])
        
        if title:
            title_lower = title.lower()
            for match in matches:
                if match['Title'].lower() == title_lower:
                    return match
        
        return matches[0] if matches else None
    
    def find_characters(self, name: str, attribute: str) -> List[Dict]:
        key = (name.lower(), attribute.upper())
        return self.char_index.get(key, [])

    def find_name(self, name: str) -> List[Dict]:
        return self.char_name.get(name.lower(), [])
    
    def find_cells(self, name: str, attribute: str, cellType: str) -> List[Dict]:
        key = (name.lower(), attribute.upper(), cellType.upper())
        return self.cells_index.get(key, [])
    
    def find_cells_list(self, name: str, attribute: str) -> List[Dict]:
        key = (name.lower(), attribute.upper())
        return self.cells_list.get(key, [])
    
    def get_top_characters(self, stat: str, limit: int) -> List[Dict]:
        return self.rankings.get(stat, [])[:limit]
    