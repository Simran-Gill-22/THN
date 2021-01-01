from typing import List
import discord
from discord.ext import commands
import json

from Modules.Error import Error

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global MemeDirectory
        global AppreciationDirectory
        MemeDirectory = 'Images/Approval.json'
        AppreciationDirectory = 'Images/AppreciationApproval.json'
    
    async def GetImagesFromLists(self, DirectoryToUse, JSONObjectName, TypeOfList, ListOfMemes, MemeStatus):
        with open(DirectoryToUse) as f:
            #load the contents
            data = json.load(f)
            #loops through the json file
            for i in data:
                #look for image
                if i == JSONObjectName:
                    #go through the multiple image
                    for Image in data[JSONObjectName]:
                        if TypeOfList == 'All':
                            if JSONObjectName == 'Appreciation':
                                #sets the appreciation sociaty accronym if looking for appreciation 
                                ListOfMemes = (f"{ListOfMemes}{Image['Name']}({Image['AppreciationSociety']})\n")
                            else:
                                #set the list of image to be used by the embed later
                                ListOfMemes = (f"{ListOfMemes}{Image['Name']}\n")
                            #set the list of image statuses to be used by the embed later
                            MemeStatus = (f"{MemeStatus}{Image['ApprovalStatus']}\n")
                        else:
                            #only check for the approval type 
                            if Image["ApprovalStatus"] == TypeOfList:
                                #set the list of image to be used by the embed later
                                ListOfMemes = (f"{ListOfMemes}{Image['Name']}\n")
        
        return ListOfMemes, MemeStatus

    @commands.command(pass_context=True, name='Image', aliases=['image'], no_pm=True)
    async def Image(self, ctx, MemeName):
        with open(MemeDirectory) as f:
            #load the contents
            data = json.load(f)
            #loops through the json file
            for i in data:
                #look for Memes
                if i == 'Memes':
                    #go through the multiple memes
                    for Meme in data['Memes']:
                        if Meme["Name"] == MemeName and Meme["ApprovalStatus"] == "Approved":
                            return await ctx.send(Meme["URL"])
                        elif Meme["ApprovalStatus"] == "Denied":
                            #send an error
                            #set error title and message
                            Title = str('Image has been Denied')
                            Content = str(f'This Image has been denied {Meme["ApprovingUser"]}')
                            #send the embeded message
                            return await ctx.send(embed = Error(Title, Content))
                        elif Meme["ApprovalStatus"] == "Waiting":
                            #send an error
                            #set error title and message
                            Title = str('Image is still pending')
                            Content = str(f'This Image has not been approved or denied')
                            #send the embeded message
                            return await ctx.send(embed = Error(Title, Content))
        
        #send an error
        #set error title and message
        Title = str('No image found')
        Content = str(f'No image has been found by that name')
        #send the embeded message
        return await ctx.send(embed = Error(Title, Content))


    
    @commands.command(pass_context=True, name='ListImages', aliases=['listimages'], no_pm=True)
    async def ListImages(self, ctx, TypeOfList):

        #set the text to lowercase to not make it case sensitive
        LowercaseString = TypeOfList.lower()

        #set the embed colour
        if LowercaseString == 'approved':
            EmbedColor = discord.Color.green()
        elif LowercaseString == 'pending':
            EmbedColor = discord.Color.from_rgb(255,255,0)
        elif LowercaseString == 'denied':
            EmbedColor = discord.Color.red()
        elif LowercaseString == 'all':
            EmbedColor = discord.Color.blue()
        else:
            #if a keyword is not found
            e = discord.Embed(title = f'Error, invalid argument', color = discord.Color.red())
            e.add_field(name= str(f'Available key words'), value= str(f'Approved\nPending\nDenied\nAll'))
            return await ctx.send(embed = e)
        
        ListOfMemes = ''
        MemeStatus = ''
        Result1 = await self.GetImagesFromLists(AppreciationDirectory, 'Appreciation', TypeOfList, ListOfMemes, MemeStatus)
        Result2 = await self.GetImagesFromLists(MemeDirectory, 'Memes', TypeOfList, Result1[0], Result1[1])

        ListOfMemes = Result2[0]
        MemeStatus = Result2[1]
        

        #check if the list of memes found is empty if not set them to a default message
        if not ListOfMemes:
            ListOfMemes = "No images found"
        if not MemeStatus:
            MemeStatus = "Null"

        #set the embeded message appropriatly for a status or all 
        if TypeOfList == 'All':
            e = discord.Embed(title = f'All images', color = EmbedColor)
            e.add_field(name= str(f'Image Name'), value= str(f'{ListOfMemes}'))
            e.add_field(name= str(f'Message'), value= str(f'{MemeStatus}'))
        else:
            e = discord.Embed(title = f'All {TypeOfList} images', color = EmbedColor)
            e.add_field(name= str(f'Image Name'), value= str(f'{ListOfMemes}'))
        #send embeded message
        await ctx.send(embed = e)

def setup(bot):
    bot.add_cog(Image(bot))