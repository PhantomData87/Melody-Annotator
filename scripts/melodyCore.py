#Adding plugins
from sys import path as mod
from os.path import abspath as ful
mod.insert(0, ful('../plugins')) # To include the other directory to have working plugins
import pluginMediator as pm

#Gui
import tkinter as tk
from tkinter import Grid
from tkinter import Label
from tkinter import Button
from tkinter import Canvas
from tkinter import Frame
from tkinter import Text

# For a globally defined plugin mediator
plug = pm.plugs()

class notes():
    def __init__(self):
        """ The main attracting to the app I hope.
        To organize, sort, and categorize unorganized text into easy to defined paragrahps.
        """
        pass
    def organize(self):
        """ Defined soon
        """
        pass
    def pluginCheck(self):
        """ Defined soon
        """
        pass

class noteNode():
    def __init__(self, keyPair, localInfo, localFile):
        """ This is a simple template to map and relate
        other noteNodes. And its used by the 'notes' class
        """
        self._info = localInfo
        self._file = localFile
        self._identifiers = keyPair
        
        self._left = None
        self._right = None
        self._behind = None

class melody():
    def __init__(self, root):
        """ Initialize the GUI of the application
        Here is where most of the UI will be loaded and rendered.
        The first 2 paragraphs of code will be used throughtout the rest of the application,
        and will be used to remember any changes made to the application.
        """
        self.root = root

        # Colors used in app
        self.mainBackgroundColor = "#231F1F"
        self.mainSidebarColor = "#2F2828"
        self.mainForegroundColor = "#413535"
        self.mainSeperatorColor = "#524C4C"
        self.inputColor = "#332626"
        self.tabOptionColor = "#332626"
        self.writeForegroundColor = "#272738"
        self.writeBackgroundColor = "#272738"
        self.textWriteColor = "#FFFFFF"
        self.labelColor = "#FFFFFF"
        self.sideLabelColor = "#928E8E"
        self.titleColor = "#FFFFFF"
        #self.backgroundCheck()

        # Size of certain UI elements
        self.seperatorFrame = 35
        self.seperatorSize = 5
        self.nonSeperatorSize = self.seperatorFrame - self.seperatorSize
        self.movingSidebar = 225
        self.writeBlockPadX = 100
        self.writeBlockPadY = 10
        self.buttonPadY = 2
        self.buttonPadX = 2
        self.buttonWidth = 5
        self.buttonHeight = 1
        
        # Defining mainframe and label for root window                                                                                                              # From here, we have two things in screen.
        self.mainLabel = Label(self.root, text="Melody-Annotator v0.0.1 | Opened in: ", background = self.mainBackgroundColor, foreground = self.labelColor)        # A widget acting as a title of the app
        self.mainLabel.pack(fill=tk.X, side='top')                                                                                                                  # and will be placed on the top.
        self.mainFrame = Frame(self.root, background = self.mainBackgroundColor)                                                                                    # A widget acting as a container for more widgets
        self.mainFrame.pack(fill=tk.BOTH, expand=True, side='bottom')                                                                                               # placed on the bottom.

        # Defining frames for mainframe.                                                                                                                            # From here, in the bottom frame we make two more frames.
        self.inFrame1 = Frame(self.mainFrame, background = self.mainBackgroundColor)                                                                                # A frame that will hold in more widgets
        self.inFrame1.pack(fill=tk.BOTH, expand=True, side='top')                                                                                                   # thats placed at the top.
        self.inFrame2 = Frame(self.mainFrame, background = self.mainSidebarColor, height = self.seperatorFrame)                                                     # A frame that will represent the current line, charcter counter, and word count
        self.inFrame2.pack(fill=tk.X, expand=False, side='bottom')                                                                                                  # Placed at the bottom.
        
        #***# Defining widgets for inFrame2                                                                                                                         # As discused before, it will contain widgets
        self.if2Seperator = Canvas(self.inFrame2, background = self.mainSeperatorColor, highlightthickness = 0, height = self.seperatorSize)                        # that are meant to represent and track
        self.if2Seperator.pack(fill=tk.X, side='top')                                                                                                               # the current file/tree's
        self.if2WordLabel = Label(self.inFrame2, text="Hi 1", background = self.mainSidebarColor, foreground = self.sideLabelColor)                                 # word counter, character counter, line nunmber
        self.if2WordLabel.pack(side='right')                                                                                                                        # and possibly more.
        self.if2CharacterLabel = Label(self.inFrame2, text="Hi 2", background = self.mainSidebarColor, foreground = self.sideLabelColor)                            #
        self.if2CharacterLabel.pack(side='right')                                                                                                                   #

        #***# Defining frames for inFrame1 & Weight distribution in inFrame1                                                                                        # Here we will define how the UI will be resized when the window changes.
        self.inFrame1.grid_rowconfigure(0, weight=0)                                                                                                                # This will affectif1FileBar.
        self.inFrame1.grid_rowconfigure(1, weight=1)                                                                                                                # This will affect if1Side & if1Block.
        self.inFrame1.grid_columnconfigure(0, weight=0)                                                                                                             # This will affect if1Side & if1FileBar.
        self.inFrame1.grid_columnconfigure(1, weight=1)                                                                                                             # This will affect if1Block.

        self.if1Side = Frame(self.inFrame1, background = self.mainSidebarColor, width = self.nonSeperatorSize)                                                      # This frame will be used for a nice &
        self.if1Side.pack_propagate(0)                                                                                                                              # (This frame kept getting resized by its children)
        self.if1Side.grid(row=1, column=0, sticky="nsew")                                                                                                           # easy side menu.
        self.if1Block = Frame(self.inFrame1, background = self.writeBackgroundColor)                                                                                # This frame will be used for opening and displaying
        self.if1Block.grid(row=1, column=1, sticky="nsew")                                                                                                          # text and the tree structure of heading/files.
        self.if1FileBar = Frame(self.inFrame1, background = self.mainForegroundColor, height = self.seperatorFrame)                                                 # This frame will be used to explicitely show which heading/file
        self.if1FileBar.pack_propagate(0)                                                                                                                           # (This frame kept getting resized by its children)
        self.if1FileBar.grid(row=0, column=0, columnspan=2, sticky="new")                                                                                           # you are looking, and to switch between different tabs.

        #*******# Defining widget & frames for if1Block. Including weight distribution                                                                              # This frame contains the various tabs and text output.
        self.if1Block.grid_rowconfigure(0, weight = 1)                                                                                                              # This will affect all widgets/frames.
        self.if1Block.grid_columnconfigure(0, weight = 0)                                                                                                           # This will affect treeViewFrame, searchFrame, spareFrame.
        self.if1Block.grid_columnconfigure(1, weight = 1)                                                                                                           # This will affect writingBlock.

        self.treeViewFrame = Frame(self.if1Block, background = self.mainForegroundColor, width = self.movingSidebar)                                                # This frame is used for selecting need headers and files from a tree menu.
        self.searchFrame = Frame(self.if1Block, background = self.mainForegroundColor, width = self.movingSidebar)                                                  # This frame is used to search in the files.
        self.spareFrame = Frame(self.if1Block, background = self.mainForegroundColor, width = self.movingSidebar)                                                   # Doesn't have a purpose just yet. It might soon.

        self.treeViewFrame.grid(row=0, column=0, sticky="nsew")                                                                                                     #
        self.searchFrame.grid(row=0, column=0, sticky="nsew")                                                                                                       #
        self.spareFrame.grid(row=0, column=0, sticky="nsew")                                                                                                        #

        self.writingBlock = Text(self.if1Block, highlightthickness = 0, background = self.writeForegroundColor, foreground = self.textWriteColor,                   # Used for displaying text from headers and files
        borderwidth = 0, padx = self.writeBlockPadX, pady = self.writeBlockPadY)                                                                                    # and will apply easy editing and deleting to those files
        self.writingBlock.grid(row=0, column=1, sticky="nswe")                                                                                                      # And it's dynammic to resizing.

        #*******# Defining widgets for if1Side                                                                                                                      # The helpful sidebar that I hope is helpful (Will cause popups or affect UI):
        self.expandButton = Button(self.if1Side, background = self.mainSidebarColor, command = self.emptyAction, highlightthickness = 0, borderwidth = 0)           # This will expand/shrink the UI tabs for treeview, searching and such.
        self.commandButton = Button(self.if1Side, background = self.mainSidebarColor, command = self.emptyAction, highlightthickness = 0, borderwidth = 0)          # A command pallet button!.
        self.pluginsButton = Button(self.if1Side, background = self.mainSidebarColor, command = self.emptyAction, highlightthickness = 0, borderwidth = 0)          # To manage plugins.
        self.undoButton = Button(self.if1Side, background = self.mainSidebarColor, command = self.emptyAction, highlightthickness = 0, borderwidth = 0)             # To undo.
        self.redoButton = Button(self.if1Side, background = self.mainSidebarColor, command = self.emptyAction, highlightthickness = 0, borderwidth = 0)             # To redo.

        self.expandButton.pack(side='top', expand=False, pady = self.buttonPadY)                                                                                    # Ensuring none of the buttons can expand.
        self.commandButton.pack(side='top', expand=False, pady = self.buttonPadY)                                                                                   # And they are defined to be placed on the top left.
        self.pluginsButton.pack(side='top', expand=False, pady = self.buttonPadY)                                                                                   #
        self.undoButton.pack(side='top', expand=False, pady = self.buttonPadY)                                                                                      #
        self.redoButton.pack(side='top', expand=False, pady = self.buttonPadY)                                                                                      #

        self.aboutButton = Button(self.if1Side, background = self.mainSidebarColor, command = self.emptyAction, highlightthickness = 0, borderwidth = 0)            # To see a more detailed view of the app
        self.openFileButton = Button(self.if1Side, background = self.mainSidebarColor, command = self.emptyAction, highlightthickness = 0, borderwidth = 0)         # To open/add a new file for this app to look at
        self.configButton = Button(self.if1Side, background = self.mainSidebarColor, command = self.emptyAction, highlightthickness = 0, borderwidth = 0)           # To change settings of this thing with some nice UI

        self.configButton.pack(side='bottom', expand=False, pady = self.buttonPadY)                                                                                 # Ensuring none of the buttons can expand.
        self.openFileButton.pack(side='bottom', expand=False, pady = self.buttonPadY)                                                                               # And they are defined to be placed on the bottom left.
        self.aboutButton.pack(side='bottom', expand=False, pady = self.buttonPadY)                                                                                  #

        #*******# Defining widgets for if1FileBar and a frame. Including weight distribution
        self.choiceBar = Frame(self.if1FileBar, background = self.mainBackgroundColor, height = self.if1FileBar.winfo_reqheight(),                                                # Due to UI bugs, this has been divided into two frames;
        width = self.movingSidebar + self.nonSeperatorSize - self.seperatorSize)                                                                                    # This will contain the option to turn off/on treeViewFrame, searchFrame & spareFrame.
        self.headingBar = Frame(self.if1FileBar, background = self.mainForegroundColor, height = self.nonSeperatorSize)                                             # This frame contains the header, and two button for editing the text box below.

        self.fileSeperator = Canvas(self.if1FileBar, background = self.mainSeperatorColor, height = self.seperatorSize, highlightthickness = 0)                     # This is a UI cosmetic.
        self.currentView = Label(self.headingBar, text="Te current file or whatever", background = self.mainForegroundColor,                                        # This is to display the name of the header/file.
        foreground = self.titleColor, anchor = "w", padx = 5)                                                                                                       #
        self.buttonleft = Button(self.headingBar, background = self.mainForegroundColor, command=self.emptyAction, highlightthickness = 0, borderwidth = 0)         # A button that will be defined soon.
        self.buttonRight = Button(self.headingBar, background = self.mainForegroundColor, command=self.emptyAction, highlightthickness = 0, borderwidth = 0)        # A button that will be defined soon.

        self.choiceBar.pack(side='left', expand=False)                                                                                                              #
        self.fileSeperator.pack(side='bottom', anchor="s", expand=True, fill=tk.X)                                                                                  #
        self.headingBar.pack(side='top', anchor="w", expand=True, fill=tk.X)                                                                                        #
        
        self.currentView.pack(side='left', anchor="w", expand=True, fill=tk.X)                                                                                      #
        self.buttonRight.pack(side='right', anchor="e", expand=False)                                                                                               #
        self.buttonleft.pack(side='right', anchor="e", expand=False)                                                                                                #
        
        #***********# Defining widgets for treeViewFrame
        # TO DO ish;    https://www.pythontutorial.net/tkinter/tkinter-listbox/
        #***********# Defining widgets for searchFrame
        # TO DO ish;    https://www.pythontutorial.net/tkinter/tkinter-scrollbar/
        #***********# Defining widgets for spareFrame
        # TO DO ish;    https://pythonguides.com/python-tkinter-read-text-file/

        
        #***********# Defining widgets for ChoiceBar and custom art by using frames
        self.padding = Canvas(self.choiceBar, background = self.mainBackgroundColor ,width = self.if1Side.winfo_reqwidth(),                                         # Due to where the bottom UI will be placed. I required a bit of padding to move the three tabs.
        height = self.choiceBar.winfo_reqheight(), borderwidth = 0, highlightthickness = 0)                                                                         # 
        self.padding.pack(side="left", expand=True)                                                                                                                 # 
        self.choiceBarUI = Frame(self.choiceBar, background = self.mainBackgroundColor, width = self.movingSidebar, height = self.choiceBar.winfo_reqheight())      # A made a new frame for the tab buttons. This made by life easier.
        self.choiceBarUI.pack_propagate(0)                                                                                                                          # To prevent the UI widgets from resizing the frame.
        self.choiceBarUI.pack(side='right', expand=True)                                                                                                            # 
        
        self.filesButton = Button(self.choiceBarUI, background = self.mainForegroundColor, command = self.emptyAction, padx=0, pady=0,                              # This will cause the treeViewFrame to appear on the UI.
        highlightthickness = 0, borderwidth = 0, width = self.buttonWidth, height = self.buttonHeight)                                                              # 
        self.searchButton = Button(self.choiceBarUI, background = self.tabOptionColor, command = self.emptyAction, padx=0, pady=0,                                  # This will cause the searchFrame to appear on the UI.
        highlightthickness = 0, borderwidth = 0, width = self.buttonWidth, height = self.buttonHeight)                                                              # 
        self.spareButton = Button(self.choiceBarUI, background = self.tabOptionColor, command = self.emptyAction, padx=0, pady=0,                                   # This will cause the spareFrame to appear on the UI.
        highlightthickness = 0, borderwidth = 0, width = self.buttonWidth, height = self.buttonHeight)                                                              # 
        self.filesButton.pack(side="left", expand=False, anchor = "sw", padx = self.buttonPadX)                                                                     # First.
        self.searchButton.pack(side="left", expand=False, anchor = "sw", padx = self.buttonPadX)                                                                    # Middle.
        self.spareButton.pack(side="left", expand=False, anchor = "sw", padx = self.buttonPadX)                                                                     # Last.

    def emptyAction(self):
        """ A test function to see if the buttons were implemented correctly
        So far all the buttons added work and appear where they belong
        """
        print("I work")

    def backgroundCheck(self):
        """ Originally was going to check in a file the current color settings.
        Now it might be deprecated soon.
        """
        pass

if __name__ == "__main__":
    """ Only runs when this script is specifically called.
    Why aren't these defined in the class? Because that would be restricting.
    Maybe some want it to never move, and others want a bigger screen size.
    """
    root = tk.Tk()
    root.geometry("1440x1024")                                                                                                                                      # Width x Height
    root.resizable(True, True)                                                                                                                                      # Set these to False to prevent resizing
    melody(root)
    root.mainloop()
