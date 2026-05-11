import discord
from discord.ext import commands
from discord import app_commands

OWNER_ID = 1212917780735725609  # てくとるのID

def is_owner(interaction: discord.Interaction):
    return interaction.user.id == OWNER_ID


class ControlPanel(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    # Kick ボタン
    @discord.ui.button(label="Kick", style=discord.ButtonStyle.danger)
    async def kick(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        await interaction.response.send_message("Kick するユーザーを @メンション してください。", ephemeral=True)

    # Ban ボタン
    @discord.ui.button(label="Ban", style=discord.ButtonStyle.danger)
    async def ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        await interaction.response.send_message("Ban するユーザーを @メンション してください。", ephemeral=True)

    # Shadowban
    @discord.ui.button(label="Shadowban", style=discord.ButtonStyle.secondary)
    async def shadowban(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        await interaction.response.send_message("Shadowban するユーザーを @メンション してください。", ephemeral=True)

    # Wipe（全削除）
    @discord.ui.button(label="Wipe User", style=discord.ButtonStyle.secondary)
    async def wipe(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        await interaction.response.send_message("全削除するユーザーを @メンション してください。", ephemeral=True)

    # チャンネル複製
    @discord.ui.button(label="Clone Channel", style=discord.ButtonStyle.primary)
    async def clone(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        await interaction.channel.clone()
        await interaction.response.send_message("📑 チャンネルを複製しました。", ephemeral=True)

    # 一斉送信
    @discord.ui.button(label="Broadcast", style=discord.ButtonStyle.success)
    async def broadcast(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        await interaction.response.send_message("送信するメッセージを入力してください。", ephemeral=True)


class Panel2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="panel2", description="てくとる専用 GUI 管理パネル")
    async def panel2(self, interaction: discord.Interaction):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        embed = discord.Embed(
            title="👑 てくとる専用 GUI パネル",
            description="ボタンを押して操作してください。",
            color=0xffcc00
        )

        view = ControlPanel(self.bot)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Panel2(bot))
