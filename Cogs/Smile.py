import discord
from discord.ext import commands

class Smile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #post the smile meme
    @commands.command(pass_context=True, name='Smile', aliases=['sendsmilememe'], no_pm=True)
    async def Smile(self, ctx):
        #image location
        path = 'Memes/Smile.jpg'
        #pushes the image
        return await ctx.send(file=discord.File(path))

def setup(bot):
    bot.add_cog(Smile(bot))