import discord
import aiohttp
from discord.ext import commands
from bs4 import BeautifulSoup

PARKING_URL = "https://apss.oga.ncku.edu.tw/park/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

class NCKUParking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_parking_data(self):
        """從成功大學停車場網頁抓取剩餘機車車位數"""
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(PARKING_URL) as response:
                if response.status == 200:
                    html = await response.text()
                    return self.parse_parking_data(html)  
                else:
                    print(f"HTTP 錯誤代碼: {response.status}")
                    return None

    def parse_parking_data(self, html):
        """解析 HTML 取得機車剩餘車位數"""
        soup = BeautifulSoup(html, "html.parser")
        
        parking_info = soup.find("table", class_="table")  # 檢查這行是否正確
        if not parking_info:
            print("找不到 table，可能 HTML 結構改變")
            return None

        rows = parking_info.find_all("tr")
        result = []
        for row in rows[1:]:  
            cols = row.find_all("td")
            if len(cols) >= 2:
                area = cols[0].text.strip()
                slots = cols[1].text.strip()
                result.append(f"{area}: {slots} 位")

        return "\n".join(result) if result else None

    @commands.command(name="nckupark")
    async def check_parking(self, ctx):
        """查詢成功大學的機車剩餘車位數"""
        data = await self.fetch_parking_data()
        if data:
            await ctx.send(f"🚗 **成功大學機車剩餘車位數** 🚗\n{data}")  
        else:
            await ctx.send("❌ 無法取得成功大學的車位資訊，請稍後再試！")

async def setup(bot):
    await bot.add_cog(NCKUParking(bot))
