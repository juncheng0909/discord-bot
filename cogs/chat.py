import discord
from discord.ext import commands
import google.generativeai as genai
import os

# 從 env 檔案讀取金鑰和人物風格
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    print(f"Gemini API 設定失敗 {e}")

SYSTEM_PROMPT = os.getenv("GEMINI_SYSTEM_PROMPT")

# 設定使用的模型和安全設定
generation_config = {
  "temperature": 0.7,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # 每個頻道建立一個獨立的對話
        self.chat_sessions = {}
        self.default_persona = os.getenv("GEMINI_SYSTEM_PROMPT", "你是一個樂於助人的 AI 助理。")
        # 建立一個字典，存放各個頻道的人設
        self.channel_personas = {}
    def get_chat_session(self, channel_id: int):
        # 為指定頻道建立一個新的對話
        if channel_id not in self.chat_sessions:
            # 決定用哪個人設
            # 找不到頻道人設，就用 self.default_persona
            current_persona = self.channel_personas.get(channel_id, self.default_persona)
            print(f"頻道 {channel_id} 正在使用人設: {current_persona[:30]}...")
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash-latest",
                # 將決定好的人設傳入
                system_instruction=current_persona,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            self.chat_sessions[channel_id] = model.start_chat(history=[])
        return self.chat_sessions[channel_id]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if self.bot.user.mentioned_in(message):
            content = message.content.replace(f'<@!{self.bot.user.id}>', '').strip()
            content = content.replace(f'<@{self.bot.user.id}>', '').strip()

            if not content:
                await message.channel.send("找我有什麼事嗎？")
                return
            
            async with message.channel.typing():
                try:
                    chat = self.get_chat_session(message.channel.id)
                    # 發送訊息給 Gemini
                    response = await chat.send_message_async(content)
                    
                    # 從response中取得文字內容
                    ai_response = response.text

                    # 將回覆發送到 Discord 頻道
                    await message.reply(ai_response)

                except genai.types.generation_types.BlockedPromptException as e:
                    print(f"Gemini禁止請求: {e}")
                    await message.reply("無法回答。")
                except Exception as e:
                    print(f"與 Gemini API 互動發生錯誤: {e}")
                    await message.reply("稍後再試吧！")

    @commands.command(name="set_persona", help="設定 AI 在目前頻道的專屬人設。")
    # 用 *, persona_text: str 可以讓指令接收包含空格的完整句子
    async def set_persona(self, ctx: commands.Context, *, persona_text: str):
        channel_id = ctx.channel.id
        self.channel_personas[channel_id] = persona_text
        if channel_id in self.chat_sessions:
            del self.chat_sessions[channel_id]
        await ctx.send(f"這個頻道的人設已更新為：「{persona_text[:100]}...」")

    @commands.command(name="reset_persona", help="清除頻道的專屬人設，恢復為預設。")
    async def reset_persona(self, ctx: commands.Context):
        channel_id = ctx.channel.id
        if channel_id in self.channel_personas:
            del self.channel_personas[channel_id]
        
            # 清除舊的 session
            if channel_id in self.chat_sessions:
                del self.chat_sessions[channel_id]
                
            await ctx.send("在這個頻道的人設已重設為預設值。")
        else:
            await ctx.send("這個頻道沒有設定過專屬人設喔。")

    @commands.command(name="current_persona", help="查看目前頻道的 AI 人設。")
    async def current_persona(self, ctx: commands.Context):
        channel_id = ctx.channel.id
        persona = self.channel_personas.get(channel_id, self.default_persona)
        await ctx.send(f"目前人設：\n>>> {persona}")

    @commands.command(name="clear_chat", help="清除目前頻道的 AI 對話紀錄")
    async def clear_chat_history(self, ctx: commands.Context):
        channel_id = ctx.channel.id
        if channel_id in self.chat_sessions:
            del self.chat_sessions[channel_id]
            await ctx.send("這個頻道的 AI 對話記憶已經被我忘光光了！")
        else:
            await ctx.send("這個頻道本來就沒有跟我的對話紀錄喔。")

async def setup(bot):
    # 檢查 Key 是否存在
    if not os.getenv("GOOGLE_API_KEY"):
        print("錯誤：請在 .env 檔案中設定 GOOGLE_API_KEY")
        return
    await bot.add_cog(Chat(bot))