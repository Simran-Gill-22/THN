import random
from discord.ext import commands
from discord.utils import get, find

class Book(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #will probably have to re-write
    @commands.command(pass_context=True)  
    async def Book(self, ctx,*args):
        #set some variables
        RoleName : str = 'Cinema'
        RoleUsers = []
        #get the role
        role = find(lambda r: r.name == RoleName, ctx.guild.roles)
        #go through all the users in the server
        for user in ctx.guild.members:
            #if the user has the role 
            if role in user.roles:
                #gets the id's of the users with the roles and makes it a mention to be stored
                RoleUsers.append('<@' + str(user.id) + '>')

        #prints the role for debugging purposes 
        print(*RoleUsers)
        #return an error if no users are found in that role
        if not RoleUsers: 
            return await ctx.send(f'No users found in the {RoleName} role')
        else:
            #selects a random user from the array
            booking_user = ('You have been chosen '  + random.choice(RoleUsers))
            #mentions them
            return await ctx.send(booking_user)
                

def setup(bot):
    bot.add_cog(Book(bot))