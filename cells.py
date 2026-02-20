import csv
from collections import defaultdict
from typing import List, Dict

class CellsDatabase:

    def __init__(self):
        self.cells: List[Dict] = []
        self.cells_list: Dict[tuple, List[Dict]] = defaultdict(list)
        self.cells_index: Dict[tuple, List[Dict]] = defaultdict(list)
        self._load_cells('csv/cells.csv')
        self._build_cells_index()
    

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
    

    def find_cells(self, name: str, attribute: str, cellType: str) -> List[Dict]:
        key = (name.lower(), attribute.upper(), cellType.upper())
        return self.cells_index.get(key, [])
    
    
    def find_cells_list(self, name: str, attribute: str) -> List[Dict]:
        key = (name.lower(), attribute.upper())
        return self.cells_list.get(key, [])
    