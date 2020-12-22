from discord.ext import commands
import datetime
from datetime import date
import os.path
import os

from Modules.Scraper import Scraper
from Modules.TimeConvert import TimeConvert

Now = datetime.datetime.now()

class SCMoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       
    #This function utilises the scraper and difference in time to give a difference in money generated for rsi
    @commands.command(pass_context=True, name='SCMoney', aliases=['scmoneyscraper'], no_pm=True)
    async def SCMoney(self, ctx, *args):
        #define the file to use
        directory = 'fundingGoals.txt'
        #ets the user know this will take some time
        await ctx.send('This takes a couple of seconds....')
        #if the file is found
        if os.path.isfile(directory):
            #open the file
            file = open(directory, 'r+')
            #read the lines
            lines = file.readlines()

            #if the file is empty
            if os.stat(directory).st_size == 0:
                #set a current value to 0 and time to now
                file.write('0')
                file.write('\n')
                file.write(str(Now))
            #if it's not empty
            else:
                #set a counter to increment for each line fo the document
                count : int = 0
                #go through each line in the document
                for line in lines:
                    #if the line is empty
                    if line == "\n":
                        #for the first line
                        if count == 0:
                            #set it to 0 and create a new line
                            lines[0] = '0 \n'
                            #for the second line 
                        elif count == 1:
                            #set the second line for now
                            lines[1] = f'{str(Now)}'    
                    #increment the counter                
                    count += 1
                #this checks the second line and formats it correctly 
                #if the count is 1 and the is a new line in the first line
                if count == 1 and '\n' in lines[0]:
                    #set the second line to now 
                    file.write(f'{str(Now)}')
                #if there is no new line in the first line
                elif count == 1:
                    #create a new line and set it to now
                    file.write(f'\n{str(Now)}')
                #write the changes to the file
                with open(directory, 'w') as file:
                    file.writelines( lines )
            
            #sets a variable to know if to write to the file later
            WriteFile = False

            #validate the lines are the correct format
            #set the variable to the first line without the new line
            s = lines[0].replace('\n', '')
            #try to convert to an int
            try:
                i = int(s)
            except ValueError as verr:
                #if it can't convert it will set the first line to 0 and new line 
                lines[0] = '0 \n'
                #set the WriteFile variable to true
                WriteFile = True
                #continue out the try 
                pass
            #throws an error is there is an issue with converting
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print(f'Failed to convert {s} to an int\n{exc}') 
            
            #set the variable to the second line without the new line
            DateString = lines[1].replace('\n', '')
            #set the format of the datetime
            format = '%Y-%m-%d %H:%M:%S.%f'
            #make sure it is in the correct format
            try:
                datetime.datetime.strptime(DateString, format)
            except ValueError as verr:
                #if it can't convert it will set the second line to now
                lines[1] = str(Now)
                #set the WriteFile variable to true
                WriteFile = True
                #continue out the try 
                pass
            #throws an error is there is an issue with converting
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print(f'Failed to convert {s} to an int\n{exc}') 

            #if the write file is set to true it will write the changes to the file
            if WriteFile == True:
                with open(directory, 'w') as file:
                    file.writelines( lines )

            #close the file to re-open it
            file.close()
            #open the file
            file = open(directory, 'r+')
            #read the lines
            lines = file.readlines()
            #get values from the file
            oldMoney, oldTime = lines[0], lines[1]
            dateTimeObj = datetime.datetime.strptime(oldTime, format)
            #call the scraper function with the returned value being an int
            newMoney = Scraper()
            #calculate the difference between the new and old value
            moneyDiff = int(newMoney) - int(oldMoney)
            #call the time difference function
            timeDiff = TimeConvert(dateTimeObj, Now)
            #send a message with these values
            statement = 'Chris Roberts has ${:,} making him ${:,} richer in {}'.format(int(newMoney), moneyDiff, timeDiff)
            await ctx.send(statement)
            #replaces the values in the file with the new values
            file.seek(0)
            file.truncate()
            file.write(newMoney)
            file.write('\n')
            file.write(str(Now))
            file.close()
            #if there is a difference the Money command is called to display the money meme
            if moneyDiff > 0:
                await ctx.invoke(self.bot.get_command('Money'))          
        else:
            #if the file is not found it will create a new file
            file = open(directory, 'w+')
            #call the scraper function with the returned value being an int
            moneySpent = Scraper()
            #send a message with these values
            statement = 'Star Citizen has raised ${:,} at the time of {}'.format(int(moneySpent), Now)
            await ctx.send(statement)
            #store the values in the file
            file.write(moneySpent)
            file.write('\n')
            file.write(str(Now))
            file.close()
            #if there is a difference the Money command is called to display the money meme
            await ctx.invoke(self.bot.get_command('Money'))

def setup(bot):
    bot.add_cog(SCMoney(bot))