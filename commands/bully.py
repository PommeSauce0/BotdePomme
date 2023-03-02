from discord.ext import commands
import discord
import asyncio
import random


class Bully(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Les commandes de harcelement sont connectées.")

    @commands.command(name="bully")
    @commands.has_permissions(administrator=True)
    async def bully(self, ctx, member: discord.Member):
        def check(message):
            return message.author == member and message.channel == ctx.channel

        await ctx.send(f"Je vais bully {member} bien comme il faut.")

        bully_word = open("./config/bully_list.txt", "r")
        bahaha = bully_word.read().split(',')

        async def bully_loop():
            while True:
                message = await self.bot.wait_for('message', check=check)
                await message.channel.send(random.choice(bahaha))
                if message.content.lower() in ['azewsxrdctfvygbuhniyutrxezwrxedtcytvuybiunoinuytvcrxewiuniyutgvyfctd6489198189184191981981']:
                    break

        task = asyncio.create_task(bully_loop())
        try:
            await task
        finally:
            await ctx.send(f"Arrêt du bully pour {member.mention}.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Bully(bot))
