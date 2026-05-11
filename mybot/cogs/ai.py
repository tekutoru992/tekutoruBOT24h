import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # AIチャット
    @app_commands.command(name="chat", description="AIと会話します")
    async def chat(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(f"🤖（AI風）: {text} について考えてみるよ…")

    # 要約
    @app_commands.command(name="summarize", description="文章を要約します")
    async def summarize(self, interaction: discord.Interaction, text: str):
        summary = text[:50] + "..." if len(text) > 50 else text
        await interaction.response.send_message(f"📝 要約: {summary}")

    # 言語判定
    @app_commands.command(name="detectlang", description="文章の言語を判定します")
    async def detectlang(self, interaction: discord.Interaction, text: str):
        if any("あ" <= c <= "ん" for c in text):
            lang = "日本語"
        else:
            lang = "英語っぽい"
        await interaction.response.send_message(f"🌐 言語判定: **{lang}**")

async def setup(bot):
    await bot.add_cog(AI(bot))
