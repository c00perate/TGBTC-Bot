import discord
from discord.ext import commands
import csv
from config import *
from collections import defaultdict
from functools import lru_cache
from typing import Optional, List, Dict

# ============================================================================
# DATA LOADING AND INDEXING
# ============================================================================

class CharacterDatabase:
    """Efficiently manages character data with optimized lookups"""
    
    def __init__(self, csv_path: str = 'characters.csv'):
        self.characters: List[Dict] = []
        self.char_index: Dict[tuple, List[Dict]] = defaultdict(list)
        self.rankings: Dict[str, List[Dict]] = {}
        self._load_characters(csv_path)
        self._build_index()
        self._calculate_rankings()
    
    def _load_characters(self, csv_path: str):
        """Load characters from CSV with type conversion"""
        int_fields = ['Base CP', '3x Cell CP', '4x Cell CP', 'Base ATK', 'Base DEF', 'Base HP']
        
        #encoding to account for funny characters
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                for field in int_fields:
                    row[field] = int(row[field])
                row['Nicknames'] = str(row.get('Nicknames', ''))
                self.characters.append(row)
    
    def _build_index(self):
        """Build optimized lookup index"""
        for char in self.characters:
            character_name = char['Character'].lower()
            attribute = char['Attribute']
            
            # Primary key: (name, attribute)
            key = (character_name, attribute)
            self.char_index[key].append(char)
            
            # Index individual words only if multi-word name
            name_parts = character_name.split()
            if len(name_parts) > 1:
                for part in name_parts:
                    self.char_index[(part, attribute)].append(char)  

            # Index nicknames
            if char['Nicknames']:
                for nickname in char['Nicknames'].lower().split(';'):
                    nickname = nickname.strip()
                    if nickname:
                        self.char_index[(nickname, attribute)].append(char)
    
    def _calculate_rankings(self):
        """Pre-calculate rankings for all stats"""
        stats = ['Base CP', 'Base ATK', 'Base DEF', 'Base HP', '3x Cell CP', '4x Cell CP']
        
        for stat in stats:
            sorted_chars = sorted(self.characters, key=lambda x: x[stat], reverse=True)
            self.rankings[stat] = sorted_chars
            for rank, char in enumerate(sorted_chars, start=1):
                char[f'{stat}_rank'] = rank
    
    def find_character(self, name: str, attribute: str, title: Optional[str] = None) -> Optional[Dict]:
        """Find a character by name, attribute, and optionally title"""
        key = (name.lower(), attribute.upper())
        matches = self.char_index.get(key, [])
        
        if not matches:
            return None
        
        if title:
            title_lower = title.lower()
            for match in matches:
                if match['Title'].lower() == title_lower:
                    return match
        
        # Return first match if no title specified
        return matches[0] if matches else None
    
    def find_characters(self, name: str, attribute: str) -> List[Dict]:
        """Find all characters matching name and attribute"""
        key = (name.lower(), attribute.upper())
        return self.char_index.get(key, [])
    
    def get_top_characters(self, stat: str, limit: int = 10) -> List[Dict]:
        """Get top N characters by stat"""
        return self.rankings.get(stat, [])[:limit]


class TeamDatabase:
    """Manages team data"""
    
    def __init__(self, csv_path: str = 'teams.csv'):
        self.teams: List[Dict] = []
        self._load_teams(csv_path)
    
    def _load_teams(self, csv_path: str):
        """Load teams from CSV"""
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.teams = list(reader)
    
    def get_teams_by_faction(self, faction: str) -> List[Dict]:
        """Get all teams for a specific faction"""
        faction_lower = faction.lower()
        return [team for team in self.teams if team['faction'].lower() == faction_lower]


# ============================================================================
# BOT SETUP
# ============================================================================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    activity=discord.Game(name="Type !command for a guide!")
)

# Initialize databases
char_db = CharacterDatabase()
team_db = TeamDatabase()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_character_embed(char: Dict) -> discord.Embed:
    """Create an embed for a character"""
    character_slug = char['Character'].lower().replace(' ', '')
    title_slug = char['Title'].lower().replace(' ', '').replace('/', '')
    thumbnail_url = f"https://raw.githubusercontent.com/c00perate/btc-images/main/{character_slug}-{title_slug}.png"
    
    embed = discord.Embed(
        title=char['Character'],
        description=char['Title'],
        color=COLOUR[char['Attribute']]
    )
    embed.set_thumbnail(url=thumbnail_url)
    
    # Add fields in a more organized way
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
    """Create an embed for a team"""
    display_name = FACTION_DISPLAY[faction]['name']
    
    embed = discord.Embed(
        title=f"{display_name} Teams",
        description=f"Current meta teams for {display_name}",
        color=FACTION_DISPLAY[faction]['colour']
    )
    
    team_members = []
    overall_cp3 = 0
    overall_cp4 = 0
    
    # Iterate through team members
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


