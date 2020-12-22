######################################
#current release date:      27/11/2020
#current version:           0.1
######################################

#import modules
from asyncio import constants
import math
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext import tasks
import logging
import os
import random
import time
import datetime
from datetime import timedelta
import os.path
from os import path  
from time import gmtime, strftime
from bs4 import BeautifulSoup
from selenium import webdriver
import sys

#client const
OSBuid : float = 0.1
IsDebug : bool = True
Now = datetime.datetime.now()

#prefix for the bot 
bot_prefix= "$"
client = commands.Bot(command_prefix=bot_prefix)

@client.event
async def on_ready():
    #gets time and date
    time_date = Now.strftime("%d-%m-%Y %H:%M")
    #print when the bot is ready as well as the date and time for the user
    print("Bot Online!")
    print('Current time is:' + time_date)
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print ("OS Build: {}".format(OSBuid))
    #sets the presence of the bot
    await client.change_presence(status=discord.Status.idle, activity=None)
    #starting loops
    cr_image_loop.start()
    mm_image_loop.start()
    kr_image_loop.start()
    # ping_loop.start()
    # noice_loop.start()

#purpose command
@client.command(pass_context=True, name='purpose', aliases=['sendpurposemessage'], no_pm=True)
async def purpose(ctx):
    await ctx.send(""" My purpose is to reply to all Summit1G emotes with :nauseated_face: & post memes of Chris Roberts & Magic Mike""")
    return

@client.command(pass_context=True, name='invite', aliases=['createinvitelink'], no_pm=True)
async def invite(ctx):
    #create the invite
    invite = await ctx.channel.create_invite()
    await ctx.send(f"Here's your invite: {invite}")
    return

@client.command(pass_context=True, name='getbans', aliases=['getbanneduser'], no_pm=True)
async def getbans(ctx):
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

    await ctx.send(embed=embedVar)
    return

@client.command(pass_context=True, name='clear', aliases=['clearmessages'], no_pm=True)
async def clear(ctx, number):
    #sets default variables
    mgs = []
    number = int(number)
    if number > 99 or number < 1:
        #if more than or less than required messages
        await ctx.send("I can only delete messages within a range of 1 - 99")
    else:
        #get all messages upto the number sent
        async for message in ctx.message.channel.history(limit=int(number+1)):
            mgs.append(message)
        #deletes the messages
        await ctx.message.channel.delete_messages(mgs)
        #await ctx.channel.purge(limit = int(number+1))
        await ctx.send('Successfully Deleted {0} messages'.format(number))
    return

################################################################################################################
#################################################TESTING BLOCK#################################################
################################################################################################################
# @client.command(pass_context=True, name='ban', aliases=['banuser'], no_pm=True)
# async def ban(ctx, *, member : discord.Member = None):
#     if not ctx.message.author.server_permissions.administrator:
#         return
#     channel = ctx.channel
#     if not member:
#         return await channel.send(ctx.message.author.mention + "Specify a user to ban!")
#     try:
#         await client.ban(member)
#     except Exception as e:
#         if 'Privilege is too low' in str(e):
#             return await channel.send(":x: Privilege too low!")
 
#     embed = discord.Embed(description = "**%s** has been banned!"%member.name, color = 0xFF0000)
#     return

# @client.command(pass_context=True, name='kick', aliases=['kickuser'], no_pm=True)
# async def kick(ctx, *, member : discord.Member = None):
#     if not ctx.message.author.server_permissions.administrator:
#         return
#     channel = ctx.channel
#     if not member:
#         return await channel.send(ctx.message.author.mention + "Specify a user to kick!")
#     try:
#         await client.kick(member)
#     except Exception as e:
#         if 'Privilege is too low' in str(e):
#             return await channel.send(":x: Privilege too low!")
#     embed = discord.Embed(description = "**%s** has been kicked!"%member.name, color = 0xFF0000)
#     return

# #will probably have to re-write
# @client.command(pass_context=True)  
# async def book(ctx,*args):
#     #set variables for the role to search
#     channel = ctx.channel
#     server = ctx.guilds
#     role_name = (' '.join(args))
#     role_id = server.roles[0]
#     #serches for the role 
#     for role in server.roles:
#         if role_name == role.name:
#             role_id = role
#             break
#     else:
#         #no role found
#         await ctx.send("Role doesn't exist")
#         return
#     #creates array for the users to be stored in
#     role_users = []
#     #goes through all memebers to match the roles for the one serched
#     for member in ctx.server.members:
#         if role_id in member.roles:
#             #prints out all names the the channel 
#             #await client.say(f"{role_name} - {member.name}")
#             #gets the id's of the users with the roles and makes it a mention to be stored
#             role_users.append('<@' + member.id + '>')
#     #prints the role for debugging purposes 
#     #print(*role_users)
#     #selects a random user from the array
#     booking_user = ('You have been chosen '  + random.choice (role_users))
#     #mentions them
#     msg = await ctx.send(booking_user)
#     return
################################################################################################################

