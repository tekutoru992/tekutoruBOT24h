import discord
from discord.ext import commands

LOG_CHANNEL_NAME = "tkt-log"  # てくとる専用ログチャンネル

class AdminLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # BAN ログ
    # -------------------------
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
        if channel:
            embed = discord.Embed(
                title="🚫 BAN 実行",
                description=f"{user} が BAN されました。",
                color=0xff0000
            )
            await channel.send(embed=embed)

    # -------------------------
    # UNBAN ログ
    # -------------------------
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
        if channel:
            embed = discord.Embed(
                title="♻️ UNBAN 実行",
                description=f"{user} の BAN が解除されました。",
                color=0x00ff00
            )
            await channel.send(embed=embed)

    # -------------------------
    # KICK ログ
    # -------------------------
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # KICK と退出の区別は難しいが、管理者操作は panel 側でログを送る
        pass

    # -------------------------
    # メッセージ削除ログ（CLEAR）
    # -------------------------
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = discord.utils.get(message.guild.text_channels, name=LOG_CHANNEL_NAME)
        if channel and not message.author.bot:
            embed = discord.Embed(
                title="🗑️ メッセージ削除",
                description=f"**{message.author}** のメッセージが削除されました。",
                color=0xff8800
            )
            embed.add_field(name="内容", value=message.content)
            await channel.send(embed=embed)

    # -------------------------
    # ロール変更ログ
    # -------------------------
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        channel = discord.utils.get(after.guild.text_channels, name=LOG_CHANNEL_NAME)
        if not channel:
            return

        # ロール追加
        if len(after.roles) > len(before.roles):
            added = list(set(after.roles) - set(before.roles))[0]
            embed = discord.Embed(
                title="➕ ロール付与",
                description=f"{after.mention} に **{added.name}** が付与されました。",
                color=0x00ffcc
            )
            await channel.send(embed=embed)

        # ロール削除
        elif len(after.roles) < len(before.roles):
            removed = list(set(before.roles) - set(after.roles))[0]
            embed = discord.Embed(
                title="➖ ロール削除",
                description=f"{after.mention} から **{removed.name}** が削除されました。",
                color=0xffcc00
            )
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdminLog(bot))
