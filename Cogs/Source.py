from discord.ext import commands

class Source(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Clears the chat in the channel it is called using the number from the command
    @commands.command(pass_context=True, name='Source', aliases=['sourcemessage'], no_pm=True)
    async def Source(self, ctx):
        #sets default variables
        URL : str = 'https://github.com/Simran-Gill-22/THN'
        return await ctx.send(f'Source code {URL}')

def setup(bot):
    bot.add_cog(Source(bot))