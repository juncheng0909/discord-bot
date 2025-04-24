import discord
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 更改狀態(self, ctx, *, status: str = None):
        if status is None:
            await ctx.send("你要改成什麼啦？")
        else:
            game = discord.Game(status)
            await self.bot.change_presence(status=discord.Status.idle, activity=game)
            await ctx.send(f"✅ 狀態已更改為：{status}")

async def setup(bot):
    await bot.add_cog(Status(bot))
