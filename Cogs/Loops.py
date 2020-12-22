import asyncio
import random
import discord
from discord.ext import commands, tasks
from discord.utils import get
from Modules.FolderBuilder import FolderBuilder

class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot       
        self.mm_image_loop.start()
        self.kr_image_loop.start()
        self.cr_image_loop.start()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.CreateChannels()
    
    def cog_unload(self):
        self.mm_image_loop.stop()
        self.kr_image_loop.stop()
        self.cr_image_loop.stop()

    #mm posting loop
    @tasks.loop(seconds=random.randint(28800, 57600), count=None)
    async def mm_image_loop(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(3)
        print("mm loop has started")
        #define channel
        channel_name = 'magic-mike-appreciation-society'
        #finds all channels
        channel = get(self.bot.get_all_channels(), name=channel_name) 
        #if the channel is not found 
        if not channel:
            #call the function to create the channel
            self.CreateChannels()
            #get the channel object again
            channel = get(self.bot.get_all_channels(), name=channel_name) 
        #Call folder builder to make the image
        path = FolderBuilder(channel_name)
        #pushes the image
        await channel.send(file=discord.File(path))
    
    #cr posting loop
    @tasks.loop(seconds=random.randint(28800, 57600), count=None)
    async def cr_image_loop(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(3)
        print("cr loop has started")
        #define channel
        channel_name = 'chris-roberts-appreciation-society'
        #finds all channels
        channel = get(self.bot.get_all_channels(), name=channel_name) 
                #if the channel is not found 
        if not channel:
            #call the function to create the channel
            self.CreateChannels()
            #get the channel object again
            channel = get(self.bot.get_all_channels(), name=channel_name) 
        #Call folder builder to make the image
        path = FolderBuilder(channel_name)
        #pushes the image
        await channel.send(file=discord.File(path))

    #kr posting loop
    @tasks.loop(seconds=random.randint(28800, 57600), count=None)
    async def kr_image_loop(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(3)
        print("kr loop has started")
        #define channel
        channel_name = 'keanu-reeves-appreciation-society'
        #finds all channels
        channel = get(self.bot.get_all_channels(), name=channel_name) 
        #if the channel is not found 
        if not channel:
            #call the function to create the channel
            self.CreateChannels()
            #get the channel object again
            channel = get(self.bot.get_all_channels(), name=channel_name) 
        #Call folder builder to make the image
        path = FolderBuilder(channel_name)
        #pushes the image
        await channel.send(file=discord.File(path))

    #this checks all the channels are present and in the correct categories 
    @commands.command(pass_context=True, name='CreateChannels', aliases=['createchannels'], no_pm=True)
    async def CreateChannels(self):
        #wait until the bot is ready
        await self.bot.wait_until_ready()
        #creates the categories and channels to be used by the loop
        CategoryName = 'Appreciation Society'
        channel_name = ['magic-mike-appreciation-society', 'chris-roberts-appreciation-society', 'keanu-reeves-appreciation-society']  
        #get all the guilds the bot is in
        AllGuilds = self.bot.guilds
        #go through the guilds the bot is in 
        for guild in AllGuilds:
            #get the category 
            category = get(guild.categories, name = CategoryName) 
            #initialise variable
            global FoundCategoryID
            #if the category is not found
            if not category:
                #create the category
                category = await guild.create_category(CategoryName, overwrites = None, reason = None)
            #set the category id
            FoundCategoryID = category.id
            #go through all the items in the channel_name list
            for channel in channel_name:
                try:
                    #get the channel as an object 
                    ChannelSearch = get(self.bot.get_all_channels(), name = channel) 
                    #if it's not found it will create it
                    if not ChannelSearch:
                        print(f'creating channel for: {channel} in guild: {guild}')
                        await guild.create_text_channel(name = channel, category = category)
                    #if it is found
                    else:
                        #check if the channel is not already part of the category
                        if ChannelSearch.category_id != FoundCategoryID or not ChannelSearch.category_id:
                            #move the channel
                            print(f'Moving channel {channel} to {category}')
                            await ChannelSearch.edit(category = category)
                except Exception as e:
                    exc = '{}: {}'.format(type(e).__name__, e)
                    print(f'Failed to create or move channel {channel}\n{exc}')

def setup(bot):
    bot.add_cog(Loops(bot))