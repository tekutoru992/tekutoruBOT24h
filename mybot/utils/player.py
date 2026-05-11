import asyncio

class MusicPlayer:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.now_playing = None
        self.play_next_song = asyncio.Event()

    async def add_song(self, song):
        await self.queue.put(song)

    async def get_next_song(self):
        self.play_next_song.clear()
        song = await self.queue.get()
        self.now_playing = song
        return song

    def skip(self):
        self.play_next_song.set()
