import json
import asyncio
import os
import random
import discord
from discord.ext import commands, tasks
from discord.utils import get

from Modules.FolderBuilder import FolderBuilder
from Modules.AllFolderExist import AllFolderExist
from Modules.Error import Error

class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot      
        self.mm_image_loop.start()
        self.kr_image_loop.start()
        self.cr_image_loop.start()

    @commands.Cog.listener()
    async def on_ready(self):
        directory = 'Json/Config.json'
        global UseFolders
        if os.path.isfile(directory):
            with open(directory) as f:
                data = json.load(f)
                if 'UseFolders' not in data:
                    print('use folders not in config, not going to use folders')
                else:
                    UseFolders = data['UseFolders']
                    if UseFolders != "False":
                        #Check and create all folders exist
                        AllFolderExist()
                        print(data['UseFolders'])
                    else:
                        print("not using folders")
        else:
            UseFolders = "False"

        print("""
        ######################
        ###Checking Channels##
        ######################
        """)
        await self.CreateChannels('Appreciation Society', ['magic-mike-appreciation-society', 'chris-roberts-appreciation-society', 'keanu-reeves-appreciation-society'] )
        print("""
        ######################
        ####Starting Loops####
        ######################
        """) 
    
    def cog_unload(self):
        self.mm_image_loop.stop()
        self.kr_image_loop.stop()
        self.cr_image_loop.stop()
    
    async def UnloadLoop(self, channel):
        #set variables
        ChannelToUnload = channel.name
        #set error title and message
        Title = str(f'{ChannelToUnload} Loop Error')
        Content = str(f'This loop has stoppped, see the logs to know more')
        #send the embeded message
        await channel.send(embed = Error(Title, Content))

        #logic to decide which loop to unload
        if ChannelToUnload == 'magic-mike-appreciation-society':
            print('MM loop has been unloaded')
            self.mm_image_loop.cancel()
        elif ChannelToUnload == 'chris-roberts-appreciation-society':
            print('CR loop has been unloaded')
            self.cr_image_loop.cancel()
        elif ChannelToUnload == 'keanu-reeves-appreciation-society':
            print('KR loop has been unloaded')
            self.kr_image_loop.cancel()

    #mm posting loop
    @tasks.loop(seconds=random.randint(28800, 57600), count=None)
    async def mm_image_loop(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(3)
        print("MM loop has started")
        #define channel
        channel_name = 'magic-mike-appreciation-society'
        #finds all channels
        channel = get(self.bot.get_all_channels(), name=channel_name) 
        #if the channel is not found 
        if not channel:
            #call the function to create the channel
            self.CreateChannels('Appreciation Society', [channel_name])
            #get the channel object again
            channel = get(self.bot.get_all_channels(), name=channel_name) 
        #Call folder builder to make the image
        path = FolderBuilder(channel_name, UseFolders)
        #stop the loop is string is empty
        if not path:
            await self.UnloadLoop(channel)
        #check what type of path to send the appropriate message
        if "http" in path:
            await channel.send(path)
        else:
            #pushes the image
            await channel.send(file=discord.File(path))
    
    #cr posting loop
    @tasks.loop(seconds=random.randint(28800, 57600), count=None)
    async def cr_image_loop(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(3)
        print("CR loop has started")
        #define channel
        channel_name = 'chris-roberts-appreciation-society'
        #finds all channels
        channel = get(self.bot.get_all_channels(), name=channel_name) 
                #if the channel is not found 
        if not channel:
            #call the function to create the channel
            self.CreateChannels('Appreciation Society', [channel_name])
            #get the channel object again
            channel = get(self.bot.get_all_channels(), name=channel_name) 
        #Call folder builder to make the image
        path = FolderBuilder(channel_name, UseFolders)
        #stop the loop is string is empty
        if not path:
            await self.UnloadLoop(channel)
        #check what type of path to send the appropriate message
        if "http" in path:
            await channel.send(path)
        else:
            #pushes the image
            await channel.send(file=discord.File(path))

    #kr posting loop
    @tasks.loop(seconds=random.randint(28800, 57600), count=None)
    async def kr_image_loop(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(3)
        print("KR loop has started")
        #define channel
        channel_name = 'keanu-reeves-appreciation-society'
        #finds all channels
        channel = get(self.bot.get_all_channels(), name=channel_name) 
        #if the channel is not found 
        if not channel:
            #call the function to create the channel
            self.CreateChannels('Appreciation Society', [channel_name])
            #get the channel object again
            channel = get(self.bot.get_all_channels(), name=channel_name) 
        #Call folder builder to make the image
        path = FolderBuilder(channel_name, UseFolders)
        #stop the loop is string is empty
        if not path:
            await self.UnloadLoop(channel)          
        #check what type of path to send the appropriate message
        if "http" in path:
            await channel.send(path)
        else:
            #pushes the image
            await channel.send(file=discord.File(path))

    #this checks all the channels are present and in the correct categories 
    @commands.command(pass_context=True, name='CreateChannels', aliases=['createchannels'], no_pm=True)
    async def CreateChannels(self, CategoryName, channel_name):
        #wait until the bot is ready
        await self.bot.wait_until_ready()
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