##### Example plugin template to be used to copy and paste 
# Will be fairly verboose to allow easy understanding and interaction with Melody Annotator
#########################################################

#########################################################
def setup():
    pass
''' An optional function that can be run to check if dependencies are missing. 
This includes certain web fourms, config preferences, imports from python missing, etc
'''

#########################################################
def pluginCheck():
    return False
''' This is trusted apon the plugin creator to write a way to check if the plugin works. 
Please minimize how much it interacts with the internet/system and focus more if it can work correctly its various functions.
'''
#########################################################
def removal():
    pass
''' An optional function that removes anything that was UNIQUELY made by them. Maybe uninstalling a really obscured python packet. 
Don't forget to include safety checks that you are not affecting the user to much
'''

#########################################################
def init():
    pass
''' This is a funciton that will be ran by default everytime MelodyAnt has been ran.
'''

#########################################################
def categoryRequest():
    pass
''' An optional function thats highly encourage to be used
This defines how it can interact with melody with certain permissions.
The categories are seperated by commas: UI, Mouse, Keyboard, Buttons, Network, Filesystem, High priv access.
'''

#########################################################
'''
Whatever the plugin is meant to do goes here
'''

##########################################################
# --The default function that will kick off the plugin-- #
##########################################################
if __name__ == "pluginTemplate": # Change this!
    print("I was imported")
    # Start importing needed imports here such as sys, path, or whatever.
    init()