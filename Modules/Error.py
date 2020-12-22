import discord
from discord.ext import commands

def Error(ErrorTitle, ErrorMessage):
    #set the embeded message
    e = discord.Embed(title = "Error", color = discord.Color.dark_red())
    e.add_field(name= str(f'{ErrorTitle}'), value= str(f'{ErrorMessage}'))
    #returns the embeded message
    return e

