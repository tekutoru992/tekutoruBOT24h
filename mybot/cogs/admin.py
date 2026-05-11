import discord
from discord import app_commands
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="ユーザーをBANします")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("権限がありません。", ephemeral=True)
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member} をBANしました。")

    @app_commands.command(name="unban", description="ユーザーをUNBANします")
    async def unban(self, interaction: discord.Interaction, username: str):
        banned = await interaction.guild.bans()
        name, tag = username.split("#")
        for entry in banned:
            if entry.user.name == name and entry.user.discriminator == tag:
                await interaction.guild.unban(entry.user)
                return await interaction.response.send_message(f"{entry.user} をUNBANしました。")
        await interaction.response.send_message("見つかりませんでした。")

    @app_commands.command(name="kick", description="ユーザーをKickします")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if not interaction.user.guild_permissions.kick_members:
            return await interaction.response.send_message("権限がありません。", ephemeral=True)
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member} をKickしました。")

    @app_commands.command(name="clear", description="メッセージを削除します")
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"{amount}件削除しました。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
