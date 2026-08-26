import discord
from discord.ext import commands
from discord.commands import Option
from cells import CellsDatabase
from embeds import create_cells_embed, create_cells_list_embed
from buttons import Paginator
from config import TEST_GUILD

class Cells(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = CellsDatabase()

    #guild_ids=[TEST_GUILD]
    @discord.slash_command(name="find-cell", description="List all available cells for a character!", guild_ids=[TEST_GUILD])
    async def test(self, ctx, *, name:str, attr:str, slot:Option(str, "Enter the Slot of the Cell", required = False, default = ' ')):
        tempstr = name + " " + attr + " " + slot

        parts = tempstr.split()

        if len(parts) == 2:
            name, attribute = parts
            matches = self.db.find_cells_list(name, attribute)

            if not matches:
                await ctx.respond("Cell not Found! Make sure you typed correctly or try /command for help!", ephemeral=True)
                return

            if len(matches) == 1:
                embed = create_cells_embed(matches[0])
                await ctx.respond(embed=embed)

            elif len(matches) < 11:
                embed = create_cells_list_embed(matches)
                await ctx.respond(embed=embed)

            else:
                #try not preloading all the embeds
                count = 0
                pages = []
                while count < len(matches):
                    page_embed = create_cells_list_embed(
                        matches[count:count+10], 
                        start_index=count
                    )
                    pages.append(page_embed)
                    count += 10
                
                view = Paginator(pages, lambda e: e, author_id=ctx.author.id)
                embed = pages[0]
                message = await ctx.respond(embed=embed, view=view)
                view.message = message

        elif len(parts) == 3:
            name, attribute, cellType = parts
            matches = self.db.find_cells(name, attribute, cellType)
            
            if not matches:
                await ctx.respond("Cell not found! Make sure you typed correctly "
                                "or try `/command` for help!", ephemeral=True)
                return
            
            embed = create_cells_embed(matches[0])

            if len(matches) == 1:
                await ctx.respond(embed=embed)

            else:
                view = Paginator(matches, embed_factory=create_cells_embed, author_id=ctx.author.id)
                message = await ctx.respond(f"Found {len(matches)} matches:\n", embed=embed, view=view)
                view.message = message

        else: 
            await ctx.respond("Missing argument! Try `/command` for help.", ephemeral=True)


def setup(bot):
    bot.add_cog(Cells(bot))