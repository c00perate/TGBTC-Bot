import discord
from discord.ext import commands
from src.config import SHEET_URL, SERVER
from src.config import TEST_GUILD

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #, guild_ids=[TEST_GUILD]
    @discord.slash_command(name="credit", aliases=["credits"], description="show the credits for the bot")
    async def show_credits(self, ctx):
        await ctx.respond(
            "Made by c00per and Hnff."
        )

    #, guild_ids=[TEST_GUILD]
    @discord.slash_command(name="sheet", description="base stat sheet for the bot")
    async def show_sheet(self, ctx):
        await ctx.respond(f"Here's my [sheet]({SHEET_URL})")

    @discord.slash_command(name="resources", description="community resources")
    async def show_resources(self, ctx):
        await ctx.respond(f"Bot support server: {SERVER}\n"
            "Gluttony server (for leaks): https://discord.gg/jurzSUchHU\n"
            "Chatmojo website: https://tkgbtc.com", 
             ephemeral=True)


    #, guild_ids=[TEST_GUILD]
    @discord.slash_command(name='command', description="shows all command syntax")
    async def show_commands(self, ctx):
        await ctx.respond(
            "`/find-char [character] [optional: skl/spd/str/psy/wit/dst]`\n"
            "Example: `/find-char arima wit`\n"
            "Example: `/find-char arima`\n\n"
            "`/team [anteiku/aogiri/ccg/noorg]`\n"
            "Example: `/team noorg`\n\n"
            "`/rank [base/3x/4x/atk/def/hp]`\n"
            "Example: `/rank 3x`\n\n"
            "`/find-cell [character] [attribute] [optional: atk/def/hp]`\n"
            "Example: `/find-cell kaneki str atk`\n"
            "Example: `/find-cell kaneki str`", ephemeral=True
        )

def setup(bot):
    bot.add_cog(Misc(bot))