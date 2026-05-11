import discord
from discord.ext import commands
from discord import app_commands

OWNER_ID = 1212917780735725609  # ← てくとるのID

def is_owner(interaction: discord.Interaction):
    return interaction.user.id == OWNER_ID

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # オーナー情報
    @app_commands.command(name="owner", description="Botのオーナー情報（てくとる専用）")
    async def owner(self, interaction: discord.Interaction):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        embed = discord.Embed(
            title="👑 Botオーナー",
            description="このBotの唯一のオーナーは **てくとる** です。",
            color=0xffcc00
        )
        await interaction.response.send_message(embed=embed)

    # 一斉送信
    @app_commands.command(name="broadcast", description="サーバー全体にメッセージ送信（てくとる専用）")
    async def broadcast(self, interaction: discord.Interaction, message: str):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        for channel in interaction.guild.text_channels:
            try:
                await channel.send(f"📢 **Broadcast:** {message}")
            except:
                pass

        await interaction.response.send_message("送信完了しました。")

    # シャドウバン（発言を見えなくする）
    @app_commands.command(name="shadowban", description="指定ユーザーの発言を隠します（てくとる専用）")
    async def shadowban(self, interaction: discord.Interaction, user: discord.Member):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False

        for channel in interaction.guild.text_channels:
            await channel.set_permissions(user, overwrite=overwrite)

        await interaction.response.send_message(f"{user.mention} をシャドウバンしました。")

    # サーバー情報
    @app_commands.command(name="serverstats", description="サーバー情報を表示（てくとる専用）")
    async def serverstats(self, interaction: discord.Interaction):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        guild = interaction.guild
        embed = discord.Embed(title="📊 サーバー情報", color=0x00ffcc)
        embed.add_field(name="サーバー名", value=guild.name)
        embed.add_field(name="メンバー数", value=guild.member_count)
        embed.add_field(name="チャンネル数", value=len(guild.channels))
        embed.add_field(name="ロール数", value=len(guild.roles))
        embed.add_field(name="作成日", value=guild.created_at.strftime("%Y-%m-%d"))
        await interaction.response.send_message(embed=embed)

    # Botに喋らせる
    @app_commands.command(name="sayasbot", description="Botにメッセージを喋らせる（てくとる専用）")
    async def sayasbot(self, interaction: discord.Interaction, message: str):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        await interaction.channel.send(message)
        await interaction.response.send_message("送信しました。", ephemeral=True)

    # DM送信
    @app_commands.command(name="dm", description="指定ユーザーにDMを送る（てくとる専用）")
    async def dm(self, interaction: discord.Interaction, user: discord.Member, message: str):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        try:
            await user.send(message)
            await interaction.response.send_message("DMを送信しました。")
        except:
            await interaction.response.send_message("DMを送れませんでした。", ephemeral=True)

    # 大量削除
    @app_commands.command(name="purge", description="大量削除（てくとる専用）")
    async def purge(self, interaction: discord.Interaction, amount: int):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"{amount} 件削除しました。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Owner(bot))
