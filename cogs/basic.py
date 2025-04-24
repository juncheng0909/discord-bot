from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 說(self, ctx, *, message: str = None):
        if message is None:
            await ctx.send("你要我說什麼啦？")
        else:
            await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Basic(bot))
