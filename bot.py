import discord
import json
import os
from discord.ext import commands
import asyncio

# 讀取 JSON 設定檔
with open('items.json', "r", encoding="utf8") as file:
    data = json.load(file)

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
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
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
        await bot.start(data["token"])  # 讀取 JSON 檔內的 Token

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

import asyncio
asyncio.run(main())  # 使用 asyncio.run() 來啟動 bot
