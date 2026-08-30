import discord
from discord.ext import commands
from src.config import FACTION_DISPLAY
from src.teams import TeamDatabase
from src.characters import CharacterDatabase
from src.embeds import create_team_embed
from src.config import TEST_GUILD
from src.buttons import Paginator

class Teams(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.team = TeamDatabase()
        self.char = CharacterDatabase()


    #, guild_ids = [TEST_GUILD]
    @discord.slash_command(name='team', description="shows the meta teams for a faction!")
    async def show_team(self, ctx, faction: str):
        faction_lower = faction.lower()
        
        if faction_lower not in FACTION_DISPLAY:
            await ctx.respond("Invalid faction! Try `/command` for help.", ephemeral=True)
            return
        
        teams = self.team.get_teams_by_faction(faction_lower)

        #print(teams)
        
        if not teams:
            await ctx.respond(f"No teams found for {faction}", ephermeral=True)
            return

        pages = []
        #print(pages)
        
        for team in teams:
            pages.append(create_team_embed(faction_lower, team, self.char))

        if(len(pages) != 1):
            view = Paginator(pages, lambda e: e, author_id=ctx.author.id)
            message = await ctx.respond(embed=pages[0], view=view)
            view.message = message
        else:
            await ctx.respond(embed=pages[0])

        
def setup(bot):
    bot.add_cog(Teams(bot))