import os.path
from os import path
import random

#this function gets scrapes the rsi site
def AllFolderExist():
        FoldersToCheck = ['magic-mike-appreciation-society', 'chris-roberts-appreciation-society', 'keanu-reeves-appreciation-society', 'Memes']  
        print("""
        ######################
        ###Checking Folders###
        ######################
        """)
        for Folder in FoldersToCheck:
            if not path.isdir(Folder):
                try:
                    os.mkdir(Folder)
                except OSError:
                    print (f"Creation of the directory {Folder} failed")
                else:
                    print (f"Successfully created the directory {Folder}")
            else:
                print(f'Folder {Folder} exist already')
        return 