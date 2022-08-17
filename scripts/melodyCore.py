# Adding plugins
from sys import path as mod
from os.path import abspath as ful
mod.insert(0, ful('../plugins')) # To include the other directory to have working plugins
import pluginMediator as pm

# Gui
import tkinter as tk
from tkinter import Grid
from tkinter import Label
from tkinter import Button
from tkinter import Canvas
from tkinter import Frame
from tkinter import Text
from tkinter import Scrollbar
from tkinter import Entry

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

class createWindow():
    def __init__(self, root, windowType):
        """ For any button pressed in the UI.
        This will make a secondary window that will dissapear when the user exits it.
        """
        self.root = root
        self.window = tk.Toplevel(root)
        self.closingButton = Button(self.window, text='Close', command=self.window.destroy)
        self.closingButton.pack(side='bottom', expand=True, fill=tk.Y)
        print(windowType)

class melody():
    def __init__(self, root):
        """ Initialize the GUI of the application
        Here is where most of the UI will be loaded and rendered.
        The first 2 paragraphs of code will be used throughtout the rest of the application,
        and will be used to remember any changes made to the application.
        """
        self.root = root
        width = "1024"
        height = "1440"
        self.root.geometry(height+"x"+width)                                                                                                                                      # Width x Height
        self.root.resizable(True, True)                                                                                                                                      # Set these to False to prevent resizing

    # Configuration
        # Colors used in app
        self.mainBackgroundColor = "#231F1F"
        self.mainSidebarColor = "#2F2828"
        self.mainForegroundColor = "#413535"
        self.mainSeperatorColor = "#524C4C"
        self.searchBoxColor = "#332626"
        self.tabOptionColor = "#332626"
        self.writeForegroundColor = "#272738"
        self.writeBackgroundColor = "#272738"
        self.textWriteColor = "#FFFFFF"
        self.searchColor = "#FFFFFF"
        self.fadedSearchColor = "#555555"
        self.labelColor = "#FFFFFF"
        self.sideLabelColor = "#928E8E"
        self.titleColor = "#FFFFFF"
        self.mainHighlightColor = "#00FF00"

        # Size of certain UI elements
        self.seperatorFrame = 35
        self.seperatorSize = 5
        self.nonSeperatorSize = self.seperatorFrame - self.seperatorSize
        self.movingSidebar = 225
        self.currentWidth = self.movingSidebar
        self.movingSidebarMin = 155
        self.movingSidebarMax = int(width) - self.movingSidebar * 3
        self.animatedSidebarCreep = 10
        self.inputPadX = 5
        self.writeBlockPadX = 100
        self.writeBlockPadY = 10
        self.buttonPadY = 2
        self.buttonPadX = 2
        self.buttonWidth = 5
        self.buttonHeight = 1

    # Windows & UI of the APP    
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
        self.if1Block.grid_propagate(False)                                                                                                                         #
        self.if1FileBar = Frame(self.inFrame1, background = self.mainForegroundColor, height = self.seperatorFrame)                                                 # This frame will be used to explicitely show which heading/file
        self.if1FileBar.pack_propagate(0)                                                                                                                           # (This frame kept getting resized by its children)
        self.if1FileBar.grid(row=0, column=0, columnspan=2, sticky="new")                                                                                           # you are looking, and to switch between different tabs.

        #*******# Defining widget & frames for if1Block. Including weight distribution                                                                              # This frame contains the various tabs and text output.
        self.if1Block.grid_rowconfigure(0, weight = 1)                                                                                                              # This will affect all widgets/frames.
        self.if1Block.grid_columnconfigure(0, weight = 0)                                                                                                           # This will affect treeViewFrame, searchFrame, spareFrame.
        self.if1Block.grid_columnconfigure(1, weight = 1)  
        self.if1Block.grid_columnconfigure(2, weight = 1)                                                                                                           # This will affect writingBlock.

        self.spareFrame = Frame(self.if1Block, background = self.mainForegroundColor, width = self.movingSidebar)                                                   # Doesn't have a purpose just yet. It might soon.
        self.spareFrame.pack_propagate(0)                                                                                                                           #
        self.searchFrame = Frame(self.if1Block, background = self.mainForegroundColor, width = self.movingSidebar)                                                  # This frame is used to search in the files.
        self.searchFrame.pack_propagate(0)                                                                                                                          #
        self.treeViewFrame = Frame(self.if1Block, background = self.mainForegroundColor, width = self.movingSidebar)                                                # This frame is used for selecting need headers and files from a tree menu.
        self.treeViewFrame.pack_propagate(0)                                                                                                                        #

        self.treeViewFrame.grid(row=0, column=0, sticky="nsew")                                                                                                     #
        self.searchFrame.grid(row=0, column=0, sticky="nsew")                                                                                                       #
        self.spareFrame.grid(row=0, column=0, sticky="nsew")                                                                                                        #

        self.seperatorDrag = Canvas(self.if1Block, background = self.mainSeperatorColor, width = self.seperatorSize, borderwidth = 0, highlightthickness = 0)       # This can be pulled by the user to resize the current frame.
        self.seperatorDrag.grid(row=0, column=1, sticky="nsw")                                                                                                      # 

        self.writingBlock = Text(self.if1Block, highlightthickness = 0, background = self.writeForegroundColor, foreground = self.textWriteColor,                   # Used for displaying text from headers and files
        borderwidth = 0, padx = self.writeBlockPadX, pady = self.writeBlockPadY)                                                                                    # and will apply easy editing and deleting to those files
        self.writingBlock.grid(row=0, column=2, sticky="nswe")                                                                                                      # And it's dynammic to resizing.

        self.writingScroll = Scrollbar(self.if1Block, orient='vertical', command=self.writingBlock.yview)                                                           # Making the text box scrollable by linking this scrollbar to that
        self.writingScroll.grid(row=0, column=3, sticky="nse")                                                                                                      #
        self.writingBlock.configure(yscrollcommand=self.writingScroll.set)                                                                                          # Ensuring it communicates back to the scroll widget

        #*******# Defining widgets for if1Side                                                                                                                      # The helpful sidebar that I hope is helpful (Will cause popups or affect UI):
        self.expandButton = Button(self.if1Side, background = self.mainSidebarColor, command = self.hideBar, highlightthickness = 0, borderwidth = 0)               # This will expand/shrink the UI tabs for treeview, searching and such.
        self.commandButton = Button(self.if1Side, background = self.mainSidebarColor, command = lambda: self.userWindow("Pallet"),                                  # A command pallet button!.
        highlightthickness = 0, borderwidth = 0)                                                                                                                    #
        self.pluginsButton = Button(self.if1Side, background = self.mainSidebarColor, command = lambda: self.userWindow("Plugin"),                                  # To manage plugins.
        highlightthickness = 0, borderwidth = 0)                                                                                                                    #
        self.undoButton = Button(self.if1Side, background = self.mainSidebarColor, command = self.emptyAction, highlightthickness = 0, borderwidth = 0)             # To undo.
        self.redoButton = Button(self.if1Side, background = self.mainSidebarColor, command = self.emptyAction, highlightthickness = 0, borderwidth = 0)             # To redo.

        self.expandButton.pack(side='top', expand=False, pady = self.buttonPadY)                                                                                    # Ensuring none of the buttons can expand.
        self.commandButton.pack(side='top', expand=False, pady = self.buttonPadY)                                                                                   # And they are defined to be placed on the top left.
        self.pluginsButton.pack(side='top', expand=False, pady = self.buttonPadY)                                                                                   #
        self.undoButton.pack(side='top', expand=False, pady = self.buttonPadY)                                                                                      #
        self.redoButton.pack(side='top', expand=False, pady = self.buttonPadY)                                                                                      #

        self.aboutButton = Button(self.if1Side, background = self.mainSidebarColor, command = lambda: self.userWindow("About"),                                     # To see a more detailed view of the app
        highlightthickness = 0, borderwidth = 0)                                                                                                                    #
        self.openFileButton = Button(self.if1Side, background = self.mainSidebarColor, command = lambda: self.userWindow("File"),                                   # To open/add a new file for this app to look at
        highlightthickness = 0, borderwidth = 0)                                                                                                                    #
        self.configButton = Button(self.if1Side, background = self.mainSidebarColor, command = lambda: self.userWindow("Config"),                                   # To change settings of this thing with some nice UI
        highlightthickness = 0, borderwidth = 0)                                                                                                                    #

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
        
        #***********# Defining widgets for treeViewFrame & treeViewFrameBar
        self.treeViewFrameBar = Frame(self.treeViewFrame, background = self.mainForegroundColor, width = self.movingSidebar)                                        #
        self.treeViewFrameBar.pack(side="top", anchor="n")                                                                                                          #
        
        self.button1 = Button(self.treeViewFrameBar, background = self.mainForegroundColor, command=self.emptyAction, highlightthickness = 0, borderwidth = 0       #
        , width = self.buttonHeight, height = self.buttonHeight)                                                                                                    #
        self.button2 = Button(self.treeViewFrameBar, background = self.mainForegroundColor, command=self.emptyAction, highlightthickness = 0, borderwidth = 0       #
        , width = self.buttonHeight, height = self.buttonHeight)                                                                                                    #
        self.button3 = Button(self.treeViewFrameBar, background = self.mainForegroundColor, command=self.emptyAction, highlightthickness = 0, borderwidth = 0       #
        , width = self.buttonHeight, height = self.buttonHeight)                                                                                                    #
        self.button1.pack(side="left", fill = tk.X, expand = True, padx = self.buttonPadX)                                                                          #
        self.button2.pack(side="left", fill = tk.X, expand = True, padx = self.buttonPadX)                                                                          #
        self.button3.pack(side="left", fill = tk.X, expand = True, padx = self.buttonPadX)                                                                          #

        self.FileLabel = Label(self.treeViewFrame, text="Tree branch(es): 0\nFile(s) open: 0", background = self.mainForegroundColor,                               #
        foreground = self.titleColor, anchor="w", justify="left")                                                                                                   #
        self.FileLabel.pack(side="top", anchor="n", expand=False, fill=tk.X)                                                                                        #

        self.buttonCanvas = Canvas(self.treeViewFrame, highlightthickness = 0, borderwidth = 0, background = self.mainForegroundColor)                              #
        self.buttonScrollVer = Scrollbar(self.treeViewFrame, orient='vertical', command=self.buttonCanvas.yview)                                                    #
        self.buttonScrollHor = Scrollbar(self.treeViewFrame, orient='horizontal', command=self.buttonCanvas.xview)                                                  #
        self.buttonCanvas.configure(yscrollcommand=self.buttonScrollVer.set, xscrollcommand=self.buttonScrollHor.set)                                               #

        self.buttonScrollVer.pack(side="right", anchor="se", fill=tk.Y)                                                                                             #
        self.buttonScrollHor.pack(side="bottom", anchor="s", fill=tk.X)                                                                                             #
        self.buttonCanvas.pack(side="top", anchor="n", fill=tk.BOTH, expand=True)                                                                                   #

        self.buttonFrame = Frame(self.buttonCanvas, background = self.mainForegroundColor)                                                                          #
        self.innerButtonCanvas = self.buttonCanvas.create_window(0,0, window=self.buttonFrame, anchor="n")                                                          #

        #***********# Defining widgets for searchFrame & searchFrameBar & searchInputFrame
        self.searchFrameBar = Frame(self.searchFrame, background = self.mainForegroundColor, width = self.movingSidebar)                                            #
        self.searchFrameBar.pack(side="top", anchor="n")                                                                                                            #
        
        self.search1 = Button(self.searchFrameBar, background = self.mainForegroundColor, command=self.emptyAction, highlightthickness = 0, borderwidth = 0         #
        , width = self.buttonHeight, height = self.buttonHeight)                                                                                                    #
        self.search2 = Button(self.searchFrameBar, background = self.mainForegroundColor, command=self.emptyAction, highlightthickness = 0, borderwidth = 0         #
        , width = self.buttonHeight, height = self.buttonHeight)                                                                                                    #
        self.search3 = Button(self.searchFrameBar, background = self.mainForegroundColor, command=self.emptyAction, highlightthickness = 0, borderwidth = 0         #
        , width = self.buttonHeight, height = self.buttonHeight)                                                                                                    #
        self.search4 = Button(self.searchFrameBar, background = self.mainForegroundColor, command=self.emptyAction, highlightthickness = 0, borderwidth = 0         #
        , width = self.buttonHeight, height = self.buttonHeight)                                                                                                    #
        self.search5 = Button(self.searchFrameBar, background = self.mainForegroundColor, command=self.emptyAction, highlightthickness = 0, borderwidth = 0         #
        , width = self.buttonHeight, height = self.buttonHeight)                                                                                                    #
        self.search1.pack(side="left", fill = tk.X, expand = True, padx = self.buttonPadX)                                                                          #
        self.search2.pack(side="left", fill = tk.X, expand = True, padx = self.buttonPadX)                                                                          #
        self.search3.pack(side="left", fill = tk.X, expand = True, padx = self.buttonPadX)                                                                          #
        self.search4.pack(side="left", fill = tk.X, expand = True, padx = self.buttonPadX)                                                                          #
        self.search5.pack(side="left", fill = tk.X, expand = True, padx = self.buttonPadX)                                                                          #

        self.searchInputFrame = Frame(self.searchFrame, background = self.searchBoxColor, width = self.movingSidebar)                                               #
        self.searchInputFrame.pack(side="top", anchor="n", expand=False, fill=tk.X, padx = self.inputPadX)                                                          #

        self.inputSearch = Entry(self.searchInputFrame, background = self.searchBoxColor, foreground = self.fadedSearchColor,                                       #
        highlightthickness = 0, borderwidth = 0)                                                                                                                    #
        self.inputSearch.insert(0, "Type here to search...")
        self.inputSearch.pack(side = "left", anchor = "w", expand = True, fill=tk.X, padx = self.inputPadX)                                                         #
        self.clearText = Button(self.searchInputFrame, background = self.searchBoxColor, highlightthickness = 0, borderwidth = 0,                                   #
        command = self.clearInputSearch)                                                                                                                            #
        self.clearText.pack(side = "right", anchor = "e", expand = False, fill=tk.X)                                                                                #

        self.searchCanvas = Canvas(self.searchFrame, highlightthickness = 0, borderwidth = 0, background = self.mainForegroundColor)                                #
        self.searchScrollVer = Scrollbar(self.searchFrame, orient='vertical', command=self.searchCanvas.yview)                                                      #
        self.searchCanvas.configure(yscrollcommand=self.searchScrollVer.set)                                                                                        #

        self.searchScrollVer.pack(side="right", anchor="se", fill=tk.Y, expand = True)                                                                              #
        self.searchCanvas.pack(side="top", anchor = "nw", fill=tk.BOTH, expand = True)                                                                              #

        self.searchResultFrame = Frame(self.searchCanvas, background = self.mainForegroundColor)                                                                    #
        self.innerSearchCanvas = self.searchCanvas.create_window(0,0, window=self.searchResultFrame, anchor="n")                                                    #

        #***********# Defining widgets for spareFrame
        # Eventually this will obtain a purpose

        
        #***********# Defining widgets for ChoiceBar                                                                                                                # This will allow for the main UI to change and work for the needs of the user
        self.padding = Canvas(self.choiceBar, background = self.mainBackgroundColor ,width = self.if1Side.winfo_reqwidth(),                                         # Due to where the bottom UI will be placed. I required a bit of padding to move the three tabs.
        height = self.choiceBar.winfo_reqheight(), borderwidth = 0, highlightthickness = 0)                                                                         # 
        self.padding.pack(side="left", expand=True)                                                                                                                 # 
        self.choiceBarUI = Frame(self.choiceBar, background = self.mainBackgroundColor, width = self.movingSidebar, height = self.choiceBar.winfo_reqheight())      # A made a new frame for the tab buttons. This made by life easier.
        self.choiceBarUI.pack_propagate(0)                                                                                                                          # To prevent the UI widgets from resizing the frame.
        self.choiceBarUI.pack(side='right', expand=True)                                                                                                            # 
        
        self.filesButton = Button(self.choiceBarUI, background = self.mainForegroundColor, command = self.switchFrameTree, padx=0, pady=0,                          # This will cause the treeViewFrame to appear on the UI.
        highlightthickness = 0, borderwidth = 0, width = self.buttonWidth, height = self.buttonHeight)                                                              # 
        self.searchButton = Button(self.choiceBarUI, background = self.tabOptionColor, command = self.switchFrameSearch, padx=0, pady=0,                            # This will cause the searchFrame to appear on the UI.
        highlightthickness = 0, borderwidth = 0, width = self.buttonWidth, height = self.buttonHeight)                                                              # 
        self.spareButton = Button(self.choiceBarUI, background = self.tabOptionColor, command = self.switchFrameSpare, padx=0, pady=0,                              # This will cause the spareFrame to appear on the UI.
        highlightthickness = 0, borderwidth = 0, width = self.buttonWidth, height = self.buttonHeight)                                                              # 
        self.filesButton.pack(side="left", expand=False, anchor = "sw", padx = self.buttonPadX)                                                                     # First.
        self.searchButton.pack(side="left", expand=False, anchor = "sw", padx = self.buttonPadX)                                                                    # Middle.
        self.spareButton.pack(side="left", expand=False, anchor = "sw", padx = self.buttonPadX)                                                                     # Last.

    # Binding events used in the UI.
        # For using the scrollwheel when interacting with the file tree
        self.buttonCanvas.bind_all("<MouseWheel>", self.buttonCanvasMouseWheel)                                                                                     # This is for Windows to bind to the mousewheel. (And uses delta)
        self.buttonCanvas.bind_all("<Button-4>", self.buttonCanvasMouseWheel)                                                                                       # For linux to bind towards the UP direction of the mousewheel
        self.buttonCanvas.bind_all("<Button-5>", self.buttonCanvasMouseWheel)                                                                                       # For linux to bind towards the DOWN direction of the mousewheel.        

        # For using the scrollwheel when interacting with the search list
        self.searchCanvas.bind_all("<MouseWheel>", self.searchCanvasMouseWheel)                                                                                     #
        self.searchCanvas.bind_all("<Button-4>", self.searchCanvasMouseWheel)                                                                                       #
        self.searchCanvas.bind_all("<Button-5>", self.searchCanvasMouseWheel)                                                                                       #

        # For the search field when looking up files
        self.inputSearch.bind("<Button>", self.removePlaceHold)                                                                                                     #
        self.inputSearch.bind("<Enter>", self.placeholdText)                                                                                                        #
        self.inputSearch.bind("<Leave>", self.placeholdText)                                                                                                        #

        # For the seperator that can be moved around via a mouse
        self.seperatorDrag.bind("<B1-Motion>", self.seperatorDragged)                                                                                               #
        self.seperatorDrag.bind("<Button-1>", self.switchSeperatorColorOn)                                                                                          #
        self.seperatorDrag.bind("<ButtonRelease-1>", self.switchSeperatorColorAway)                                                                                 #

    def emptyAction(self):
        """ A test function to see if the buttons were implemented correctly
        So far all the buttons added work and appear where they belong
        """
        print("I work")

    # UI Events from Buttons & Events
    def switchFrameTree(self):
        """ Switches to the file tree view frame & updates UI """
        if self.filesButton['background'] == self.tabOptionColor:                                                                                                   #
            self.treeViewFrame.tkraise()                                                                                                                            #
            self.filesButton.config(background = self.mainForegroundColor)                                                                                          #
            self.searchButton.config(background = self.tabOptionColor)                                                                                              #
            self.spareButton.config(background = self.tabOptionColor)                                                                                               #

    def switchFrameSearch(self):
        """ Switches to the search method frame & updates UI """
        if self.searchButton['background'] == self.tabOptionColor:                                                                                                  #
            self.searchFrame.tkraise()                                                                                                                              #
            self.filesButton.config(background = self.tabOptionColor)                                                                                               #
            self.searchButton.config(background = self.mainForegroundColor)                                                                                         #
            self.spareButton.config(background = self.tabOptionColor)                                                                                               #

    def switchFrameSpare(self):
        """ Switches to the spare frame & updates UI """
        if self.spareButton['background'] == self.tabOptionColor:                                                                                                   #
            self.spareFrame.tkraise()                                                                                                                               #
            self.filesButton.config(background = self.tabOptionColor)                                                                                               #
            self.searchButton.config(background = self.tabOptionColor)                                                                                              #
            self.spareButton.config(background = self.mainForegroundColor)                                                                                          #

    def switchSeperatorColorOn(self, event):
        """ To highlight the seperator when the mouse runs over it """
        if self.seperatorDrag['background'] == self.mainSeperatorColor:                                                                                             #
            self.seperatorDrag.configure(background = self.mainHighlightColor)                                                                                      #
    
    def switchSeperatorColorAway(self, event):
        """ To remove the highlighting of the seperator when the mouse is over it"""
        if self.seperatorDrag['background'] == self.mainHighlightColor:                                                                                             #
            self.seperatorDrag.configure(background = self.mainSeperatorColor)                                                                                      #
            self.currentWidth = self.treeViewFrame.winfo_reqwidth()                                                                                                 #

    def seperatorDragged(self, event):                                                                                                                              #
        referanceWidth = self.treeViewFrame.winfo_reqwidth()                                                                                                        #
        if event.x < 0:                                                                                                                                             #
            if referanceWidth + event.x < self.movingSidebarMin:                                                                                                    #
                return None                                                                                                                                         #
            self.treeViewFrame.configure(width = referanceWidth + event.x - self.seperatorSize)                                                                     #
            self.searchFrame.configure(width = referanceWidth + event.x - self.seperatorSize)                                                                       #
            self.spareFrame.configure(width = referanceWidth + event.x - self.seperatorSize)                                                                        #
        elif event.x > self.seperatorDrag.winfo_reqwidth():                                                                                                         #
            if referanceWidth + event.x > self.movingSidebarMax:                                                                                                    #
                return None                                                                                                                                         #
            self.treeViewFrame.configure(width = referanceWidth + event.x)                                                                                          #
            self.searchFrame.configure(width = referanceWidth + event.x)                                                                                            #
            self.spareFrame.configure(width = referanceWidth + event.x)                                                                                             #

    # Keyboard & Mouse events
    def clearInputSearch(self):
        """ Removes all text from the input searchbar offered by the searchFrame """
        self.inputSearch.delete(0, tk.END)                                                                                                                          #
        self.inputSearch.config(foreground = self.fadedSearchColor)                                                                                                 #
        self.inputSearch.insert(0, "Type here to search...")                                                                                                        #

    def placeholdText(self, event):
        """ Will put some placeholder text for the input field.
        This will run when the input field is empty
        """
        if self.inputSearch.get() == '':                                                                                                                            #
            self.inputSearch.config(foreground = self.fadedSearchColor)                                                                                             #
            self.inputSearch.insert(0, "Type here to search...")                                                                                                    #

    def removePlaceHold(self, event):
        """ Removes the placeholder text when user clicks the field
        """
        if "Type here to search..." in self.inputSearch.get() or self.inputSearch.get() in "Type here to search...":                                                #
            self.inputSearch.delete(0, tk.END)                                                                                                                      #
            self.inputSearch.config(foreground = self.searchColor)                                                                                                  #

    def buttonCanvasMouseWheel(self, event):
        """ A simple function to update the canvas based on scrollwheel
        This is required due to how I wish for all objects in the canvas (such as a button)
        to be scrollable.
        """
        if event.num == 5 or event.delta < 0:                                                                                                                       #
            self.buttonCanvas.yview_scroll(1, "units")                                                                                                              #
        else:                                                                                                                                                       #
            self.buttonCanvas.yview_scroll(-1, "units")                                                                                                             #

    def searchCanvasMouseWheel(self, event):
        """ A simple function to update the canvas based oon the scrollwheel
        This is required if I wish for all of the search results to be scrollable.
        """
        if event.num == 5 or event.delta < 0:                                                                                                                       #
            self.searchCanvas.yview_scroll(1, "units")                                                                                                              #
        else:                                                                                                                                                       #
            self.searchCanvas.yview_scroll(-1, "units")                                                                                                             #

    def showBar(self):
        """ To show the selection frames to have less writting space
        """
        width = self.treeViewFrame.winfo_reqwidth()                                                                                                                 #
        if width == 1:                                                                                                                                              #
            self.treeViewFrame.grid(row=0, column=0, sticky="nsew")                                                                                                 #
            self.searchFrame.grid(row=0, column=0, sticky="nsew")                                                                                                   #
            self.spareFrame.grid(row=0, column=0, sticky="nsew")                                                                                                    #
            self.seperatorDrag.grid(row=0, column=1, sticky="nsw")                                                                                                  #
            self.choiceBarUI.pack(side='right', expand=True)                                                                                                        #

        if self.treeViewFrame.winfo_reqwidth() >= self.currentWidth:                                                                                                #
            self.expandButton.configure(command= self.hideBar)                                                                                                      #
            self.treeViewFrame.configure(width = self.currentWidth)                                                                                                 #
            self.searchFrame.configure(width = self.currentWidth)                                                                                                   #
            self.spareFrame.configure(width = self.currentWidth)                                                                                                    #
            return None

        self.treeViewFrame.configure(width = width + self.animatedSidebarCreep)                                                                                     #
        self.searchFrame.configure(width = width + self.animatedSidebarCreep)                                                                                       #
        self.spareFrame.configure(width = width + self.animatedSidebarCreep)                                                                                        #
        self.root.after(1, self.showBar)                                                                                                                            #
    
    def hideBar(self):
        """ To hide the selection frames to have more writting space.
        """
        width = self.treeViewFrame.winfo_reqwidth()                                                                                                                 #
        if width == 1 or width <= self.animatedSidebarCreep:                                                                                                        #
            self.expandButton.configure(command= self.showBar)                                                                                                      #
            self.treeViewFrame.configure(width = 1)                                                                                                                 #
            self.searchFrame.configure(width = 1)                                                                                                                   #
            self.spareFrame.configure(width = 1)                                                                                                                    #
            self.treeViewFrame.grid_forget()                                                                                                                        #
            self.searchFrame.grid_forget()                                                                                                                          #
            self.spareFrame.grid_forget()                                                                                                                           #
            self.seperatorDrag.grid_forget()                                                                                                                        #
            return None

        if width == self.currentWidth:
            self.choiceBarUI.pack_forget()            

        self.treeViewFrame.configure(width = width - self.animatedSidebarCreep)                                                                                     #
        self.searchFrame.configure(width = width - self.animatedSidebarCreep)                                                                                       #
        self.spareFrame.configure(width = width - self.animatedSidebarCreep)                                                                                        #
        self.root.after(1, self.hideBar)                                                                                                                            #
    
    # Secondary Windows
    def userWindow(self, windowType):
        """ Fairly self explanitory,
        it initializes a new class that will act as a custom popup window
        """
        createWindow(self.root, windowType)                                                                                                                         #

if __name__ == "__main__":
    """ Only runs when this script is specifically called."""
    root = tk.Tk()
    melody(root)
    root.mainloop()
