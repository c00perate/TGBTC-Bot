import discord
from discord.ext import commands

from config import *
from teams import*
from characters import *
from embeds import *


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    activity=discord.Game(name="Type !command for a guide!")
)

char_db = CharacterDatabase()
team_db = TeamDatabase()


@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    print(f'Loaded {len(char_db.characters)} characters')
    print(f'Loaded {len(team_db.teams)} teams')


@bot.event
async def on_message(message):
    if message.author.id in BLOCKED_USERS:
        return
    
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        if message.author.id == 1164259640452857906:
            await message.channel.send("hi matti")
        else:
            await message.channel.send("Try `!command` for help!")
        return
    
    await bot.process_commands(message)


@bot.command(name='command')
async def show_commands(ctx):
    await ctx.send(
        "Commands:\n\n"
        "`![character name] [optional: skl/spd/str/psy/wit]`\n"
        "Example: `!arima wit`\n"
        "Example: `!arima`\n\n"
        "`!team [anteiku/aogiri/ccg/noorg]`\n"
        "Example: `!team noorg`\n\n"
        "`!rank [base/3x/4x/atk/def/hp]`\n"
        "Example: `!rank 3x`"
    )


@bot.command(name='team')
async def show_team(ctx, faction: str):
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
    category_lower = category.lower()
    
    if category_lower not in SEARCH_QUERIES:
        await ctx.send("Invalid parameter! Use `!rank` with a valid query or try `!command` for help!")
        return
    
    stat_name = SEARCH_QUERIES[category_lower]['value']
    top_chars = char_db.get_top_characters(stat_name, limit=10)
    
    embed = create_ranking_embed(stat_name, top_chars, stat_name)

    await ctx.send(embed=embed)


@bot.command(name='cell')
async def show_cells(ctx, *, name: str):

    parts = name.split(maxsplit=1)

    if len(parts) != 2:
        await ctx.send("Missing argument! Try `!command` for help.")

    name, attribute = parts
    matches = char_db.find_characters(name, attribute)
    
    if not matches:
        await ctx.send("Character not found! Make sure you typed correctly "
                        "or try `!command` for help!")
        return
    
    embed = create_cell_embed(matches[0])

    if len(matches) == 1:
        await ctx.send(embed=embed)

    else:
        view = Paginator(matches)
        await ctx.send(f"Found {len(matches)} matches:\n")
        message = await ctx.send(embed=embed, view=view)
        view.message = message
    

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await handle_character_search(ctx)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument! Try `!command` for help.")
    else:
        print(f"Error: {error}")
        await ctx.send("An error occurred. Try `!command` for help!")


@bot.command(name='credits')
async def show_credits(ctx):
    await ctx.send(
        "Made by c00per and Hnff for the Tokyo Ghoul: Break the Chains (Global) server!\n"
        "Special thanks to Ariku for providing the character thumbnails."
    )

@bot.command(name='sheet')
async def show_sheet(ctx):
    await ctx.send(f"Here's my [sheet]({SHEET_URL})")


@bot.command(name='youtube')
async def show_youtube(ctx):
    await ctx.send(f"Here's my [Youtube channel]({YOUTUBE_URL})")


async def handle_character_search(ctx):
    content = ctx.message.content
    
    if not content.startswith('!'):
        return
    
    parts = content[1:].split(maxsplit=1)
    
    if len(parts) == 1:
        name = parts[0]
        matches = char_db.find_name(name)

        if not matches:
            await ctx.send("Character not found! Make sure you typed correctly "
                           "or try `!command` for help!")
            return
        elif len(matches) == 1:
            embed = create_character_embed(matches[0])
            await ctx.send(embed=embed)
        else:
            embed = create_name_embed(matches)
            await ctx.send(embed=embed)

    elif len(parts) == 2:
        name, attribute = parts
        matches = char_db.find_characters(name, attribute)
        
        if not matches:
            await ctx.send("Character not found! Make sure you typed correctly "
                           "or try `!command` for help!")
            return
        
        embed = create_character_embed(matches[0])

        if len(matches) == 1:
            await ctx.send(embed=embed)

        else:
            view = Paginator(matches)
            await ctx.send(f"Found {len(matches)} matches:\n")
            message = await ctx.send(embed=embed, view=view)
            view.message = message

    else:
        await ctx.send("Invalid command! Try `!command` for help!")
        return


if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Failed to start bot: {e}")