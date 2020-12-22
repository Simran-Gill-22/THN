import os
import random

#random image scripts
def FolderBuilder(channel_name):
        #set variables
        folder_list = os.listdir(channel_name) 
        folder_string = ''
        image_list = ''
        image_string = ''
        path =''

        try:
                folder_string = random.choice(folder_list) 
        except IndexError:
                print (f"{channel_name} Folder is empty")

        try:
                image_list = os.listdir(channel_name + '/' + folder_string + '/') 
        except IndexError:
                print (f"{folder_list}/{folder_string} Folder is empty")
        
        try:
                image_string = random.choice(image_list)
                path =  f'{channel_name}/{folder_string}/{image_string}'
        except IndexError:
                print (f"{folder_list}/{folder_string}/{image_list} Folder is empty")

        return path