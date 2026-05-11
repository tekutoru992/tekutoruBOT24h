import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log = discord.utils.get(message.guild.text_channels, name="bot-log")
        if log:
            await log.send(f"🗑️ 削除: {message.author} → {message.content}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            log = discord.utils.get(before.guild.text_channels, name="bot-log")
            if log:
                await log.send(f"✏️ 編集: {before.author}\n前: {before.content}\n後: {after.content}")

async def setup(bot):
    await bot.add_cog(Logs(bot))
