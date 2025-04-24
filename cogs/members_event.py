from discord.ext import commands
class MemberEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # 取得歡迎頻道 ID，並發送歡迎訊息
        channel = self.bot.get_channel(int(jdata["WELCOME_CHANNEL"]))
        if channel:
            await channel.send(f"{member} 加入了秘密基地!")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # 取得離開頻道 ID，並發送告別訊息
        channel = self.bot.get_channel(int(jdata["LEAVE_CHANNEL"]))
        if channel:
            await channel.send(f"{member} 888888!")

# 註冊 cog
async def setup(bot):
    await bot.add_cog(MemberEvents(bot))
