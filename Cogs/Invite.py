from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #creates an invite to the server
    @commands.command(pass_context=True, name='Invite', aliases=['createinvitelink'], no_pm=True)
    async def Invite(self, ctx):
        #create the invite
        invite = await ctx.channel.create_invite()
        return await ctx.send(f"Here's your invite: {invite}")

def setup(bot):
    bot.add_cog(Invite(bot))