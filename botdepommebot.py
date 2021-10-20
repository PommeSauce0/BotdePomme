import os
import random
import discord
import youtube_dl
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import asyncio

load_dotenv(dotenv_path="config") 

ytdl_options = {
    'default_search': 'auto'
}
ytdl = youtube_dl.YoutubeDL(ytdl_options)

musics = {}

class botdepommebot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", help_command=None)

    async def on_ready(self):
        prefix = '"!"'
        print('Logged in as {0.user} with the prefix '.format(self) + f'{prefix}\t' + str(datetime.now()))


bot = botdepommebot()


class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        if 'entries' in video:
            video_format = video['entries'][0]["formats"][0]
        elif 'formats' in video:
            video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send(f"Error: Missing Required Argument // {error}")
        print("Error: MissingRequiredArgument")
    elif isinstance(error, commands.BadArgument):
        await ctx.channel.send(f"Error: Bad Argument // {error}")
        print("Error: Bad Argument")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.channel.send(f"Error: Missing Permissions // {error}")
        print("Error: Missing Permissions")
    elif isinstance(error, commands.ChannelNotReadable):
        await ctx.channel.send(f'Error: Channel Not Readable // {error}')
        print("Error: Channel Not Readable")
    else:
        print(f"Error: Unknown // {error}")


@bot.command()
async def play(ctx, *, url):
    client = ctx.guild.voice_client
    video = Video(url)

    if client and client.channel:
        musics[ctx.guild].append(video)
        await ctx.send("I add it to the waiting list ;)")
    elif not ctx.author.voice:
        await ctx.send("It's not that I don't want to, but you're not in a voice channel :/")
    else:
        channel = ctx.author.voice.channel
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send("Music time ! Here we gooo !")
        play_song(client, musics[ctx.guild], video)


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
                                                                 , before_options="-reconnect 1 -reconnect_streamed 1 "
                                                                                  "-reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            newsong = queue[0]
            del queue[0]
            play_song(client, queue, newsong)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    # ctx.author.voice.channel.id = channel in which the user is (voice)
    # client.channel.id = channel in which the bot is located

    if not ctx.author.voice:
        await ctx.send("It's not that I don't want to, but you're not in a voice channel :/")
    elif not ctx.voice_client:
        await ctx.send("You know that if I don't play music... I'm gonna have a hard time skipping huh ?")
    elif ctx.author.voice.channel.id != client.channel.id:
        await ctx.send("So we want to annoy the people who take advantage of the bot ?")
    else:
        client.stop()
        await ctx.send(
            "Well then ? You don't like this one ? No problem, let's go to the next one !")


@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not ctx.author.voice:
        await ctx.send("It's not that I don't want to, but you're not in a voice channel :/")
    elif not ctx.voice_client:
        await ctx.send("I am not connected to a voice channel. BUT YOU WOULD KNOW THAT IF YOU PAID MORE ATTENTION TO ME!!! :(")
    elif ctx.author.voice.channel.id != client.channel.id:
        await ctx.send("So we want to annoy the people who take advantage of the bot ?")
    elif ctx.voice_client is not None:
        musics[ctx.guild] = []
        await voice.disconnect()
        await ctx.send("I'm disconnecting because I wanted to. Not because you asked me to. Ba.. baka !")


@bot.command()
async def stop(ctx):
    client = ctx.guild.voice_client
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not ctx.author.voice:
        await ctx.send("It's not that I don't want to, but you're not in a voice channel :/")
    elif not ctx.voice_client:
        await ctx.send("I am not connected to a voice channel. BUT YOU WOULD KNOW THAT IF YOU PAID MORE ATTENTION TO ME!!! :(")
    elif ctx.author.voice.channel.id != client.channel.id:
        await ctx.send("So we want to annoy the people who take advantage of the bot ?")
    elif ctx.voice_client is not None:
        musics[ctx.guild] = []
        await voice.disconnect()
        await ctx.send("As there is no more music in the queue, I allow myself to go there :)")


@bot.command()
async def pause(ctx):
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


@bot.command()
async def resume(ctx):
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


@bot.command(name="del")
@commands.has_permissions(administrator=True)
async def delete(ctx, number: int):
    messages = await ctx.channel.history(limit=number + 1).flatten()

    for each_message in messages:
        await each_message.delete()


@bot.command()
async def pof(ctx):
    cpof = ["heads", "tails", "the coin did not fall :D you owe me 2€"]
    await ctx.send("*throws the coin in the air*")
    await asyncio.sleep(3)
    await ctx.send("*Noise of a piece spinning in the air because I have too much force*")
    await asyncio.sleep(2)

    dpof = random.choice(cpof)
    if not dpof == "the coin did not fall :D you owe me 2€": 
        await ctx.send("It's {}".format(dpof))
    else:
        await ctx.send(dpof)


@bot.command()
async def help(ctx):
    prefix = '!'
    embed = discord.Embed(title='BotdePomme', color=0xB0D7FB)
    embed.set_thumbnail(url=bot.user.avatar_url)

    embed.add_field(name=f'{prefix}help',
                    value=f'So that I can make this message appear ;).\nExample: {prefix}help (if you are reading this '
                          f'that you have succeeded normally)',
                    inline=False)
    embed.add_field(name=f'{prefix}play',
                    value=f'This command allows the bot to search for you, to find you, and to play the music '
                          f' you have asked it to play. \nExample: {prefix}play *link yt or word* ',
                    inline=False)
    embed.add_field(name=f'{prefix}skip',
                    value=f'This command allows you to skip the current music to go to the next one.',
                    inline=False)
    embed.add_field(name=f'{prefix}pause',
                    value=f'Do I really need to explain? YES?? Well... pause the music in progress.',
                    inline=False)
    embed.add_field(name=f'{prefix}resume',
                    value=f'If the music is paused, then stop the pause.',
                    inline=False)
    embed.add_field(name=f'{prefix}leave ou {prefix}stop',
                    value=f'I... I... It\'s disconnecting me from the voice channel... Don\'t you dare do that, '
                          f'huh ? UwU',
                    inline=False)
    embed.add_field(name=f'{prefix}pof',
                    value=f'Heads or tails. BASIC \nExample: {prefix}pof',
                    inline=False)
    embed.add_field(name=f'{prefix}del (ADMIN ONLY)',
                    value=f'Delete messages. \nExample: {prefix}del *number of messages*',
                    inline=False)
    embed.set_footer(text='By PommeSauce0')
    await ctx.channel.send(embed=embed)

bot.run(os.getenv("token"))
