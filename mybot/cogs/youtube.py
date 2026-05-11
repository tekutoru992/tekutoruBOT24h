import discord
from discord import app_commands
from discord.ext import commands

class YoutubeView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(
            label="YouTubeを見る",
            url="https://www.youtube.com/"
        ))

class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="youtube", description="YouTubeリンクを表示します")
    async def youtube(self, interaction: discord.Interaction):
        await interaction.response.send_message("こちらです！", view=YoutubeView())

async def setup(bot):
    await bot.add_cog(Youtube(bot))
