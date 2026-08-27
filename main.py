import discord
from discord.ext import commands
from src.config import TOKEN
import os

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
        intents=intents, 
        activity=discord.Game(name="Use /command for a guide!"),
        default_command_integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,},
        )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Connected to {len(bot.guilds)} servers")
    print(f"loaded cogs: {[cog for cog in bot.cogs]}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content.startswith("!"):
        await message.channel.send("The bot has been updated with slash commands!\n" \
        "Use `/command` to see available commands.\n" \
        "If the bot isn't available in a server, add it to `My Apps` to use it anywhere!\n" \
        "Join the support server for more information: discord.gg/BE5GaYk6wq")

    await bot.process_commands(message)



for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"failed to start bot: {e}")


