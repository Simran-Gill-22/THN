import json
import os
import random

#random image scripts
def FolderBuilder(channel_name, UseFolders):
        path =''
        if UseFolders:
                #set variables
                image_list = os.listdir(channel_name) 
                folder_string = ''
                image_string = ''

                try:
                        image_string = random.choice(image_list) 
                        path =  f'{channel_name}/{image_string}'
                except IndexError:
                        print (f"{channel_name} no images added")
        else:
                directory = ""
                if channel_name == "magic-mike-appreciation-society":
                        directory = "Images/mm.json"
                elif channel_name == "chris-roberts-appreciation-society":
                        directory = "Images/cr.json"
                elif channel_name == "keanu-reeves-appreciation-society":
                        directory = "Images/kr.json"

                if os.path.isfile(directory):
                        #open the json file
                        with open(directory) as f:
                                #load the contents
                                data = json.load(f)
                                LengthOfFile = len(data) - 1
                                NumberOfImage = random.randint(0, LengthOfFile)
                                path = data[str(NumberOfImage)]

        return path