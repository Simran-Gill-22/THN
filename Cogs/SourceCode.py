from discord.ext import commands

class SourceCode(commands.Cog):
    'This category handles the source code for the bot'
    def __init__(self, bot):
        self.bot = bot

    #Clears the chat in the channel it is called using the number from the command
    @commands.command(pass_context=True, name='Source', aliases=['sourcemessage'], no_pm=True)
    async def Source(self, ctx):
        'This command gives the URL to the bots source code'
        #sets default variables
        URL : str = 'https://github.com/ssg22/TNH'
        sending_user = ctx.author.mention
        return await ctx.send(f'{sending_user} Source code {URL}')

def setup(bot):
    bot.add_cog(SourceCode(bot))