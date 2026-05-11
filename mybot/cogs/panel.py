import discord
from discord.ext import commands
from discord import app_commands

# -------------------------
# 管理パネルのボタン
# -------------------------
class AdminPanelButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="BAN", style=discord.ButtonStyle.danger)
    async def ban_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("BAN するユーザーを選んでください： `/ban @ユーザー`", ephemeral=True)

    @discord.ui.button(label="KICK", style=discord.ButtonStyle.danger)
    async def kick_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("KICK するユーザーを選んでください： `/kick @ユーザー`", ephemeral=True)

    @discord.ui.button(label="CLEAR", style=discord.ButtonStyle.primary)
    async def clear_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("削除する数を入力： `/clear 10`", ephemeral=True)

    @discord.ui.button(label="サーバー情報", style=discord.ButtonStyle.secondary)
    async def serverinfo_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        embed = discord.Embed(title="サーバー情報", color=0x00ffcc)
        embed.add_field(name="名前", value=guild.name)
        embed.add_field(name="メンバー数", value=guild.member_count)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="ユーザー情報", style=discord.ButtonStyle.secondary)
    async def userinfo_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        embed = discord.Embed(title="ユーザー情報", color=0x00ffcc)
        embed.add_field(name="名前", value=member.name)
        embed.add_field(name="ID", value=member.id)
        embed.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)


# -------------------------
# メニュー（ロール付与など）
# -------------------------
class AdminSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="ロール付与", description="ユーザーにロールを付ける"),
            discord.SelectOption(label="ロール削除", description="ユーザーのロールを外す"),
            discord.SelectOption(label="ミュート", description="ユーザーをミュートする"),
            discord.SelectOption(label="タイムアウト", description="ユーザーをタイムアウトする"),
        ]
        super().__init__(placeholder="管理アクションを選択", options=options)

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]

        if choice == "ロール付与":
            await interaction.response.send_message("ロール付与： `/addrole @ユーザー @ロール`", ephemeral=True)

        elif choice == "ロール削除":
            await interaction.response.send_message("ロール削除： `/removerole @ユーザー @ロール`", ephemeral=True)

        elif choice == "ミュート":
            await interaction.response.send_message("ミュート： `/mute @ユーザー`", ephemeral=True)

        elif choice == "タイムアウト":
            await interaction.response.send_message("タイムアウト： `/timeout @ユーザー 10m`", ephemeral=True)


class AdminPanelSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(AdminSelect())


# -------------------------
# Cog 本体
# -------------------------
class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="panel", description="てくとる専用の管理パネルを表示します")
    async def panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="てくとる専用 管理パネル",
            description="下のボタンとメニューから操作できます。",
            color=0x00ffcc
        )
        await interaction.response.send_message(
            embed=embed,
            view=AdminPanelButtons(),
            ephemeral=False
        )
        await interaction.followup.send(
            "追加アクションはこちら：",
            view=AdminPanelSelect(),
            ephemeral=False
        )


async def setup(bot):
    await bot.add_cog(Panel(bot))
