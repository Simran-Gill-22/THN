import discord
from discord import channel
from discord.ext import commands

from Modules.FolderBuilder import FolderBuilder

class NewImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #provides a new image to the channel
    @commands.command(pass_context=True, name='NewImage', aliases=['newimage'], no_pm=True)
    async def NewImage(self, ctx):
        #get the current channel name
        CurrentChannel = ctx.message.channel.name
        #list of allowed channels
        AllowedChannels = ['magic-mike-appreciation-society', 'chris-roberts-appreciation-society', 'keanu-reeves-appreciation-society']
        #go through all the channels in the allowed list
        for Channel in AllowedChannels:
            #if a channel from the list matches the channel a command is sent from
            if Channel == CurrentChannel:
                #build an image path
                path = FolderBuilder(CurrentChannel)
                #pushes the image
                await ctx.send(file=discord.File(path))
                #prevent the script from running further
                return
        #initialising a variable
        AllowedChannelsList = ''
        #go through the channel list
        for Channel in AllowedChannels:
            #concat the list into a string with linebreaks 
            AllowedChannelsList += f'\n{Channel}'
        #return a message stating it is not a valid channel
        return await ctx.send(f'No image to post to this channel, please try one of the following: {AllowedChannelsList}')

def setup(bot):
    bot.add_cog(NewImage(bot))