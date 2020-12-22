import discord
from discord.ext import commands

class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #posts the cr money meme
    @commands.command(pass_context=True, name='Money', aliases=['sendmoneymeme'], no_pm=True)
    async def Money(self, ctx):
        #image location
        path = 'Memes/Money.jpg'
        #pushes the image
        return await ctx.send(file=discord.File(path))

def setup(bot):
    bot.add_cog(Money(bot))