@client.command(pass_context=True)
async def scmoney(ctx,*args):
    #directory = 'C:/Users/Simran/Google Drive/Personal/THN Bot/DEV/fundingGoals.txt'
    directory = 'fundingGoals.txt'
    channel = ctx.message.channel
    await ctx.send('This takes a couple of seconds....')
    if os.path.isfile(directory):
        file = open(directory, 'r+')
        lines = file.readlines()
        oldMoney, oldTime = lines[0], lines[1]
        dateTimeObj = datetime.datetime.strptime(oldTime, '%Y-%m-%d %H:%M:%S.%f')
        newMoney = scraper()
        moneyDiff = int(newMoney) - int(oldMoney)
        timeDiff = timeConvert(dateTimeObj)
        statement = 'Chris Roberts has ${:,} making him ${:,} richer in {}'.format(int(newMoney), moneyDiff, timeDiff)
        await ctx.send(statement)
        file.seek(0)
        file.truncate()
        file.write(newMoney)
        file.write('\n')
        file.write(str(Now))
        file.close()
        file.close()
        if moneyDiff > 0:
            await money.invoke(ctx)            
    else:
        file = open(directory, 'w+')
        moneySpent = scraper()
        statement = 'Star Citizen has raised ${:,} at the time of {}'.format(int(moneySpent), Now)
        await client.send_message(channel, statement)
        file.write(moneySpent)
        file.write('\n')
        file.write(str(Now))
        file.close()
        await money.invoke(ctx)
        
def scraper():
    url = 'https://robertsspaceindustries.com/funding-goals'
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    #driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    moneySpent = soup.find(class_='digits js-digits')
    value = moneySpent.get_text().replace(",", "")
    driver.quit()
    return value

def timeConvert(oldTime):
    diff = Now - oldTime
    diffS = diff.total_seconds()
    y , mod_ = divmod(diffS, 31556926)
    d , mod_ = divmod(mod_, 86400)        
    h , mod_ = divmod(mod_, 3600)               
    m , mod_ = divmod(mod_, 60)                
    s , mod_ = divmod(mod_, 1) 
    return('{:02d} Days {:02d} Hours {:02d} Minutes and {:02d} Seconds'.format(int(d), int(h), int(m), int(s)))

@client.command(pass_context=True, name='money', aliases=['sendmoneymeme'], no_pm=True)
async def money(ctx):
    channel = ctx.message.channel
    #image location
    path = 'Memes/Money.jpg'
    #pushes the image
    msg = await ctx.send(file=discord.File(path))
    return

@client.command(pass_context=True, name='smile', aliases=['sendsmilememe'], no_pm=True)
async def smile(ctx):
    channel = ctx.message.channel
    #image location
    path = 'Memes/Smile.jpg'
    #pushes the image
    msg = await ctx.send(file=discord.File(path))
    return

@client.event
async def on_message(message):
    channel = message.channel
    if message.author == client.user:
        return

    global culprit_user
    #saves the user who sent it for a response 
    sending_user = message.author.mention
    matt_id = '<@98128408969506816 00000>'

    #for matt 
    if sending_user == matt_id:
        culprit_user = message.author.mention
        matt_message = (culprit_user + ' weeb')     
        #send the message
        await channel.send(matt_message)
        return culprit_user 
    
    if (client.user != sending_user):
        #keywords you want to respond to (summit)
        sum_message_emotes = (':sum' , ':NotW')
        sum_message_emotes_whitelist = (':summitPls:')
        #searches for the emotes
        if sum_message_emotes_whitelist in message.content:
            #does nothing
            return
        elif any(x in message.content for x in sum_message_emotes):
            #saves the user who sent it for a response 
            culprit_user = message.author.mention
            #puts the message together
            sum_message = (culprit_user + ' Summit1G emotes :nauseated_face:')     
            #send the message
            await channel.send(sum_message)
            #returns the user so it can be used in other commands
            return culprit_user      
        
        #keywords you want to respond to (noice)
        #noice_message_emotes = ('noice' , ':mattW:' 'NOICE' , 'Noice')
        #searches for the emotes
        #if any(x in message.content for x in noice_message_emotes):
            #puts the message together
            #noice_message = (sending_user + ' Noice <:mattW:436999765142536193>')     
            #send the message
            #msg = await client.send_message(message.channel, noice_message)    
        #command needed to use other commands

        # #stops returning an error 
        # if not 'culprit_user' in globals():
        #     # culprit_user does not exist exists.
        #     return

    await client.process_commands(message)

