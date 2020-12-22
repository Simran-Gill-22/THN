import os
import random

#this function gets scrapes the rsi site
def FolderBuilder(channel_name):
        #random image scripts
        folder_list = os.listdir(channel_name) 
        folder_string = random.choice(folder_list) 
        image_list = os.listdir(channel_name + '/' + folder_string + '/')
        image_string = random.choice(image_list)
        path = channel_name + '/' + folder_string + '/' + image_string
        #pushes the image
        return path