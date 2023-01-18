import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path="config/config")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


class BotdePomme(commands.Bot):
    def __init__(self):
        # Intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True

        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        prefix = '"!"'
        print('Logged in as {0.user} with the prefix '.format(self) + f'{prefix}\t' + str(datetime.now()))

    async def on_command_error(self, ctx, error):
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


async def load(bot: commands.Bot):
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')


async def main(bot: commands.Bot, token):
    async with bot:
        await load(bot)
        await bot.start(token)


token = os.getenv("token")

if __name__ == "__main__":
    asyncio.run(main(BotdePomme(), token))
