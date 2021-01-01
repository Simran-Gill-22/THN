import json
import asyncio
import os
import random
import discord
from discord import client
from discord import guild
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get
import requests
import re

from Modules.Error import Error
from Modules.ImageURLValidator import ImageURLValidator

class AddImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot      

    @commands.Cog.listener()
    async def on_ready(self):
        print("""
        ######################
        ###Checking Channels##
        ######################
        """)
        await self.CallCheckChannels('Bot', ['bot-commands','image-approval'])
        i = ['bot-commands','image-approval']
        global MemeDirectory
        global AppreciationDirectory
        global DirectoryConfig
        global OwnerApproval  
        global GroupApproval
        global GroupApprovalList
        global OwnerID      
        DirectoryConfig = 'Json/Config.json'
        MemeDirectory = 'Images/Approval.json'
        AppreciationDirectory = 'Images/AppreciationApproval.json'
        if os.path.isfile(DirectoryConfig):
            with open(DirectoryConfig) as f:
                data = json.load(f)
                #check if the value is in the config
                if 'OwnerApproval' not in data:
                    #if not it will default to false
                    OwnerApproval = False
                #if it is in the app
                else:
                    #check if it is true or false
                    if data['OwnerApproval'] == 'True' or data['OwnerApproval'] == 'False':
                        #if it is set the variable appropriatly
                        if data['OwnerApproval'] == 'True':
                            OwnerApproval = True
                        elif data['OwnerApproval'] == 'False':
                            OwnerApproval = False
                        #check the owner id is in the data
                        if 'OwnerID' in data:
                            #if yes set it 
                            OwnerID = data['OwnerID']

                #check if the value is in the config
                if 'GroupApproval' not in data:
                    #if not it will default to false
                    GroupApproval = False
                #if it is in the app
                else:
                    #check if it is true or false
                    if data['GroupApproval'] == 'True' and not OwnerApproval and data['ApprovalList']:
                        GroupApproval = True
                        GroupApprovalList = data['ApprovalList']
                    else:
                        GroupApproval = False
                        GroupApprovalList = ''

        #if the file is found
        if not os.path.isfile(MemeDirectory):
            with open(MemeDirectory, "w") as write_file:
                json.dump({"Memes": []}, write_file, indent=4)

    async def CallCheckChannels(self, Category, ChannelName):
        channel = get(self.bot.get_all_channels(), name=ChannelName) 
        #if the channel is not found 
        if not channel:
            CreateChannels = self.bot.get_cog('Loops')  
            if type(ChannelName) == 'list':
                await CreateChannels.CreateChannels(Category, [ChannelName])
            else:
                await CreateChannels.CreateChannels(Category, ChannelName)
            #get the channel object again
            channel = get(self.bot.get_all_channels(), name=ChannelName) 
        return channel
        
    async def GetAppreciationName(self, ImageName):
        #convert to lower
        ImageNameLower = ImageName.lower()
        #set the variable appropriatly 
        if ImageNameLower == 'kr':
            ImageAppreciationSociety = 'Keanu Reeves'
        elif ImageNameLower == 'cr':
            ImageAppreciationSociety = 'Chris Roberts'
        elif ImageNameLower == 'mm':
            ImageAppreciationSociety = 'Magic Mike'
        else:
            #if an invalid value has been just set it to empty
            ImageAppreciationSociety = ''
        #return the value
        return ImageAppreciationSociety


    async def GetImageToEdit(self, ImageName, DirectoryToUse, JSONObjectName, channel):
        with open(DirectoryToUse) as f:
            #load the contents
            data = json.load(f)
            #loops through the json file
            for i in data:
                #look for Memes
                if i == JSONObjectName:
                    #go through the multiple memes
                    for Image in data[JSONObjectName]:
                        #if the message id is found in the json
                        if Image["Name"] == ImageName:
                            #set title and message
                            e = discord.Embed(title = "Edit image", color = discord.Color.from_rgb(255,255,0))
                            e.add_field(name= str(f'Message'), value= str(f'Edit the following image \n \nName: {ImageName} \nURL: {Image["URL"]}'))
                            if JSONObjectName == 'Appreciation':
                                ImageAppreciationSociety = await self.GetAppreciationName(Image["AppreciationSociety"])
                                e.add_field(name= str(f'Message'), value= str(f'Please approve the following {ImageAppreciationSociety} image. \n\nURL: {Image["URL"]} \n\nReference: {ImageName}'))
                            elif JSONObjectName == 'Memes':
                                e.add_field(name= str(f'Message'), value= str(f'Please approve the following image.  \n\nURL: {Image["URL"]} \n\nReference: {ImageName}'))


                            e.add_field(name= str(f'Current Status'), value= str(f'{Image["ApprovalStatus"]}'))
                            #send the embeded message
                            message = await channel.send(embed = e)
                            emojis = ['✅', '❌']
                            for emoji in emojis:
                                await message.add_reaction(emoji)
                            
                            message_id = message.id
                            Image["MessageID"] = message_id
                            with open(DirectoryToUse, "w") as write_file:
                                json.dump(data, write_file, indent=4)

                            return True
        return False


    async def ChangeApprovalType(self, ctx, ApprovalType , ApprovalBool):
        sending_user = ctx.author.id
        OwnerID = ctx.guild.owner_id
        if sending_user != OwnerID:
            #set error title and message
            Title = str(f'Invalid Permission')
            Content = str(f'You (<@{sending_user}>) do not have valid permission. Please contact <@{OwnerID}>')
            #send the embeded message
            await ctx.send(embed = Error(Title, Content))
        #set variables
        ApprovalBoolLower = ApprovalBool.lower()
        ApprovalTypeLower = ApprovalType.lower()
        ApprovalMethod = ''
        if ApprovalBoolLower == 'true' or ApprovalBoolLower == 'false':
            #open/create the json file
            with open(DirectoryConfig) as f:
                data = json.load(f)

            if ApprovalTypeLower == 'owner':
                ApprovalMethod = 'OwnerApproval'
            elif ApprovalTypeLower == 'list':
                ApprovalMethod = 'GroupApproval'

            #checks what the user has sent to be set
            if ApprovalBoolLower == 'true':
                #check the value stored already
                if data[ApprovalMethod] == 'True':
                    #if it is the current vlaue it will set the appropriate messgae 
                    #set title and message
                    e = discord.Embed(title = f"{ApprovalType} approvals", color = discord.Color.green())
                    e.add_field(name= str(f'Message'), value= str(f'{ApprovalType} approvals has already been set to true.'))
                else:
                    e = discord.Embed(title = f"{ApprovalType} approvals", color = discord.Color.green())
                    if ApprovalTypeLower == 'owner':
                        #set approval to true in the config
                        data['OwnerApproval'] = 'True'
                        data['GroupApproval'] = 'False'
                        #set title and message
                        e.add_field(name= str(f'Message'), value= str(f'Owner approvals has been set. Only <@{OwnerID}> can approve images'))
                    elif ApprovalTypeLower == 'list':
                        #set approval to true in the config
                        data['OwnerApproval'] = 'False'
                        data['GroupApproval'] = 'True'
                        #set title and message
                        e = discord.Embed(title = "Group approvals", color = discord.Color.green())
                        #set variable
                        GroupApprovalListString = ''
                        #if users are in a list 
                        if GroupApprovalList:
                            #go through each user 
                            for user in GroupApprovalList:
                                #concat into a string
                                GroupApprovalListString = (f"{user}\n")
                            #set the field to use
                            e.add_field(name= str(f'Users who can approve'), value= str(GroupApprovalListString))
                        else:
                            e.add_field(name= str(f'Message'), value= str(f'Group approvals has been set. Add users to the list'))
            elif ApprovalBoolLower == 'false':
                #check the value stored already
                if data[ApprovalMethod] == 'False':
                    #if it is the current vlaue it will set the appropriate messgae 
                    #set title and message
                    e = discord.Embed(title = f"{ApprovalType} approvals", color = discord.Color.green())
                    e.add_field(name= str(f'Message'), value= str(f'{ApprovalType} approvals has already been set to false.'))
                else:
                    #set approval to true in the config
                    data[ApprovalMethod] = 'False'
                    #set title and message
                    e = discord.Embed(title = f"{ApprovalType} approvals", color = discord.Color.green())
                    e.add_field(name= str(f'Message'), value= str(f'{ApprovalType} approvals has been set. eveyone can approve images'))
            
            if not data['OwnerID']:
                #find the correct key and set it
                data['OwnerID'] = OwnerID
            
            #save the new json
            with open(DirectoryConfig, "w") as f:
                json.dump(data, f, indent=4)
        
            #send the embeded message
            await ctx.send(embed = e)

        else:
            #if it is not a valid argument
            #set error title and message
            Title = str(f'Invalid Argument')
            Content = str(f'command needs to be True/False')
            #send the embeded message
            await ctx.send(embed = Error(Title, Content))    


    async def ApproveDenyImage(self, reaction, user, MessageID, DirectoryToUse, JSONObjectName):
        with open(DirectoryToUse) as f:
                #load the contents
                data = json.load(f)
                #loops through the json file
                for i in data:
                    #look for image
                    if i == JSONObjectName:
                        #go through the multiple image
                        for Image in data[JSONObjectName]:
                            #if the message id is found in the json
                            if Image["MessageID"] == MessageID:
                                Image#check for the tick emoji
                                if reaction.emoji == '✅': 
                                    if user.id != OwnerID:
                                        if OwnerApproval:
                                            #set error title and message
                                            Title = str(f'Error')
                                            Content = str(f'Only admins can approve images. Please contact <@{OwnerID}>')
                                            #send the embeded message
                                            return await reaction.message.channel.send(embed = Error(Title, Content))

                                        #check ig group approval is used
                                        if GroupApproval:
                                            #sets variables for is a user is not found
                                            UserFound = False
                                            #go through the users in the list
                                            for user in GroupApproval:
                                                #if a user is found
                                                if user.id == user:
                                                    #set variable to true
                                                    UserFound = True
                                            #if they are not found
                                            if not UserFound:
                                                #set error title and message
                                                Title = str(f'Error')
                                                Content = str(f'You do not have permission to approve images. To see who can approve images use $ApprovalListUsers')
                                                #send the embeded message
                                                return await reaction.message.channel.send(embed = Error(Title, Content))

                                    #check if the image has already been approved
                                    if Image["ApprovalStatus"] == "Approved":
                                        #check first to send the appropriate messgae
                                        if Image["AppreciationSociety"] and JSONObjectName == 'Appreciation':
                                            await reaction.message.channel.send(f'{Image["UserID"]}, your image has already been approved by <@{user.id}>. It is now in rotation.')
                                        else:
                                            #if so let the user know
                                            await reaction.message.channel.send(f'{Image["UserID"]}, your image has already been approved by <@{user.id}>. Use the following command to call it: \n$Image {Image["Name"]}')
                                    else:
                                        #set the approval status to approved
                                        Image["ApprovalStatus"] = "Approved"
                                        #if it is looking for an appriciation image
                                        if Image["AppreciationSociety"] and JSONObjectName == 'Appreciation':
                                            #set the appropriate file to open dynamically 
                                            AppreciationSociatyDirectory = str(f'Images/{Image["AppreciationSociety"]}.json')
                                            if os.path.isfile(AppreciationSociatyDirectory):
                                                #open the json file
                                                with open(AppreciationSociatyDirectory) as s:
                                                    #load the contents
                                                    DataAppreciation = json.load(s)
                                                    #get the length of the file to determine next key name
                                                    LengthOfFile = len(DataAppreciation)
                                                    #set the new key in the appreciation file
                                                    DataAppreciation[LengthOfFile] = Image["URL"]
                                                    #set that key value in the file
                                                    Image["ImageID"] = LengthOfFile   
                                                #save the new json
                                                with open(AppreciationSociatyDirectory, "w") as s:
                                                    json.dump(DataAppreciation, s, indent=4)
                                        #check first to send the appropriate messgae
                                        if Image["AppreciationSociety"] and JSONObjectName == 'Appreciation':
                                            await reaction.message.channel.send(f'{Image["UserID"]}, your image has already been approved by <@{user.id}>. It is now in rotation.')
                                        else:
                                            #if so let the user know
                                            await reaction.message.channel.send(f'{Image["UserID"]}, your image has already been approved by <@{user.id}>. Use the following command to call it: \n$Image {Image["Name"]}')
                                    

                                #check for the tick emoji
                                elif reaction.emoji == '❌':
                                    if Image["ApprovalStatus"] == "Denied":
                                        #if so let the user know
                                        await reaction.message.channel.send(f'{Image["UserID"]}, your image has already been denied by <@{user.id}>.')
                                    else:
                                        #set the approval status to denied
                                        Image["ApprovalStatus"] = "Denied"
                                        #if it is looking for an appriciation image
                                        if Image["AppreciationSociety"] and JSONObjectName == 'Appreciation' and Image["ImageID"]:
                                            #set the appropriate file to open dynamically 
                                            AppreciationSociatyDirectory = str(f'Images/{Image["AppreciationSociety"]}.json')
                                            if os.path.isfile(AppreciationSociatyDirectory):
                                                #open the json file
                                                with open(AppreciationSociatyDirectory) as s:
                                                    #load the contents
                                                    DataAppreciation = json.load(s)
                                                    #set the image key
                                                    ImageKeyString = str(Image['ImageID'])
                                                    #Delete the key from the file
                                                    del DataAppreciation[ImageKeyString]
                                                    #set that key value in the file
                                                    Image["ImageID"] = ""   
                                                #save the new json
                                                with open(AppreciationSociatyDirectory, "w") as s:
                                                    json.dump(DataAppreciation, s, indent=4)
                                        #let the user know
                                        await reaction.message.channel.send(f'{Image["UserID"]}, your image has been denied')

                                        
                                Image["ApprovingUser"] = f'<@{user.id}>'
                                
                            #save the new json
                            with open(DirectoryToUse, "w") as f:
                                json.dump(data, f, indent=4)
                            
                            #remove reaction
                            await reaction.message.remove_reaction(reaction.emoji, user)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        #if the bot reacts just return
        if user.bot:
            return

        #check for only these 2 emojis
        if reaction.emoji == '✅' or reaction.emoji == '❌':
            MessageID = reaction.message.id
            #check the image is in either json
            SuccessfulyFoundMessageAppreciation = await self.ApproveDenyImage(reaction, user, MessageID, AppreciationDirectory, 'Appreciation')
            SuccessfulyFoundMessageMeme = await self.ApproveDenyImage(reaction, user, MessageID, MemeDirectory, 'Memes')

            #if it was found in a json 
            if SuccessfulyFoundMessageAppreciation or SuccessfulyFoundMessageMeme:
                #just return to prevent the script from running further
                return      


    @commands.command(pass_context=True, name='ApprovalListUsers', aliases=['approvallistusers'], no_pm=True)
    async def ApprovalListUsers(self, ctx):
        #set variable
        GroupApprovalListString = ''

        if GroupApproval:
            e = discord.Embed(title = "User List (Active)", color = discord.Color.green())
        else:
            e = discord.Embed(title = "User List (Not active)", color = discord.Color.green())

        #if users are in a list 
        if GroupApprovalList:
            #go through each user 
            for user in GroupApprovalList:
                #concat into a string
                GroupApprovalListString = (f"{user}\n")
            #set the field to use
            e.add_field(name= str(f'Users who can approve'), value= str(GroupApprovalListString))
        else:
            #use a default field
            e.add_field(name= str(f'Users found'), value= str('None'))

        return await ctx.send(embed = e)

    
    @commands.command(pass_context=True, name='ApprovalList', aliases=['approvallist'], no_pm=True)
    async def ApprovalList(self, ctx, AddRemove, UserToAddRemove):
        #set the AddRemove to lower
        AddRemoveLower = AddRemove.lower()
        #check if owner
        if ctx.message.author.id != OwnerID:
            #set error title and message
            Title = str(f'Not an Owner')
            Content = str(f'Need to be an owner to access this commmand')
            #send the embeded message
            await ctx.send(embed = Error(Title, Content))
        #check a valid argument
        elif AddRemoveLower != 'add' and AddRemoveLower != 'remove':
            #set error title and message
            Title = str(f'Not a valid argument')
            Content = str(f'Please use Add or Remove')
            #send the embeded message
            await ctx.send(embed = Error(Title, Content))
        #check if a valid user
        elif '@' not in UserToAddRemove:
            #set error title and message
            Title = str(f'Not a valid user')
            Content = str(f'Please @ the user you wish to add')
            #send the embeded message
            await ctx.send(embed = Error(Title, Content))
        
        #strip the @ from the id
        StrippedUserID = re.sub('[^0-9]','', UserToAddRemove)
        #set variable
        UserFound = False
        AddedOrRemoved = ''
        #open/create the json file
        with open(DirectoryConfig) as f:
                data = json.load(f)

        #look through all the users in the list
        for user in data['ApprovalList']:
            #if a user is found
            if user == StrippedUserID:
                #set variable to let it know a user has been found
                UserFound = True
                #if they are trying to be added 
                if AddRemoveLower == 'add':
                    #prepare an error letting them know they are already on the list
                    Title = str(f'User already added')
                    Content = str(f'The user you are trying to add has already been added')
                    #send the embeded message 
                    return await ctx.send(embed = Error(Title, Content))
                #if it is to remove them they will be removed
                elif AddRemoveLower == 'remove':
                    data['ApprovalList'].remove(StrippedUserID)
                    AddedOrRemoved = 'Removed'
                    
        if not UserFound:
            if AddRemoveLower == 'add':
                data['ApprovalList'].append(StrippedUserID)
                AddedOrRemoved = 'Added'
            elif AddRemoveLower == 'remove':
                #prepare an error letting them know they are already on the list
                Title = str(f'User not found')
                Content = str(f'The user you are trying to remove was not found')
                #send the embeded message 
                return await ctx.send(embed = Error(Title, Content))
        
        #save the new json
        with open(DirectoryConfig, "w") as f:
            json.dump(data, f, indent=4)

        e = discord.Embed(title = "User approvals", color = discord.Color.green())
        e.add_field(name= str(f'Message'), value= str(f'{UserToAddRemove} has been {AddedOrRemoved}'))
        return await ctx.send(embed = e)


    @commands.command(pass_context=True, name='OwnerApproval', aliases=['ownerapproval'], no_pm=True)
    async def OwnerApproval(self, ctx, OwnerApprovalBool):
        await self.ChangeApprovalType(ctx, 'Owner', OwnerApprovalBool)

    @commands.command(pass_context=True, name='ListApproval', aliases=['listapproval'], no_pm=True)
    async def ListApproval(self, ctx, OwnerApprovalBool):
        await self.ChangeApprovalType(ctx, 'List', OwnerApprovalBool)


    @commands.command(pass_context=True, name='AddImage', aliases=['addimage'], no_pm=True)
    async def AddImage(self, ctx, ImageName, ImageURL):

        ValidImage = ImageURLValidator(ImageURL)
        if not ValidImage:
            Title = str('Invalid URL')
            Content = str(f'The follwing URL {ImageURL} is not a valid picture.\nPlease use a valid url')
            #send the embeded message
            return await ctx.send(embed = Error(Title, Content))

        #define channel
        channel_name = 'image-approval'
        #call the function to create the channel
        channel = await self.CallCheckChannels('Bot', channel_name)

        #sending users name
        sending_user = ctx.author.mention

        #set variables to lower
        ImageNameLower = ImageName.lower()
        #set the approprite json to use
        if ImageNameLower == 'kr' or ImageNameLower == 'cr' or ImageNameLower == 'mm':
            DirectoryToUse = AppreciationDirectory
            JSONObjectName = 'Appreciation'
            ImageAppreciationSociety = await self.GetAppreciationName(ImageName)
        else:
            DirectoryToUse = MemeDirectory
            JSONObjectName = 'Memes'

        with open(DirectoryToUse) as f:
            #load the contents
            data = json.load(f)

        #loops through the json file
        for i in data:
            #look for images
            if i == JSONObjectName:
                #go through the multiple images
                for Image in data[JSONObjectName]:
                    #if the Image is waiting to be approved send the following message
                    if Image["URL"] == ImageURL and Image["ApprovalStatus"] == "Waiting":
                        #set error title and message
                        Title = str(f'Message')
                        Content = str(f'{sending_user}, this image has already been submitted and is waiting to be approved')
                        #send the embeded message
                        return await ctx.send(embed = Error(Title, Content))  
                    #if the Image has been approved send the following message
                    elif Image["URL"] == ImageURL and Image["ApprovalStatus"] == "Approved":
                        #set error title and message
                        Title = str(f'Message')
                        Content = str(f'{sending_user}, this image has already been approved by {Image["ApprovingUser"]}')
                        #send the embeded message
                        return await ctx.send(embed = Error(Title, Content))  
                    elif Image["URL"] == ImageURL and Image["ApprovalStatus"] == "Denied":
                        #set error title and message
                        Title = str(f'Message')
                        Content = str(f'{sending_user}, this image has already been Denied by {Image["ApprovingUser"]}')
                        #send the embeded message
                        return await ctx.send(embed = Error(Title, Content)) 

        #let the user know the message needs approval
        UniqueReferenceID = await ctx.send(f'{sending_user}, your image has been submitted for approval')
        UniqueID = UniqueReferenceID.id
        #set title and message
        e = discord.Embed(title = "Image for approval", color = discord.Color.from_rgb(255,255,0))
        if JSONObjectName == 'Appreciation':
            e.add_field(name= str(f'Message'), value= str(f'Please approve the following {ImageAppreciationSociety} image. \n\nURL: {ImageURL} \n\nReference: {UniqueID}'))
        elif JSONObjectName == 'Memes':
            e.add_field(name= str(f'Message'), value= str(f'Please approve the following image.  \n\nURL: {ImageURL} \n\nReference: {ImageName}'))
        #send the embeded message
        message = await channel.send(embed = e)
        emojis = ['✅', '❌']
        for emoji in emojis:
            await message.add_reaction(emoji)
        
        message_id = message.id
        with open(DirectoryToUse) as f:
            #load the contents
            data = json.load(f)

        if JSONObjectName == 'Appreciation':
            NewData = {
                "MessageID":message_id,
                "Name":UniqueID,
                "URL":ImageURL,
                "ApprovalStatus":"Waiting",
                "UserID": sending_user,
                "ApprovingUser": "",
                "AppreciationSociety": ImageNameLower,
                "ImageID":""
            }
        elif JSONObjectName == 'Memes':
            NewData = {
                "MessageID":message_id,
                "Name":ImageName,
                "URL":ImageURL,
                "ApprovalStatus":"Waiting",
                "UserID": sending_user,
                "ApprovingUser": ""
            }
        #set the new json 
        
        data[JSONObjectName].append(NewData)
        #write the new token to the file created
        with open(DirectoryToUse, "w") as write_file:
            json.dump(data, write_file, indent=4)


    @commands.command(pass_context=True, name='EditImage', aliases=['editimage'], no_pm=True)
    async def EditImage(self, ctx, ImageName):
        #set sending user
        sending_user = ctx.author.mention
        #define channel
        channel_name = 'image-approval'
        #call the function to create the channel
        channel = await self.CallCheckChannels('Bot', channel_name)

        #check the image is in either json
        SuccessfulyFoundMessageAppreciation = await self.GetImageToEdit(ImageName, AppreciationDirectory, 'Appreciation', channel)
        SuccessfulyFoundMessageMeme = await self.GetImageToEdit(ImageName, MemeDirectory, 'Memes', channel)

        #if it was found in a json 
        if SuccessfulyFoundMessageAppreciation or SuccessfulyFoundMessageMeme:
            #just return to prevent the script from running further
            return 
        else:
            #set error title and message
            Title = str(f'Message')
            Content = str(f'{sending_user}, no image is found by the reference {ImageName}')
            #send the embeded message
            return await ctx.send(embed = Error(Title, Content))       
            

def setup(bot):
    bot.add_cog(AddImage(bot))