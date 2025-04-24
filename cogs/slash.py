import discord
from discord.ext import commands
from discord import app_commands  #  支援 Slash 指令

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="向機器人打招呼！")  # Slash 指令
    async def hello(self, interaction: discord.Interaction):
        """回應 Hello"""
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

async def setup(bot):
    await bot.add_cog(Example(bot))
