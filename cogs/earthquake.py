import discord
import requests
import asyncio
from discord.ext import commands, tasks

API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001"
API_KEY = "CWA-68EB88C3-92B4-47C9-8D0C-431BE975B174"

class EarthquakeNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_earthquake_id = None  # 記錄最新的地震編號
        self.check_earthquake.start()  # 啟動定時任務

    def fetch_latest_earthquake(self):
        """從中央氣象署 API 取得最新地震資訊"""
        response = requests.get(API_URL, params={"Authorization": API_KEY, "format": "JSON"})
        if response.status_code == 200:
            data = response.json()
            if "records" in data and "earthquake" in data["records"]:
                earthquakes = data["records"]["earthquake"]
                if earthquakes:
                    latest = earthquakes[0]
                    eq_id = latest["earthquakeNo"]  # 地震編號

                    # 如果是新的地震，就回傳資訊
                    if eq_id != self.last_earthquake_id:
                        self.last_earthquake_id = eq_id
                        return (
                            f"🌍 **地震通知** 🌍\n"
                            f"📅 發生時間: {latest['earthquakeInfo']['originTime']}\n"
                            f"📍 位置: {latest['earthquakeInfo']['epicenter']['location']}\n"
                            f"💪 芮氏規模: {latest['earthquakeInfo']['magnitude']['magnitudeValue']}\n"
                            f"📏 深度: {latest['earthquakeInfo']['depth']['value']} 公里\n"
                            f"🗺️ [詳細資訊](https://www.cwa.gov.tw/V8/C/E/index.html)"
                        )
        return None

    @tasks.loop(minutes=5)  # 每 5 分鐘檢查一次
    async def check_earthquake(self):
        """定期檢查地震資訊，並發送通知"""
        print("🔄 正在執行定時地震檢查...")
        await self.bot.wait_until_ready()  # 確保機器人啟動後才執行
        channel_id = 1336277429974601769  # 替換成你的頻道 ID
        channel = self.bot.get_channel(channel_id)
        if channel:
            earthquake_info = self.fetch_latest_earthquake()
            if earthquake_info:
                await channel.send(earthquake_info)

    @commands.command()
    async def earthquake(self, ctx):
        """手動查詢最新地震資訊"""
        earthquake_info = self.fetch_latest_earthquake()
        if earthquake_info:
            await ctx.send(earthquake_info)
        else:
            await ctx.send("✅ 目前沒有新的地震資訊！")

async def setup(bot):
    await bot.add_cog(EarthquakeNotifier(bot))
