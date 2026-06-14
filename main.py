import discord
from discord.ext import commands
from config import TOKEN, BLOCKED_USERS

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    case_insensitive = True,
    max_messages=0,
    activity=discord.Game(name="Type !command for a guide!")
)


@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    print(f'Connected to {len(bot.guilds)} servers')
    print(f'Loaded cogs: {[cog for cog in bot.cogs]}')


@bot.event
async def on_message(message):
    if message.author.id in BLOCKED_USERS:
        return
    
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        if message.author.id == 1164259640452857906:
            await message.channel.send("hi matti")
        #else:
        #    await message.channel.send("Try `!command` for help!")
        return
    
    await bot.process_commands(message)


@bot.command(name='command', aliases=['commands'])
async def show_commands(ctx):
    await ctx.send(
        "`![character] [optional: skl/spd/str/psy/wit/dst]`\n"
        "Example: `!arima wit`\n"
        "Example: `!arima`\n\n"
        "`!team [anteiku/aogiri/ccg/noorg]`\n"
        "Example: `!team noorg`\n\n"
        "`!rank [base/3x/4x/atk/def/hp]`\n"
        "Example: `!rank 3x`\n\n"
        "`!cell [character] [attribute] [optional: atk/def/hp]`\n"
        "Example: `!cell kaneki str atk`\n"
        "Example: `!cell kaneki str`"
    )

 
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        character_cog = bot.get_cog('Characters')
        if character_cog:
            await character_cog.handle_character_search(ctx)
        else:
            await ctx.send("Cogs not found!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument! Try `!command` for help.")
    else:
        print(f"Error: {error}")
        await ctx.send("An error occurred. Try `!command` for help!")


async def setup_hook():
    await bot.load_extension('cogs.cellCogs')
    await bot.load_extension('cogs.charCogs')
    await bot.load_extension('cogs.miscCogs')
    await bot.load_extension('cogs.rankCogs')
    await bot.load_extension('cogs.teamCogs')


bot.setup_hook = setup_hook 

if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Failed to start bot: {e}")