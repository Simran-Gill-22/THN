import os
import json
import os.path
from os import path


#set variables
UseFolders = ''
MoneyMemeURL = ''
SmileMemeURL = ''
directoryConfig = 'Json/Config.json'
directoryMeme = 'Images/meme.json'
OwnerApproval = ''
GroupApproval = ''
GroupApprovalList = ''
OwnerID = ''


def AllFolderExist():
    if UseFolders:
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

#function to just return a value
def UseFoldersCheck():
    return UseFolders

#function to just return a value
def GetMoneyMemeURL():
    return MoneyMemeURL

#function to just return a value
def GetMoneySmileURL():
    return SmileMemeURL

#function to just return a value
def GetOwnerApproval():
    return OwnerApproval

#function to just return a value
def GetGroupApproval():
    return GroupApproval

#function to just return a value
def GetGroupApprovalList():
    return GroupApprovalList

#function to just return a value
def GetOwnerID():
    return OwnerID

#check if the file exist
if os.path.isfile(directoryConfig):
    #load the file
    with open(directoryConfig) as f:
        data = json.load(f)
        #if the key is not in the file
        if 'UseFolders' not in data:
            #set it to false by default
            UseFolders = False
        else:
            #set it to a vaiable
            UseFolders = data['UseFolders']
            #if it is false
            if UseFolders == 'False':
                #set it to variable
                UseFolders = False
                #Check and create all folders exist
                AllFolderExist()
            else:
                #set it to true 
                UseFolders = True

        if 'OwnerApproval' not in data:
            #if not it will default to false
            OwnerApproval = False
        #if it is in the app
        else:
            #check if it is true or false
            if data['OwnerApproval'] == 'True' or data['OwnerApproval'] == 'False':
                #if it is set the variable appropriatly
                if data['OwnerApproval'] == 'True':
                    OwnerApproval = True
                elif data['OwnerApproval'] == 'False':
                    OwnerApproval = False
                #check the owner id is in the data
                if 'OwnerID' in data:
                    #if yes set it 
                    OwnerID = data['OwnerID']

        #check if the value is in the config
        if 'GroupApproval' not in data:
            #if not it will default to false
            GroupApproval = False
        #if it is in the app
        else:
            #check if it is true or false
            if data['GroupApproval'] == 'True' and not OwnerApproval and data['ApprovalList']:
                GroupApproval = True
                GroupApprovalList = data['ApprovalList']
            else:
                GroupApproval = False
                GroupApprovalList = ''
else:
    #set to default if the file is not found
    UseFolders = False

#check if the file exist
if not UseFolders:
    #load the file
    if os.path.isfile(directoryMeme):
        with open(directoryMeme) as f:
            data = json.load(f)
        #go through all the keys
        for i in data:
            #if the key is found
            if i == 'Memes':
                #go through all the arrays in the key
                for FoundToken in data['Memes']:
                    #if the key is found
                    if FoundToken['Name'] == 'Money':
                        #if found write the new value
                        MoneyMemeURL = FoundToken['URL']
                    #if the key is found
                    if FoundToken['Name'] == 'Smile':
                        #if found write the new value
                        SmileMemeURL = FoundToken['URL']
        #if it is not found set the use folders to no 
        if not SmileMemeURL or not MoneyMemeURL:
            UseFolders = False
    #set to default if the file is not found
    else:
        UseFolders = False




