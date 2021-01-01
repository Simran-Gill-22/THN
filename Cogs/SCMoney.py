from discord.ext import commands
import datetime
from datetime import date
import os.path
import os
import json

from Modules.Scraper import Scraper
from Modules.TimeConvert import TimeConvert

Now = datetime.datetime.now()

class SCMoney(commands.Cog):
    'This category handles how much money earned and time has passed for RSI'
    def __init__(self, bot):
        self.bot = bot
       
    #This function utilises the scraper and difference in time to give a difference in money generated for rsi
    @commands.command(pass_context=True, name='SCMoney', aliases=['scmoneyscraper'], no_pm=True)
    async def SCMoney(self, ctx, *args):
        'This command lets the user know how much money Chris Roberts has made in a certain time'
        #define the file to use
        directory = 'Json/fundingGoals.json'
        #lets the user know this will take some time
        await ctx.send('This takes a couple of seconds....')
        #if the file is found
        oldMoney = ""
        oldTime = ""
        if os.path.isfile(directory):
            with open(directory) as f:
                #load the contents
                data = json.load(f)
                if len(data['Amount']) == 0:
                    oldMoney = 0
                else:
                    oldMoney = data['Amount']
                
                if len(data['Time']) == 0:
                    oldTime = str(Now)
                else:
                    oldTime = data['Time']
            TimeFormat = '%Y-%m-%d %H:%M:%S.%f'
            dateTimeObj = datetime.datetime.strptime(oldTime, TimeFormat)
            #call the scraper function with the returned value being an int
            newMoney = Scraper()
            #calculate the difference between the new and old value
            moneyDiff = int(newMoney) - int(oldMoney)
            #call the time difference function
            timeDiff = TimeConvert(dateTimeObj, Now)
            #send a message with these values
            statement = 'Chris Roberts has ${:,} making him ${:,} richer in {}'.format(int(newMoney), moneyDiff, timeDiff)
            await ctx.send(statement)
            #save the new json with the new values
            data['Amount'] = newMoney
            data['Time'] = str(Now)
            with open(directory, "w") as f:
                json.dump(data, f, indent=4)
            #if there is a difference the Money command is called to display the money meme
            if moneyDiff > 0:
                await ctx.invoke(self.bot.get_command('Money'))          
        else:
            #call the scraper function with the returned value being an int
            moneySpent = Scraper()
            #send a message with these values
            statement = 'Star Citizen has raised ${:,} at the time of {}'.format(int(moneySpent), Now.strftime("%d-%m-%Y %H:%M:%S"))
            await ctx.send(statement)
            #store the values in the file
            NewFundingGoal = {
                "Amount":moneySpent,
                "Time":str(Now) 
            }
            #write the new token to the file created
            with open(directory, "w") as write_file:
                json.dump(NewFundingGoal, write_file, indent=4)

            #if there is a difference the Money command is called to display the money meme
            await ctx.invoke(self.bot.get_command('Money'))

def setup(bot):
    bot.add_cog(SCMoney(bot))