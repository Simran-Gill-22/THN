import discord
from discord.ext import commands

from Modules.PathExist import PathExist
from Modules.Error import Error

class SmileMeme(commands.Cog):
    'This category handles smile meme'
    def __init__(self, bot):
        self.bot = bot

    #post the smile meme
    @commands.command(pass_context=True, name='Smile', aliases=['sendsmilememe'], no_pm=True)
    async def Smile(self, ctx):
        "Sends a meme image"
        #image location
        path = 'Memes/Smile.jpg'
        if PathExist(path):
            #if yes pushes the image
            return await ctx.send(file=discord.File(path))
        else:
            #send an error
            #set error title and message
            Title = str('Can\'t find image')
            Content = str(f'Image can\'t be posted, check logs to know more')
            #send the embeded message
            await ctx.send(embed = Error(Title, Content))

def setup(bot):
    bot.add_cog(SmileMeme(bot))