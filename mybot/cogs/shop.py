import discord
from discord.ext import commands
from discord import app_commands
import json
import os

SHOP_FILE = "shop_items.json"
INV_FILE = "inventory.json"
COIN_FILE = "coins.json"


def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4, ensure_ascii=False)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shop = load_json(SHOP_FILE, {
            "items": {
                "VIP": 5000,
                "ガチャ券": 1000,
                "経験値ブースト": 300,
                "称号：勇者": 2000
            }
        })
        self.inventory = load_json(INV_FILE, {})
        self.coins = load_json(COIN_FILE, {})

    def get_coins(self, user_id):
        uid = str(user_id)
        return self.coins.get(uid, {}).get("coins", 0)

    def add_item(self, user_id, item):
        uid = str(user_id)
        if uid not in self.inventory:
            self.inventory[uid] = []
        self.inventory[uid].append(item)
        save_json(INV_FILE, self.inventory)

    def remove_coins(self, user_id, amount):
        uid = str(user_id)
        if uid not in self.coins:
            return False
        if self.coins[uid]["coins"] < amount:
            return False
        self.coins[uid]["coins"] -= amount
        save_json(COIN_FILE, self.coins)
        return True

    # ショップ一覧
    @app_commands.command(name="shop", description="ショップの商品一覧を表示します")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🛒 ショップ", color=0x00ff99)
        for item, price in self.shop["items"].items():
            embed.add_field(name=item, value=f"{price} コイン", inline=False)
        await interaction.response.send_message(embed=embed)

    # 購入
    @app_commands.command(name="buy", description="アイテムを購入します")
    async def buy(self, interaction: discord.Interaction, item: str):
        item_list = self.shop["items"]

        if item not in item_list:
            return await interaction.response.send_message("そのアイテムは存在しません。", ephemeral=True)

        price = item_list[item]
        user_coins = self.get_coins(interaction.user.id)

        if user_coins < price:
            return await interaction.response.send_message("💸 コインが足りません。", ephemeral=True)

        self.remove_coins(interaction.user.id, price)
        self.add_item(interaction.user.id, item)

        await interaction.response.send_message(
            f"🛒 {interaction.user.mention} が **{item}** を {price} コインで購入しました！"
        )

    # 所持アイテム
    @app_commands.command(name="inventory", description="自分の所持アイテムを確認します")
    async def inventory(self, interaction: discord.Interaction):
        uid = str(interaction.user.id)
        items = self.inventory.get(uid, [])

        if not items:
            return await interaction.response.send_message("🎒 所持アイテムはありません。")

        text = "\n".join([f"- {i}" for i in items])
        embed = discord.Embed(title="🎒 所持アイテム", description=text, color=0x00ccff)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Shop(bot))
