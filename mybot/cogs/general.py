import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="挨拶します")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("こんにちは！")

    @app_commands.command(name="userinfo", description="ユーザー情報を表示します")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title="ユーザー情報", color=0x00ffcc)
        embed.add_field(name="名前", value=member.name)
        embed.add_field(name="ID", value=member.id)
        embed.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="サーバー情報を表示します")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title="サーバー情報", color=0x00ffcc)
        embed.add_field(name="名前", value=guild.name)
        embed.add_field(name="メンバー数", value=guild.member_count)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
