import discord
from discord.ext import commands
from discord import app_commands

TARGET_USER_ID = 1212917780735725609  # 例: 123456789012345678

class NowPlaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="gamecheck", description="てくとるが今プレイしているゲームを表示します")
    async def nowplaying(self, interaction: discord.Interaction):
        user = interaction.guild.get_member(TARGET_USER_ID)

        if user is None:
            await interaction.response.send_message("ユーザーが見つかりません。", ephemeral=True)
            return

        # アクティビティ（ゲーム）を取得
        activity = user.activity

        if activity is None:
            await interaction.response.send_message("てくとるは今ゲームをプレイしていません。", ephemeral=False)
            return

        # ゲーム名を取得
        game_name = activity.name

        embed = discord.Embed(
            title="🎮 てくとるの現在のプレイ状況",
            description=f"**{game_name}** をプレイ中です！",
            color=0x00ffcc
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(NowPlaying(bot))
