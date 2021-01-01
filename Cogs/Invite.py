from discord.ext import commands

class Invite(commands.Cog):
    'This category handles all the invites for the server'
    def __init__(self, bot):
        self.bot = bot

    #creates an invite to the server
    @commands.command(pass_context=True, name='Invite', aliases=['createinvitelink'], no_pm=True)
    async def NewInvite(self, ctx):
        'This command creates a new invite link to the server'
        #create the invite
        invite = await ctx.channel.create_invite()
        return await ctx.send(f"Here's your invite: {invite}")

def setup(bot):
    bot.add_cog(Invite(bot))