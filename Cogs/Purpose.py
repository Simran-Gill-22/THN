from discord.ext import commands
class Purpose(commands.Cog):
    'This category handles the purpose of the bot'
    def __init__(self, bot):
        self.bot = bot

    #lets the user know the purpose of the bot
    @commands.command(pass_context=True, name='Purpose', aliases=['sendpurposemessage'], no_pm=True)
    async def Purpose(self, ctx):
        'Let the user know the purpose of the bot'
        sending_user = ctx.author.mention
        return await ctx.send(f"""{sending_user} My purpose is to reply to all Summit1G emotes with :nauseated_face: & post memes of Chris Roberts, Magic Mike and Keanu Reeves""")

def setup(bot):
    bot.add_cog(Purpose(bot))