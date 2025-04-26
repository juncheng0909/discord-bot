import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# 載入 .env 檔案
load_dotenv()

# 取得 Discord Token
TOKEN = os.getenv("DISCORD_TOKEN")

# 設定 Intents
intents = discord.Intents.default()
intents.message_content = True

# 建立 Bot 物件，使用 commands.Bot 來支援 Cog
bot = commands.Bot(command_prefix="%", intents=intents)

# 當機器人啟動時
@bot.event
async def on_ready():
    print(f'✅ 目前登入身份：{bot.user}')
    # 確保 Slash 指令同步
    try:
        slash = await bot.tree.sync()
        print(f"✅ 載入 {len(slash)} 個斜線指令")
    except Exception as e:
        print(f"❌ Slash 指令同步失敗: {e}")
    game = discord.Game('努力學習py中')
    await bot.change_presence(status=discord.Status.idle, activity=game)

# 自動載入 cogs 資料夾內的模組
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")  # 移除 .py

# 啟動機器人
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)  # 用 .env 的 Token 啟動

# 指令：載入某個 Cog
@bot.command()
async def load(ctx, extension):
    try:
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"✅ 成功載入 {extension}.py")
    except Exception as e:
        await ctx.send(f"❌ 載入 {extension}.py 失敗: {e}")

# 指令：卸載某個 Cog
@bot.command()
async def unload(ctx, extension):
    try:
        await bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"✅ 成功卸載 {extension}.py")
    except Exception as e:
        await ctx.send(f"❌ 卸載 {extension}.py 失敗: {e}")

# 指令：重新載入某個 Cog
@bot.command()
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"✅ 成功重新載入 {extension}.py")
    except Exception as e:
        await ctx.send(f"❌ 重新載入 {extension}.py 失敗: {e}")

# 啟動主程式
if __name__ == "__main__":
    asyncio.run(main())
