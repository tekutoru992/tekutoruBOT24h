import discord
from discord.ext import commands
import os
import asyncio

TOKEN = os.getenv("TOKEN")  # Railway 用（環境変数から読み込む）

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ───────────────────────────────
#  COG 自動読み込み
# ───────────────────────────────
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded: {filename}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")
    print("すべてのCogを読み込みました。")


# ───────────────────────────────
#  Bot 起動時
# ───────────────────────────────
@bot.event
async def on_ready():
    print(f"ログイン完了: {bot.user}")
    try:
        await bot.tree.sync()
        print("スラッシュコマンドを同期しました。")
    except Exception as e:
        print(f"同期エラー: {e}")


# ───────────────────────────────
#  メイン処理（Railway 対応）
# ───────────────────────────────
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


asyncio.run(main())
