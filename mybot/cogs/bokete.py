import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random

DATA_FILE = "bokete.json"
GENRE_FILE = "bokete_genres.json"


def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4, ensure_ascii=False)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class Bokete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ボケて進行データ
        self.data = load_json(DATA_FILE, {
            "theme": "",
            "image": "",
            "entries": {},
            "voted": [],
            "points": {}
        })

        # 🔥 ジャンルデータ（ユーザー追加対応）
        self.genres = load_json(GENRE_FILE, {
            "小泉構文": [
                "https://i.imgur.com/8uQxQ2L.jpeg",
                "https://i.imgur.com/4QfZp8F.jpeg"
            ],
            "猫": [
                "https://i.imgur.com/JfZpQ0B.jpeg"
            ]
        })

    # ───────────────────────────────
    # 🔥 ジャンル追加
    # ───────────────────────────────
    @app_commands.command(name="bokete_genre_add", description="新しいジャンルを追加します")
    async def bokete_genre_add(self, interaction: discord.Interaction, genre: str, image_url: str):
        if genre not in self.genres:
            self.genres[genre] = []

        self.genres[genre].append(image_url)
        save_json(GENRE_FILE, self.genres)

        await interaction.response.send_message(
            f"🆕 ジャンル **{genre}** に画像を追加しました！\nURL: {image_url}"
        )

    # ───────────────────────────────
    # 🔥 ジャンル一覧
    # ───────────────────────────────
    @app_commands.command(name="bokete_genre_list", description="登録されているジャンル一覧を表示します")
    async def bokete_genre_list(self, interaction: discord.Interaction):
        text = "\n".join([f"- {g}（{len(imgs)}枚）" for g, imgs in self.genres.items()])
        embed = discord.Embed(title="📚 登録ジャンル一覧", description=text, color=0x00ccff)
        await interaction.response.send_message(embed=embed)

    # ───────────────────────────────
    # 🔥 ジャンルから画像お題開始
    # ───────────────────────────────
    @app_commands.command(name="bokete_genre", description="ジャンルから画像お題を開始します")
    async def bokete_genre(self, interaction: discord.Interaction, genre: str):
        if genre not in self.genres:
            return await interaction.response.send_message(
                f"そのジャンルは存在しません。\n`/bokete_genre_list` で確認できます。",
                ephemeral=True
            )

        image_url = random.choice(self.genres[genre])

        self.data = {
            "theme": f"ジャンル：{genre}",
            "image": image_url,
            "entries": {},
            "voted": [],
            "points": {}
        }
        save_json(DATA_FILE, self.data)

        embed = discord.Embed(
            title=f"🎭 ボケて開始！（ジャンル：{genre}）",
            description="`/bokete_boke` でボケを投稿！",
            color=0xffcc00
        )
        embed.set_image(url=image_url)

        await interaction.response.send_message(embed=embed)

    # ───────────────────────────────
    # ボケ投稿
    # ───────────────────────────────
    @app_commands.command(name="bokete_boke", description="ボケを投稿します")
    async def bokete_boke(self, interaction: discord.Interaction, text: str):
        uid = str(interaction.user.id)

        if not self.data["image"]:
            return await interaction.response.send_message("お題が開始されていません。", ephemeral=True)

        self.data["entries"][uid] = text
        save_json(DATA_FILE, self.data)

        await interaction.response.send_message(f"📝 ボケを受け付けました！\n\n**{text}**")

    # ───────────────────────────────
    # 投票
    # ───────────────────────────────
    @app_commands.command(name="bokete_vote", description="面白かったボケに投票します")
    async def bokete_vote(self, interaction: discord.Interaction, user: discord.Member):
        voter = str(interaction.user.id)
        target = str(user.id)

        if voter in self.data["voted"]:
            return await interaction.response.send_message("あなたはすでに投票済みです。", ephemeral=True)

        if target not in self.data["entries"]:
            return await interaction.response.send_message("そのユーザーはボケを投稿していません。", ephemeral=True)

        self.data["voted"].append(voter)
        self.data["points"][target] = self.data["points"].get(target, 0) + 1
        save_json(DATA_FILE, self.data)

        await interaction.response.send_message(f"🗳️ {user.mention} に投票しました！")

    # ───────────────────────────────
    # 結果発表
    # ───────────────────────────────
    @app_commands.command(name="bokete_result", description="ボケての結果を表示します")
    async def bokete_result(self, interaction: discord.Interaction):
        if not self.data["entries"]:
            return await interaction.response.send_message("投稿がありません。", ephemeral=True)

        points = self.data["points"]
        ranking = sorted(points.items(), key=lambda x: x[1], reverse=True)

        text = ""
        for i, (uid, p) in enumerate(ranking, start=1):
            user = interaction.guild.get_member(int(uid))
            name = user.display_name if user else "Unknown"
            boke = self.data["entries"].get(uid, "（投稿なし）")
            text += f"{i}. **{name}** — {p}票\n　📝 {boke}\n\n"

        embed = discord.Embed(title="🏆 ボケて結果発表！", description=text, color=0xffd700)
        if self.data["image"]:
            embed.set_image(url=self.data["image"])

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Bokete(bot))
