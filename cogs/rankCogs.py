import discord
from discord.ext import commands
from discord.commands import Option
from src.config import SEARCH_QUERIES
from src.characters import CharacterDatabase
from src.embeds import create_ranking_embed
from src.buttons import Paginator
from src.config import TEST_GUILD

class Rankings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = CharacterDatabase()


    #, guild_ids=[TEST_GUILD]
    @discord.slash_command(name="rank", description="shows the ranking of chars based on x stat")
    async def show_ranking(self, ctx, category:str):
        category_lower = category.lower()

        if category_lower not in SEARCH_QUERIES:
            await ctx.respond("Invalid parameter! Use `/rank` with a valid query or try `/command` for help!", ephemeral=True)
            return
        
        stat_name = SEARCH_QUERIES[category_lower]['value']
        top_chars = self.db.get_top_characters(stat_name, limit=len(self.db.characters))

        #try not preloadin geverything
        count = 0
        pages = []
        while(count < len(top_chars)):
            pages.append(create_ranking_embed(stat_name, top_chars[count:count+10], stat_name, count+1))
            count += 10

        view = Paginator(pages, lambda e: e, author_id=ctx.author.id)
        message = await ctx.respond(embed=pages[0], view=view)
        view.message = message

def setup(bot):
    bot.add_cog(Rankings(bot))