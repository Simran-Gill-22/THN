import discord
from discord.ext import commands

class GetBans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #returns a list of currently banned users
    @commands.command(pass_context=True, name='GetBans', aliases=['getbanneduser'], no_pm=True)
    async def GetBans(self, ctx):
        #get the banned users
        x = await ctx.guild.bans()
        if not x:
            #if no banned users
            embedVar = discord.Embed(title="No Banned Users", color=0x00ff00)
            await ctx.send(embed=embedVar)
        else:
            #if there are banned users
            embedVar = discord.Embed(title="Banned Users", color=0xff0000)
            for y in x:
                embedVar.add_field(name="Username", value=y.user, inline=False)
                embedVar.add_field(name="Reason", value=y.reason, inline=False)

        return await ctx.send(embed=embedVar)

def setup(bot):
    bot.add_cog(GetBans(bot))