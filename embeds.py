import discord
from typing import Dict
from characters import CharacterDatabase
from config import *


def create_character_embed(char: Dict) -> discord.Embed:
    character_slug = char['Character'].lower().replace(' ', '')
    title_slug = char['Title'].lower().replace(' ', '').replace('/', '')
    thumbnail_url = f"https://raw.githubusercontent.com/c00perate/btc-images/main/{character_slug}-{title_slug}.png"
    
    embed = discord.Embed(
        title=char['Character'],
        description=char['Title'],
        color=COLOUR[char['Attribute']]
    )
    embed.set_thumbnail(url=thumbnail_url)
    
    fields = [
        ("Attribute", char['Attribute'], True),
        ("Faction", char['Faction'], True),
        ("Tactic", char['Tactic'], True),
        ("Base CP", f"{char['Base CP']} (#{char['Base CP_rank']})", True),
        ("3x Cell CP", f"{char['3x Cell CP']} (#{char['3x Cell CP_rank']})", True),
        ("4x Cell CP", f"{char['4x Cell CP']} (#{char['4x Cell CP_rank']})", True),
        ("Base ATK", f"{char['Base ATK']} (#{char['Base ATK_rank']})", True),
        ("Base DEF", f"{char['Base DEF']} (#{char['Base DEF_rank']})", True),
        ("Base HP", f"{char['Base HP']} (#{char['Base HP_rank']})", True),
        ("Release Date", char['Release Date'], True),
        ("Obtained", char['Obtained'], True),
    ]
    
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    
    embed.set_footer(text="All Cell CP include LR cells (if any) without any upgrades\n"
                          "Base CP is extrapolated from Strategic Arena")
    
    return embed


def create_team_embed(faction: str, team: Dict, char_db: CharacterDatabase) -> discord.Embed:
    display_name = FACTION_DISPLAY[faction]['name']
    
    embed = discord.Embed(
        title=f"{display_name} Teams",
        description=f"Current meta teams for {display_name}",
        color=FACTION_DISPLAY[faction]['colour']
    )
    
    team_members = []
    overall_cp3 = 0
    overall_cp4 = 0
    
    for i in range(1, 6):
        char_name = team.get(f"char{i}")
        char_attr = team.get(f"attr{i}")
        char_title = team.get(f"title{i}")
        
        if not char_name:
            continue
        
        char = char_db.find_character(char_name, char_attr, char_title)
        if char:
            team_members.append(f"- {char['Character']} [{char['Title']}]")
            overall_cp3 += char['3x Cell CP']
            overall_cp4 += char['4x Cell CP']
    
    embed.add_field(name="Overall Team", value='\n'.join(team_members), inline=False)
    embed.add_field(name="Ultimate", value=team['ult'], inline=False)
    embed.add_field(name="Overall 3x Cell CP", value=str(overall_cp3), inline=True)
    embed.add_field(name="Overall 4x Cell CP", value=str(overall_cp4), inline=True)
    embed.add_field(name="Description", value=team['description'], inline=False)
    embed.set_thumbnail(url=f"https://raw.githubusercontent.com/c00perate/btc-images/8dda16c/{faction.lower()}.png")
    
    return embed

def create_ranking_embed(stat_name: str, top_chars: list, stat_key: str) -> discord.Embed:
    description = '\n'.join(
        f"{i}. {char['Character']} [{char['Title']}] - {char[stat_key]}"
        for i, char in enumerate(top_chars, start=1)
    )

    embed = discord.Embed(
        title=f"Top 10 Characters Ranked by {stat_name}",
        description=description,
        color=discord.Color.light_gray()
    )
    
    embed.set_footer(
        text="All Cell CP include LR cells (if any) without any upgrades\n"
             "Base CP is extrapolated from Strategic Arena"
    )
    
    return embed