@client.event
async def on_message_delete(message):
    channel = message.channel
    # #stops returning an error 
    # if not 'culprit_user' in globals():
    #         # culprit_user does not exist exists.
    #         return
        
    #message to respond when trying to delete the emote
    message_retry = (culprit_user + ' Summit1G emotes :nauseated_face:')
    #message to respond with when trying to delete the responce 
    message_response = (message_retry + ' nice try :stuck_out_tongue_winking_eye:')
    #emotes to search for --> should be the same as the on_message command
    message_emotes = (':sum' , ':NotW')
    #add a string to the end
    sum_message_evidance = (message_response + " Don't Hide the evidence")
    #add a string to the end
    sum_message_evidance_persistant = (message_response + " you can try but we know")
    
    #searches if the response tries to get delted 
    if message.content in {message_retry, message_response}:
        #sends the message
        await channel.send(message_response)

    #searches if the evidance tries to get delted 
    if any(x in message.content for x in message_emotes):
        #sends the message
        await channel.send(sum_message_evidance)

    #searches if the message for the evidance tries to get deleted 
    if message.content == sum_message_evidance:
        #sends the message
        await channel.send(sum_message_evidance_persistant)

    #searches if the message for the evidance response tries to get deleted 
    if message.content == sum_message_evidance_persistant:
        #sends the message
        await channel.send(sum_message_evidance_persistant)

    #matt reply
    matt_message = (culprit_user + ' weeb')
    matt_message_response = (culprit_user + " another one weeb")
    if message.content in {matt_message, matt_message_response}: 
        await channel.send(matt_message_response)

    #command needed to use other commands   
    await client.process_commands(message)

#cr posting loop
@tasks.loop(seconds=random.randint(28800, 57600), count=None)
async def cr_image_loop():
    print("starting cr loop")
    #runs while the client is not closed 
    while not client.is_closed():
        #define channel
        channel_name = 'chris-roberts-appreciation-society'
        #finds all channels
        for guild in client.guilds:
            for channel in guild.channels:
                if channel_name == str(channel):
                    #random image scripts
                    name = 'chris-roberts-appreciation-society'
                    folder_list = os.listdir(name) 
                    folder_string = random.choice(folder_list) 
                    image_list = os.listdir(name + '/' + folder_string + '/')
                    image_string = random.choice(image_list)
                    path = name + '/' + folder_string + '/' + image_string
                    #pushes the image
                    msg = await channel.send(file=discord.File(path))
            break  
        break

#mm posting loop
@tasks.loop(seconds=random.randint(28800, 57600), count=None)
async def mm_image_loop():
    print("starting mm loop")
    #runs while the client is not closed 
    while not client.is_closed():
        #define channel
        channel_name = 'magic-mike-appreciation-society'
        #finds all channels
        for guild in client.guilds:
            for channel in guild.channels:
                if channel_name == str(channel):
                    #random image scripts
                    name = 'magic-mike-appreciation-society'
                    folder_list = os.listdir(name) 
                    folder_string = random.choice(folder_list) 
                    image_list = os.listdir(name + '/' + folder_string + '/')
                    image_string = random.choice(image_list)
                    path = name + '/' + folder_string + '/' + image_string
                    #pushes the image
                    msg = await channel.send(file=discord.File(path))
            break  
        break

#kr posting loop
@tasks.loop(seconds=random.randint(28800, 57600), count=None)
async def kr_image_loop():
    print("starting kr loop")
    #runs while the client is not closed 
    while not client.is_closed():
        #define channel
        channel_name = 'keanu-reeves-appreciation-society'
        #finds all channels
        for guild in client.guilds:
            for channel in guild.channels:
                if channel_name == str(channel):
                    #random image scripts
                    name = 'keanu-reeves-appreciation-society'
                    folder_list = os.listdir(name) 
                    folder_string = random.choice(folder_list) 
                    image_list = os.listdir(name + '/' + folder_string + '/')
                    image_string = random.choice(image_list)
                    path = name + '/' + folder_string + '/' + image_string
                    #pushes the image
                    msg = await channel.send(file=discord.File(path))
            break  
        break

#noice loop
@tasks.loop(seconds=random.randint(28800, 57600), count=None)
async def noice_loop():
    #runs while the client is not closed 
    while not client.is_closed():
        #define channel
        channel_name = 'magic-mike-appreciation-society'
        #finds all channels
        for guild in client.guilds:
            for channel in guild.channels:
                if channel_name == str(channel):
                    #Genarates message
                    noice_message = ("Noice :mattW:")
                    #sends the message
                    await client.send(noice_message)
            break  
        break

#ping a user loop
@tasks.loop(seconds=random.randint(7200, 14000), count=None)
async def ping_loop():
    #runs while the client is not closed 
    while not client.is_closed:
        #define channel
        channel_name = 'general'
        #user id
        user_id = '<@98128408969506816>'
        #finds all channels 
        for guild in client.guilds:
            for channel in guild.channels:
                if channel_name == str(channel):
                    #sends the message
                    msg = await channel.send(user_id + ' Miss me? :mattW:')
                    #deletes the message to hide the evidence
                    await channel.delete(msg)
            break  
        break
        

if IsDebug == True:
    client.run('NDUxMDk0MjU4ODA4NTIwNzE1.XQErWg.XeiZM0xNRuNwIC-CY2OXN0dNwuQ')
else:   
    client.run('MzQzMjM0MTk2ODQ5ODE5NjUw.DGbbAg.IX8IexKdXeoFgdI-nrpWfXVD6q0')