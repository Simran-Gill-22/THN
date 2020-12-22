from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Clears the chat in the channel it is called using the number from the command
    @commands.command(pass_context=True, name='Clear', aliases=['clearmessages'], no_pm=True)
    async def Clear(self, ctx, number):
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

def setup(bot):
    bot.add_cog(Clear(bot))