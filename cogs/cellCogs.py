from discord.ext import commands
from cells import CellsDatabase
from embeds import create_cells_embed, create_cells_list_embed
from buttons import Paginator

class Cells(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = CellsDatabase()


    @commands.command(name='cell')
    async def show_cells(self, ctx, *, name: str):

        parts = name.split()

        if len(parts) == 2:
            name, attribute = parts
            matches = self.db.find_cells_list(name, attribute)
            
            if not matches:
                await ctx.send("Cell not found! Make sure you typed correctly "
                            "or try `!command` for help!")
                return

            if len(matches) == 1:
                embed = create_cells_embed(matches[0])
                await ctx.send(embed=embed)

            elif len(matches) < 11:
                embed = create_cells_list_embed(matches)
                await ctx.send(embed=embed)
                    
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
                message = await ctx.send(embed=embed, view=view)
                view.message = message

        elif len(parts) == 3:
            name, attribute, cellType = parts
            matches = self.db.find_cells(name, attribute, cellType)
            
            if not matches:
                await ctx.send("Cell not found! Make sure you typed correctly "
                                "or try `!command` for help!")
                return
            
            embed = create_cells_embed(matches[0])

            if len(matches) == 1:
                await ctx.send(embed=embed)

            else:
                view = Paginator(matches, embed_factory=create_cells_embed, author_id=ctx.author.id)
                message = await ctx.send(f"Found {len(matches)} matches:\n", embed=embed, view=view)
                view.message = message

        else: 
            await ctx.send("Missing argument! Try `!command` for help.")


async def setup(bot):
    await bot.add_cog(Cells(bot))