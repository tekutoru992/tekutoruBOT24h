import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # 翻訳コマンド
    # -------------------------
    @app_commands.command(name="translate", description="文章を自動翻訳します")
    async def translate(self, interaction: discord.Interaction, text: str):
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": "auto|ja"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()

        translated = data["responseData"]["translatedText"]

        embed = discord.Embed(title="🌐 翻訳結果", color=0x00ffcc)
        embed.add_field(name="元の文章", value=text, inline=False)
        embed.add_field(name="翻訳", value=translated, inline=False)

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # 天気コマンド
    # -------------------------
    @app_commands.command(name="weather", description="指定した場所の天気を表示します")
    async def weather(self, interaction: discord.Interaction, location: str):
        url = f"https://wttr.in/{location}?format=j1"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        current = data["current_condition"][0]
        temp = current["temp_C"]
        desc = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        wind = current["windspeedKmph"]

        embed = discord.Embed(title=f"☀️ 天気情報：{location}", color=0x00ffcc)
        embed.add_field(name="気温", value=f"{temp}℃")
        embed.add_field(name="天気", value=desc)
        embed.add_field(name="湿度", value=f"{humidity}%")
        embed.add_field(name="風速", value=f"{wind} km/h")

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # アイコン表示
    # -------------------------
    @app_commands.command(name="avatar", description="ユーザーのアイコンを表示します")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user

        embed = discord.Embed(title=f"{user.name} のアイコン", color=0x00ffcc)
        embed.set_image(url=user.avatar)

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # Ping
    # -------------------------
    @app_commands.command(name="ping", description="Bot の応答速度を表示します")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! {latency}ms")

    # -------------------------
    # ロール情報
    # -------------------------
    @app_commands.command(name="roleinfo", description="ロールの情報を表示します")
    async def roleinfo(self, interaction: discord.Interaction, role: discord.Role):
        embed = discord.Embed(title=f"🎭 ロール情報：{role.name}", color=role.color)
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="メンバー数", value=len(role.members))
        embed.add_field(name="作成日", value=role.created_at.strftime("%Y-%m-%d"))

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # 参加日
    # -------------------------
    @app_commands.command(name="joined", description="ユーザーがサーバーに参加した日を表示します")
    async def joined(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user

        embed = discord.Embed(title=f"📅 {user.name} の参加日", color=0x00ffcc)
        embed.add_field(name="参加日", value=user.joined_at.strftime("%Y-%m-%d"))

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # メッセージ検索
    # -------------------------
    @app_commands.command(name="search", description="最近のメッセージからキーワード検索します")
    async def search(self, interaction: discord.Interaction, keyword: str):
        channel = interaction.channel
        results = []

        async for msg in channel.history(limit=200):
            if keyword.lower() in msg.content.lower():
                results.append(f"{msg.author}: {msg.content}")

        if not results:
            await interaction.response.send_message("🔍 一致するメッセージはありませんでした。")
            return

        text = "\n".join(results[:10])

        embed = discord.Embed(title="🔍 検索結果", description=text, color=0x00ffcc)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Tools(bot))
