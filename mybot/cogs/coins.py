import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random
import datetime

DATA_FILE = "coins.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class Coins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()

    def add_coin(self, user_id, amount):
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id] = {"coins": 0, "last_daily": "0"}
        self.data[user_id]["coins"] += amount
        save_data(self.data)

    def get_coin(self, user_id):
        user_id = str(user_id)
        if user_id not in self.data:
            return 0
        return self.data[user_id]["coins"]

    # 所持金確認
    @app_commands.command(name="coin", description="自分の所持コインを確認します")
    async def coin(self, interaction: discord.Interaction):
        coins = self.get_coin(interaction.user.id)
        await interaction.response.send_message(f"💰 {interaction.user.mention} の所持金: **{coins} コイン**")

    # デイリー報酬
    @app_commands.command(name="daily", description="24時間に1回コインを受け取れます")
    async def daily(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        now = datetime.datetime.utcnow()

        if user_id not in self.data:
            self.data[user_id] = {"coins": 0, "last_daily": "0"}

        last = self.data[user_id]["last_daily"]
        last_time = datetime.datetime.fromisoformat(last) if last != "0" else None

        if last_time and (now - last_time).total_seconds() < 86400:
            remain = 86400 - (now - last_time).total_seconds()
            hours = int(remain // 3600)
            minutes = int((remain % 3600) // 60)
            return await interaction.response.send_message(
                f"⏳ デイリーはあと **{hours}時間 {minutes}分** 後に受け取れます。",
                ephemeral=True
            )

        reward = random.randint(100, 300)
        self.add_coin(interaction.user.id, reward)
        self.data[user_id]["last_daily"] = now.isoformat()
        save_data(self.data)

        await interaction.response.send_message(f"🎁 デイリー報酬: **{reward} コイン** を受け取りました！")

    # コイン送金
    @app_commands.command(name="give", description="他のユーザーにコインを送ります")
    async def give(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if amount <= 0:
            return await interaction.response.send_message("金額は1以上にしてください。", ephemeral=True)

        sender = str(interaction.user.id)
        receiver = str(user.id)

        if self.get_coin(sender) < amount:
            return await interaction.response.send_message("💸 コインが足りません。", ephemeral=True)

        self.add_coin(interaction.user.id, -amount)
        self.add_coin(user.id, amount)

        await interaction.response.send_message(
            f"🤝 {interaction.user.mention} → {user.mention} に **{amount} コイン** を送金しました！"
        )

    # ギャンブル
    @app_commands.command(name="gamble", description="コインを賭けて勝負します")
    async def gamble(self, interaction: discord.Interaction, amount: int):
        if amount <= 0:
            return await interaction.response.send_message("金額は1以上にしてください。", ephemeral=True)

        if self.get_coin(interaction.user.id) < amount:
            return await interaction.response.send_message("💸 コインが足りません。", ephemeral=True)

        win = random.choice([True, False])

        if win:
            self.add_coin(interaction.user.id, amount)
            await interaction.response.send_message(f"🎉 勝利！ **+{amount} コイン**")
        else:
            self.add_coin(interaction.user.id, -amount)
            await interaction.response.send_message(f"😢 敗北… **-{amount} コイン**")

    # ランキング
    @app_commands.command(name="leaderboard", description="コインランキングを表示します")
    async def leaderboard(self, interaction: discord.Interaction):
        sorted_users = sorted(self.data.items(), key=lambda x: x[1]["coins"], reverse=True)
        text = ""

        for i, (uid, info) in enumerate(sorted_users[:10], start=1):
            user = interaction.guild.get_member(int(uid))
            name = user.display_name if user else "Unknown"
            text += f"{i}. **{name}** — {info['coins']} コイン\n"

        embed = discord.Embed(title="🏆 コインランキング", description=text, color=0xffd700)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Coins(bot))