# ============================================================================
# COMMANDS
# ============================================================================

@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    print(f'Loaded {len(char_db.characters)} characters')
    print(f'Loaded {len(team_db.teams)} teams')


@bot.command(name='command')
async def show_commands(ctx):
    """Show available commands"""
    await ctx.send(
        "Commands:\n\n"
        "`![character name] [skl/spd/str/psy/wit]`\n"
        "Example: `!arima wit`\n\n"
        "`!team [anteiku/aogiri/ccg/noorg]`\n"
        "Example: `!team noorg`\n\n"
        "`!rank [base/3x/4x/atk/def/hp]`\n"
        "Example: `!rank 3x`"
    )


@bot.command(name='credits')
async def show_credits(ctx):
    """Show bot credits"""
    await ctx.send(
        "Made by c00per and Hnff for the Tokyo Ghoul: Break the Chains (Global) server!\n"
        "Special thanks to Ariku for providing the character thumbnails."
    )


@bot.command(name='sheet')
async def show_sheet(ctx):
    """Show spreadsheet link"""
    await ctx.send(f"Here's my [sheet]({SHEET_URL})")


@bot.command(name='youtube')
async def show_youtube(ctx):
    """Show YouTube channel"""
    await ctx.send(f"Here's my [Youtube channel]({YOUTUBE_URL})")


@bot.command(name='team')
async def show_team(ctx, faction: str):
    """Show teams for a specific faction"""
    faction_lower = faction.lower()
    
    if faction_lower not in FACTION_DISPLAY:
        await ctx.send("Invalid faction! Try `!command` for help.")
        return
    
    teams = team_db.get_teams_by_faction(faction_lower)
    
    if not teams:
        await ctx.send(f"No teams found for {faction}")
        return
    
    for team in teams:
        embed = create_team_embed(faction_lower, team, char_db)
        await ctx.send(embed=embed)


@bot.command(name='rank')
async def show_ranking(ctx, category: str):
    """Show top 10 characters by stat"""
    category_lower = category.lower()
    
    if category_lower not in SEARCH_QUERIES:
        await ctx.send("Invalid parameter! Use `!rank` with a valid query or try `!command` for help!")
        return
    
    stat_name = SEARCH_QUERIES[category_lower]['value']
    top_chars = char_db.get_top_characters(stat_name, limit=10)
    
    description = '\n'.join(
        f"{i}. {char['Character']} [{char['Title']}] - {char[stat_name]}"
        for i, char in enumerate(top_chars, start=1)
    )
    
    embed = discord.Embed(
        title=f"Top 10 Characters Ranked by {stat_name}",
        description=description,
        color=discord.Color.light_gray()
    )
    
    embed.set_footer(text="All Cell CP include LR cells (if any) without any upgrades\n"
                          "Base CP is extrapolated from Strategic Arena")
    
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    # Block specific users
    if message.author.id in BLOCKED_USERS:
        return
    
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Handle mentions
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        if message.author.id == 1164259640452857906:
            await message.channel.send("hi matti")
        else:
            await message.channel.send("Try `!command` for help!")
        return
    
    # Process commands
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors gracefully"""
    if isinstance(error, commands.CommandNotFound):
        # This is likely a character search command
        await handle_character_search(ctx)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument! Try `!command` for help.")
    else:
        print(f"Error: {error}")
        await ctx.send("An error occurred. Try `!command` for help!")


async def handle_character_search(ctx):
    """Handle character search when command is not found"""
    content = ctx.message.content
    
    if not content.startswith('!'):
        return
    
    parts = content[1:].split(maxsplit=1)
    
    if len(parts) != 2:
        await ctx.send("Invalid command! Try `!command` for help!")
        return
    
    name, attribute = parts
    matches = char_db.find_characters(name, attribute)
    
    if not matches:
        await ctx.send("Character not found! Make sure you typed correctly or try `!command` for help!")
        return
    
    for char in matches:
        embed = create_character_embed(char)
        await ctx.send(embed=embed)


# ============================================================================
# RUN BOT
# ============================================================================

if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Failed to start bot: {e}")