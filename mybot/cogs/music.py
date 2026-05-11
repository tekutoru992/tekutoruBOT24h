import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio

from utils.player import MusicPlayer

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    def get_player(self, guild_id):
        if guild_id not in self.players:
            self.players[guild_id] = MusicPlayer()
        return self.players[guild_id]

    @app_commands.command(name="play", description="音楽を再生します（高音質＋キュー対応）")
    async def play(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer()

        voice = interaction.user.voice
        if not voice:
            return await interaction.followup.send("ボイスチャンネルに参加してください。")

        channel = voice.channel
        guild = interaction.guild
        player = self.get_player(guild.id)

        if not guild.voice_client:
            await channel.connect()

        # YouTube から音源取得
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info["url"]
            title = info["title"]

        # キューに追加
        await player.add_song({"url": audio_url, "title": title})

        await interaction.followup.send(f"🎵 キューに追加: **{title}**")

        # 再生ループが動いていなければ開始
        if not guild.voice_client.is_playing():
            self.bot.loop.create_task(self.start_playing(guild))

    async def start_playing(self, guild):
        player = self.get_player(guild.id)

        while True:
            song = await player.get_next_song()
            source = discord.FFmpegPCMAudio(song["url"], **FFMPEG_OPTIONS)

            guild.voice_client.play(
                source,
                after=lambda e: player.play_next_song.set()
            )

            # 再生中メッセージ
            channel = guild.system_channel or guild.text_channels[0]
            await channel.send(f"▶️ 再生中: **{song['title']}**")

            await player.play_next_song.wait()

            if player.queue.empty():
                await guild.voice_client.disconnect()
                break

    @app_commands.command(name="skip", description="曲をスキップします")
    async def skip(self, interaction: discord.Interaction):
        guild = interaction.guild
        player = self.get_player(guild.id)

        if guild.voice_client and guild.voice_client.is_playing():
            player.skip()
            guild.voice_client.stop()
            await interaction.response.send_message("⏭️ スキップしました。")
        else:
            await interaction.response.send_message("再生中の曲がありません。")

    @app_commands.command(name="stop", description="音楽を停止します")
    async def stop(self, interaction: discord.Interaction):
        guild = interaction.guild
        player = self.get_player(guild.id)

        if guild.voice_client:
            player.queue = asyncio.Queue()
            guild.voice_client.stop()
            await guild.voice_client.disconnect()
            await interaction.response.send_message("⏹️ 停止しました。")
        else:
            await interaction.response.send_message("ボイスチャンネルに接続していません。")

    @app_commands.command(name="queue", description="キューを表示します")
    async def queue(self, interaction: discord.Interaction):
        guild = interaction.guild
        player = self.get_player(guild.id)

        if player.queue.empty():
            return await interaction.response.send_message("キューは空です。")

        items = list(player.queue._queue)
        text = "\n".join([f"- {item['title']}" for item in items])

        await interaction.response.send_message(f"📜 **キュー一覧**\n{text}")

    @app_commands.command(name="nowplaying", description="再生中の曲を表示します")
    async def nowplaying(self, interaction: discord.Interaction):
        guild = interaction.guild
        player = self.get_player(guild.id)

        if not player.now_playing:
            return await interaction.response.send_message("再生中の曲はありません。")

        await interaction.response.send_message(f"▶️ **再生中**: {player.now_playing['title']}")

async def setup(bot):
    await bot.add_cog(Music(bot))
