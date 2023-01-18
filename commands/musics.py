import discord
import youtube_dl
from discord import Embed
import asyncio
from discord.ext import commands

musics = {}
queue = []
ytdl_options = {
    'default_search': 'auto'
}
ytdl = youtube_dl.YoutubeDL(ytdl_options)


class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        if 'entries' in video:
            first_video = video['entries'][0]
            self.video_title = first_video['title']
            self.video_url = first_video['webpage_url']
            video_format = video['entries'][0]["formats"][0]
            if 'thumbnails' in first_video:
                self.video_thumbnails = first_video['thumbnail']
            else:
                self.video_thumbnail = 'default_thumbnail_url'
        else:
            self.video_title = video['title']
            self.video_url = video['webpage_url']
            video_format = video["formats"][0]
            if 'thumbnails' in video:
                self.video_thumbnails = video['thumbnail']
            else:
                self.video_thumbnail = 'default_thumbnail_url'
        self.stream_url = video_format["url"]


class Musics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def play_song(self, client, queue, song, ctx):
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song.stream_url, options='-vn -b:a 320k',
                                   before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

        def next(error):
            if error:
                print(f"Error: {error}")
            if len(queue) > 0:
                newsong = queue[0]
                del queue[0]
                self.play_song(client, queue, newsong, ctx)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(), self.bot.loop)

        client.play(source, after=next)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Musics is online")

    @commands.command(name='play', help='Play a song from a YouTube link')
    async def play(self, ctx, *, url):
        client = ctx.guild.voice_client
        video = Video(url)
        if not ctx.guild in musics:
            musics[ctx.guild] = []
        if client and client.channel:
            musics[ctx.guild].append(video)
            await ctx.send("I add it to the waiting list ;)")
        elif not ctx.author.voice:
            await ctx.send("It's not that I don't want to, but you're not in a voice channel :/")
        else:
            channel = ctx.author.voice.channel
            client = await channel.connect()
            await ctx.send("Music time ! Here we gooo !")
            embed = Embed(title='Titre en cours de lecture', color=0x00ff00)
            embed.add_field(name='Titre', value=video.video_title)
            embed.set_image(url=video.video_thumbnails)
            embed.add_field(name='lien', value=video.video_url)
            await ctx.send(embed=embed)
            self.play_song(client, musics[ctx.guild], video, ctx)

    @commands.command(name='skip', help='Skip the currentsong')
    async def skip(self, ctx):
        video = musics[ctx.guild][0]
        client = ctx.guild.voice_client
        if client and client.channel:
            if musics[ctx.guild]:
                embed = Embed(title='Titre en cours de lecture', color=0x00ff00)
                embed.add_field(name='Titre', value=video.video_title)
                embed.set_image(url=video.video_thumbnails)
                embed.add_field(name='lien', value=video.video_url)
                await ctx.send(embed=embed)
                client.stop()
            else:
                await ctx.send("No more songs in the queue.")
        else:
            await ctx.send("I'm not currently playing any music.")

    @commands.command()
    async def leave(self, ctx):
        client = ctx.guild.voice_client
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if not ctx.author.voice:
            await ctx.send("It's not that I don't want to, but you're not in a voice channel :/")
        elif not ctx.voice_client:
            await ctx.send(
                "I am not connected to a voice channel. BUT YOU WOULD KNOW THAT IF YOU PAID MORE ATTENTION TO ME!!! :(")
        elif ctx.author.voice.channel.id != client.channel.id:
            await ctx.send("So we want to annoy the people who take advantage of the bot ?")
        elif ctx.voice_client is not None:
            musics[ctx.guild] = []
            await voice.disconnect()
            await ctx.send("I'm disconnecting because I wanted to. Not because you asked me to. Ba.. baka !")

    @commands.command()
    async def stop(self, ctx):
        client = ctx.guild.voice_client
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if not ctx.author.voice:
            await ctx.send("It's not that I don't want to, but you're not in a voice channel :/")
        elif not ctx.voice_client:
            await ctx.send(
                "I am not connected to a voice channel. BUT YOU WOULD KNOW THAT IF YOU PAID MORE ATTENTION TO ME!!! :(")
        elif ctx.author.voice.channel.id != client.channel.id:
            await ctx.send("So we want to annoy the people who take advantage of the bot ?")
        elif ctx.voice_client is not None:
            musics[ctx.guild] = []
            await voice.disconnect()
            await ctx.send("As there is no more music in the queue, I allow myself to go there :)")

    @commands.command()
    async def pause(self, ctx):
        client = ctx.guild.voice_client

        if not ctx.author.voice:
            await ctx.send("It's not that I don't want to, but you're not in a voice channel :/")
        elif ctx.author.voice.channel.id != client.channel.id:
            await ctx.send("So we want to annoy the people who take advantage of the bot?")
        elif not client.is_paused():
            client.pause()
            await ctx.send("Did you think you were Dr. Strange or what? Well you're right, you just paused the music !")
        else:
            await ctx.send("The music is already paused, Dr. Strange.")

    @commands.command()
    async def resume(self, ctx):
        client = ctx.guild.voice_client

        if not ctx.author.voice:
            await ctx.send("It's not that I don't want to, but you're not in a voice channel :/")
        elif ctx.author.voice.channel.id != client.channel.id:
            await ctx.send("So we want to annoy the people who take advantage of the bot ?")
        elif client.is_paused():
            await ctx.send("(ah shit) Here we go again")
            client.resume()
        else:
            await ctx.send("The music is already playing! You don't want me to put it on x2 either? (That's no)")


async def setup(bot: commands.Bot):
    await bot.add_cog(Musics(bot))
