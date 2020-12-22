import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='Kick', aliases=['kickuser'], no_pm=True)
    async def Kick(ctx, *, member : discord.Member = None):
    #     if not ctx.message.author.server_permissions.administrator:
    #         return
    #     channel = ctx.channel
    #     if not member:
    #         return await channel.send(ctx.message.author.mention + "Specify a user to kick!")
    #     try:
    #         await client.kick(member)
    #     except Exception as e:
    #         if 'Privilege is too low' in str(e):
    #             return await channel.send(":x: Privilege too low!")
    #     embed = discord.Embed(description = "**%s** has been kicked!"%member.name, color = 0xFF0000)
        return

def setup(bot):
    bot.add_cog(Kick(bot))