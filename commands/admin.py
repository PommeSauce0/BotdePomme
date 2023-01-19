from discord.ext import commands
import discord


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin is online")

    @commands.command(name="del")
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx, number: int):
        messages = await ctx.channel.purge(limit=number + 1)
        for each_message in messages:
            try:
                await each_message.delete()
            except discord.errors.NotFound:
                pass
            except Exception as e:
                print(f"An error occured: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
