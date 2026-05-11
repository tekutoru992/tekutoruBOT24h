import discord
from discord.ext import commands
from discord import app_commands
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # サイコロ
    @app_commands.command(name="dice", description="サイコロを振ります")
    async def dice(self, interaction: discord.Interaction):
        num = random.randint(1, 6)
        await interaction.response.send_message(f"🎲 出た目: **{num}**")

    # スロット
    @app_commands.command(name="slot", description="スロットを回します")
    async def slot(self, interaction: discord.Interaction):
        items = ["🍒", "🍋", "⭐", "7️⃣"]
        result = [random.choice(items) for _ in range(3)]
        text = " ".join(result)
        win = "🎉 当たり！" if len(set(result)) == 1 else "😢 はずれ…"
        await interaction.response.send_message(f"{text}\n{win}")

    # バトル
    @app_commands.command(name="battle", description="てくとる vs Bot の戦闘")
    async def battle(self, interaction: discord.Interaction):
        player = random.randint(10, 100)
        bot = random.randint(10, 100)
        result = "🔥 てくとるの勝ち！" if player > bot else "🤖 Botの勝ち！"
        await interaction.response.send_message(
            f"てくとる: {player}\nBot: {bot}\n\n{result}"
        )

    # おみくじ
    @app_commands.command(name="omikuji", description="おみくじを引きます")
    async def omikuji(self, interaction: discord.Interaction):
        result = random.choice(["大吉", "中吉", "小吉", "吉", "凶"])
        await interaction.response.send_message(f"🎴 おみくじ結果: **{result}**")

async def setup(bot):
    await bot.add_cog(Games(bot))
