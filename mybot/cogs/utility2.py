import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import datetime
import urllib.parse

class Utility2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 計算機
    @app_commands.command(name="calc", description="計算します")
    async def calc(self, interaction: discord.Interaction, expression: str):
        try:
            result = eval(expression)
        except:
            await interaction.response.send_message("計算式が無効です。", ephemeral=True)
            return

        await interaction.response.send_message(f"🧮 結果: **{result}**")

    # 世界時計
    @app_commands.command(name="time", description="世界の現在時刻を表示します")
    async def time(self, interaction: discord.Interaction, region: str):
        now = datetime.datetime.utcnow()
        embed = discord.Embed(title=f"🕒 世界時計：{region}", color=0x00ffcc)
        embed.add_field(name="UTC", value=now.strftime("%Y-%m-%d %H:%M:%S"))
        await interaction.response.send_message(embed=embed)

    # URL展開
    @app_commands.command(name="urlinfo", description="URLの情報を表示します")
    async def urlinfo(self, interaction: discord.Interaction, url: str):
        parsed = urllib.parse.urlparse(url)
        embed = discord.Embed(title="🔗 URL情報", color=0x00ffcc)
        embed.add_field(name="スキーム", value=parsed.scheme)
        embed.add_field(name="ドメイン", value=parsed.netloc)
        embed.add_field(name="パス", value=parsed.path)
        await interaction.response.send_message(embed=embed)

    # URL短縮
    @app_commands.command(name="shorten", description="URLを短縮します")
    async def shorten(self, interaction: discord.Interaction, url: str):
        api = f"https://is.gd/create.php?format=simple&url={url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api) as resp:
                short = await resp.text()

        await interaction.response.send_message(f"🔗 短縮URL: {short}")

async def setup(bot):
    await bot.add_cog(Utility2(bot))
