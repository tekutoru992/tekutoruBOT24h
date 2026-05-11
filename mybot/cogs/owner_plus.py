import discord
from discord.ext import commands
from discord import app_commands
import re

OWNER_ID = 1212917780735725609  # てくとるのID

def is_owner(interaction: discord.Interaction):
    return interaction.user.id == OWNER_ID


class OwnerPlus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 強制キック
    @app_commands.command(name="forcekick", description="権限無視で強制キック（てくとる専用）")
    async def forcekick(self, interaction: discord.Interaction, user: discord.Member):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        try:
            await user.kick(reason="Force kick by Tekutoru")
            await interaction.response.send_message(f"{user} を強制キックしました。")
        except Exception as e:
            await interaction.response.send_message(f"キックできませんでした: {e}", ephemeral=True)

    # 強制ロール付与
    @app_commands.command(name="forcerole", description="どんなロールでも強制付与（てくとる専用）")
    async def forcerole(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        try:
            await user.add_roles(role)
            await interaction.response.send_message(f"{user.mention} に {role.name} を強制付与しました。")
        except Exception as e:
            await interaction.response.send_message(f"ロールを付与できませんでした: {e}", ephemeral=True)

    # ゴーストピン
    @app_commands.command(name="ghostping", description="通知だけ残して即削除（てくとる専用）")
    async def ghostping(self, interaction: discord.Interaction, user: discord.Member):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        msg = await interaction.channel.send(user.mention)
        await msg.delete()
        await interaction.response.send_message("👻 ゴーストピン完了", ephemeral=True)

    # てくとるだけが見えるメッセージ
    @app_commands.command(name="invisiblemsg", description="てくとるだけが見えるメッセージ")
    async def invisiblemsg(self, interaction: discord.Interaction, message: str):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        await interaction.response.send_message(message, ephemeral=True)

    # 絵文字コピー（修正版）
    @app_commands.command(name="stealemoji", description="他サーバーの絵文字をコピー（てくとる専用）")
    async def stealemoji(self, interaction: discord.Interaction, emoji: str):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        match = re.search(r"\d{15,20}", emoji)
        if not match:
            return await interaction.response.send_message("絵文字が無効です。", ephemeral=True)

        emoji_id = int(match.group())

        try:
            emoji_obj = await interaction.guild.fetch_emoji(emoji_id)
        except:
            return await interaction.response.send_message("絵文字を取得できませんでした。", ephemeral=True)

        try:
            new_emoji = await interaction.guild.create_custom_emoji(
                name=emoji_obj.name,
                image=await emoji_obj.read()
            )
        except Exception as e:
            return await interaction.response.send_message(f"コピーに失敗しました: {e}", ephemeral=True)

        await interaction.response.send_message(
            f"絵文字をコピーしました: <:{new_emoji.name}:{new_emoji.id}>"
        )

    # チャンネル複製
    @app_commands.command(name="clonechannel", description="チャンネルを丸ごと複製（てくとる専用）")
    async def clonechannel(self, interaction: discord.Interaction):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        await interaction.channel.clone()
        await interaction.response.send_message("📑 チャンネルを複製しました。")

    # 指定ユーザーの発言を全削除
    @app_commands.command(name="wipeuser", description="指定ユーザーの発言を全チャンネルから削除（てくとる専用）")
    async def wipeuser(self, interaction: discord.Interaction, user: discord.Member):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        count = 0
        for channel in interaction.guild.text_channels:
            try:
                async for msg in channel.history(limit=500):
                    if msg.author == user:
                        await msg.delete()
                        count += 1
            except:
                pass

        await interaction.response.send_message(f"{count} 件のメッセージを削除しました。")

    # sudo（なりすまし）
    @app_commands.command(name="sudo", description="Botを使って誰かになりすます（てくとる専用）")
    async def sudo(self, interaction: discord.Interaction, user: discord.Member, message: str):
        if not is_owner(interaction):
            return await interaction.response.send_message("権限がありません。", ephemeral=True)

        webhook = await interaction.channel.create_webhook(name=user.name)
        await webhook.send(message, avatar_url=user.avatar.url if user.avatar else None)
        await webhook.delete()
        await interaction.response.send_message("完了しました。", ephemeral=True)


async def setup(bot):
    await bot.add_cog(OwnerPlus(bot))
