import discord
from discord.ext import commands

from Modules.PathExist import PathExist
from Modules.Error import Error

class MoneyMeme(commands.Cog):
    'This class handles the Chris Roberts money meme'
    def __init__(self, bot):
        self.bot = bot

    #posts the cr money meme
    @commands.command(pass_context=True, name='Money', aliases=['sendmoneymeme'], no_pm=True)
    async def Money(self, ctx):
        'This sends the money meme to the channel it is sent'
        #image location
        path = 'Memes/Money.jpg'
        #check if the file exist
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
    bot.add_cog(MoneyMeme(bot))