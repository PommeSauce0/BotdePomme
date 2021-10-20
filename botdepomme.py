import os
import discord
import youtube_dl
from dotenv import load_dotenv
from datetime import datetime
import random
from datetime import datetime
from asyncio import sleep
import asyncio

load_dotenv(dotenv_path="config")
default_intents = discord.Intents.default()
default_intents.members = True
default_intents.guilds = True

client = discord.Client(intents=default_intents)

@client.event
async def on_ready():
    print('Connecté en tant que {0.user} '.format(client) + str(datetime.now()))
    
    
async def status_task():
    await client.wait_until_ready()

    music = []
    film = ['Re:Zero']
    stream = []
    game = ['Minecraft', 'League of Legends', 'Epic Seven']
    
    while True:
        games = random.choice(game)
        streams = random.choice(stream)
        films = random.choice(film)
        musics = random.choice(music)
        activity = [await client.change_presence(activity=discord.Streaming(name='Un bon streameur', url=streams)),
                    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=musics)),
                    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=films)),
                    await client.change_presence(activity=discord.Game(name=games))]
        random.choice(activity)
        await asyncio.sleep(120)

@client.event
async def on_member_join(member):
    channel = member.guild.system_channel
    await channel.send(content=f"Welcome {member.display_name} !")
        
client.loop.create_task(status_task())
client.run(os.getenv("token"))

