import csv
from collections import defaultdict
from typing import Optional, List, Dict
from discord.ui import View, Button
from embeds import create_character_embed
import discord


class CharacterDatabase:
    
    def __init__(self, csv_path: str = 'characters.csv'):
        self.characters: List[Dict] = []
        self.char_index: Dict[tuple, List[Dict]] = defaultdict(list)
        self.char_name: Dict[str, List[Dict]] = defaultdict(list)
        self.rankings: Dict[str, List[Dict]] = {}
        self._load_characters(csv_path)
        self._build_index()
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
    
    def _build_index(self):
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
    
    def _calculate_rankings(self):
        stats = ['Base CP', 'Base ATK', 'Base DEF', 'Base HP', '3x Cell CP', '4x Cell CP']
        
        for stat in stats:
            sorted_chars = sorted(self.characters, key=lambda x: x[stat], reverse=True)
            self.rankings[stat] = sorted_chars
            for rank, char in enumerate(sorted_chars, start=1):
                char[f'{stat}_rank'] = rank
    
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
    
    def get_top_characters(self, stat: str, limit: int = 10) -> List[Dict]:
        return self.rankings.get(stat, [])[:limit]
    

class CharacterPaginator(View):
    def __init__(self, matches: List[Dict], timeout=180):
        super().__init__(timeout=timeout)
        self.matches = matches
        self.current_index = 0
        self.message = None
        
        # Disable previous button on first page
        self.update_buttons()
    
    def update_buttons(self):
        """Enable/disable buttons based on current page."""
        # Disable previous if on first page
        self.children[0].disabled = (self.current_index == 0)
        # Disable next if on last page
        self.children[1].disabled = (self.current_index == len(self.matches) - 1)
    
    @discord.ui.button(label="◀ Previous", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_buttons()
            embed = create_character_embed(self.matches[self.current_index])
            await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Next ▶", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        if self.current_index < len(self.matches) - 1:
            self.current_index += 1
            self.update_buttons()
            embed = create_character_embed(self.matches[self.current_index])
            await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        """Disable buttons when view times out."""
        for child in self.children:
            child.disabled = True
        if self.message:
            await self.message.edit(view=self)