from tkinter import Text as T
import webbrowser as wb
import tkinter as tk
import re

class markdownView():                                                                                                                                                                                           # Welcome to more verboose comments. Again run the function found in melodyCore.py to remove them
    """ This is a fairly big class because Markdown is fairly hard to implement                                                                                                                                 #
    And if you were to read the code. You may notice that I neglect to include anythign really to chekc for HTLM (the reason for Markdown)                                                                      #
    Well, you right, but for know that it is how its going to be. I just wnated preety syntax. Unless am paid or motivated. I am not going to dedicate that much time                                           #
    To ensure that it has the entirety of Markdown implemnted (inclduing the htlm) ofr tkinter                                                                                                                  #
    """                                                                                                                                                                                                         #
    def __init__(self, root, startText, pad, location, colorPallet = ("#AAAAAA", "#272738", "#DDDDDD")):                                                                                                        # We only want to take in the bare minimum.
        self.setColor(colorPallet)                                                                                                                                                                              # Thus we mearly take in a set of colors
        self.displayFontName = 'Calibri'                                                                                                                                                                        # A font
        self.current = "r"                                                                                                                                                                                      # A variable to help us simplify the code
        self.nSize = 10
        self.bSize = 15                                                                                                                                                                                         # Size of the normal text
        self.root = root                                                                                                                                                                                        # And where melodyCore is at
                                                                                                                                                                                                                #
        self.markdownInterface = T(root, background = self.background, foreground = self.textColor, highlightthickness = 0, borderwidth = 0, wrap = tk.WORD, padx = pad[0], pady = pad[1], relief=tk.FLAT)      # Here we display markdown, however we remove symbols
        self.previewInterface = T(root, background = self.background, foreground = self.textColor, highlightthickness = 0, borderwidth = 0, wrap = tk.WORD, padx = pad[0], pady = pad[1], relief=tk.FLAT)       # This interface is meant to be a hybrid of rawInterface and markdownInterface. Symbols are kept here
        self.rawInterface = T(root, background = self.background, foreground = self.textColor, highlightthickness = 0, borderwidth = 0, wrap = tk.WORD, padx = pad[0], pady = pad[1], relief=tk.FLAT)           # Nothing fancy will happen here, and symbols are not removed
                                                                                                                                                                                                                #
        self.rawInterface.insert("1.0", startText)                                                                                                                                                              # In case we need to load a file, or for testing purposes
                                                                                                                                                                                                                #
        self.markdownInterface.grid(row=location[0], column=location[1], sticky='nswe')                                                                                                                         # Initializing on frame
        self.markdownInterface['state'] = tk.DISABLED                                                                                                                                                           # Ensuring the user cannot edit the interface
        self.previewInterface.grid(row=location[0], column=location[1], sticky='nswe')                                                                                                                          # Initializing on frame
        self.previewInterface.bindtags(self.previewInterface.bindtags() + ("basicMarkdown",))                                                                                                                   # Adding a custom tag so we can bind_class it
        self.rawInterface.grid(row=location[0], column=location[1], sticky='nswe')                                                                                                                              # Initializing on frame
        self.rawInterface.bindtags(self.rawInterface.bindtags() + ("basicMarkdown",))                                                                                                                           # Adding a custom tag so we can bind_class it
        self.rawInterface.tkraise()                                                                                                                                                                             # Making this the frame to appear
        self.rawInterface.focus_set()                                                                                                                                                                           # Setting the focus so tkinter knows which to respond first
                                                                                                                                                                                                                #
        self.markdownWritingRules = [                                                                                                                                                                           # Here we are defining a variety of Markdown's variosu rules. All of basic syntax is supported, as defined here. (https://www.markdownguide.org/basic-syntax/)
            ['```','Fenced Code Block',(f'{self.displayFontName} {self.nSize}', "#CC0000"),("Multiline", "```", "#333333")],                                                                                    # The only advanced syntax implemented so far, oh and this list follows a hierarchy
            ['^\[\d+\]: .+','Hyperlink Site', (f'{self.displayFontName} {self.nSize}', "#0000FF"), ('DetectUrl', "")],                                                                                          # This is used to reference the rest of the Hyperlinks
            ['\*\*\*\[.+\] ?\([^""]+.*\)\*\*\*','Hyperlink Italic Bold 1', (f'{self.displayFontName} {self.nSize} bold italic', "#0000FF"), ('Url', "***", 'Hyperlink Italic Bold 1', "#0000FF")],              # Making sure you can Italic bold a hyperlink
            ['\*\*\*\[.+\] ?\[\d+\].+?\*\*\*','Hyperlink Italic Bold 2', (f'{self.displayFontName} {self.nSize} bold italic', "#0000FF"), ('Url', "***", 'Hyperlink Italic Bold 2', "#0000FF")],                # Making sure you can bold a hyperlink
            ['\*\*\[.+\] ?\([^""]+.*\)\*\*','Hyperlink Bold 1', (f'{self.displayFontName} {self.nSize} bold', "#0000FF"), ('Url', "**", 'Hyperlink Bold 1', "#0000FF")],                                        # Making sure you can Italic a hyperlink
            ['\*\*\[.+\] ?\[\d+\].+?\*\*','Hyperlink Bold 2', (f'{self.displayFontName} {self.nSize} bold', "#0000FF"), ('Url', "**", 'Hyperlink Bold 2', "#0000FF")],                                          # Making sure you can Italic bold a hyperlink
            ['\*\[.+\] ?\([^""]+.*\)\*','Hyperlink Italic 1', (f'{self.displayFontName} {self.nSize} italic', "#0000FF"), ('Url', "*", 'Hyperlink Italic 1', "#0000FF")],                                       # Making sure you can bold a hyperlink
            ['\*\[.+\] ?\[\d+\].+?\*','Hyperlink Italic 2', (f'{self.displayFontName} {self.nSize} italic', "#0000FF"), ('Url', "*", 'Hyperlink Italic 2', "#0000FF")],                                         # Making sure you can Italic a hyperlink
            ['\[.+\] ?\([^""]+.*\)','Hyperlink', (f'{self.displayFontName} {self.nSize}', "#0000FF"), ('Url', "", 'Hyperlink', "#0000FF")],                                                                     # Ye regular hyperlink in one style
            ['\[.+\] ?\[\d+\].+?','Hyperlink', (f'{self.displayFontName} {self.nSize}', "#0000FF"), ('Url', "", "Hyperlink", "#0000FF")],                                                                       # Another style for hyperlinks, but this uses indexes
            ['<.*(@.)*.+>', 'Quick Hyperlink', (f'{self.displayFontName} {self.nSize}', "#0000FF"), ('Quick Url', "", "Quick Hyperlink")],                                                                      # A quick version to add a hyperlink
            ['^######[\S\s]+?$','Header 6',(f'{self.displayFontName} {self.nSize}', self.strongColor),("Left", "######")],                                                                                      # Adding the smallest header
            ['^#####[\S\s]+?$','Header 5',(f'{self.displayFontName} {15}', self.strongColor),("Left", "#####")],                                                                                                # Adding a bigger header
            ['^####[\S\s]+?$','Header 4',(f'{self.displayFontName} {20}', self.strongColor),("Left", "####")],                                                                                                  # Adding a bigger header
            ['^###[\S\s]+?$','Header 3',(f'{self.displayFontName} {25}', self.strongColor),("Left", "###")],                                                                                                    # Adding a bigger header
            ['^##[\S\s]+?$','Header 2',(f'{self.displayFontName} {30}', self.strongColor),("Left", "##")],                                                                                                      # Adding a bigger header
            ['^#[\S\s]+?$','Header 1',(f'{self.displayFontName} {40}', self.strongColor),("Left", "#")],                                                                                                        # Adding the biggest header
            ['^>+ ?######.+?','Blockquote Header 6',(f'{self.displayFontName} {self.nSize}', self.strongColor),("Blockquote Header 6", "> ######", ("#0000FF", "  ", "#333333"))],                              # Adding the smallest header for blockquotes
            ['^>+ ?#####.+?','Blockquote Header 5',(f'{self.displayFontName} {15}', self.strongColor),("Blockquote Header 5", "> #####", ("#0000FF", "  ", "#333333"))],                                        # Adding a bigger header for blockquotes
            ['^>+ ?####.+?','Blockquote Header 4',(f'{self.displayFontName} {20}', self.strongColor),("Blockquote Header 4", "> ####", ("#0000FF", "  ", "#333333"))],                                          # Adding a bigger header for blockquotes
            ['^>+ ?###.+?','Blockquote Header 3',(f'{self.displayFontName} {25}', self.strongColor),("Blockquote Header 3", "> ###", ("#0000FF", "  ", "#333333"))],                                            # Adding a bigger header for blockquotes
            ['^>+ ?##.+?','Blockquote Header 2',(f'{self.displayFontName} {30}', self.strongColor),("Blockquote Header 2", "> ##", ("#0000FF", "  ", "#333333"))],                                              # Adding a bigger header for blockquotes
            ['^>+ ?#.+?','Blockquote Header 1',(f'{self.displayFontName} {40}', self.strongColor),("Blockquote Header 1", "> #", ("#0000FF", "  ", "#333333"))],                                                # Adding the biggest header for blockquotes
            ['^>+ ?.*\*\*\*[^*]+\*\*\*.*','Blockquote Italic Bold',(f'{self.displayFontName} {self.nSize}', self.strongColor), ("Blockquote Italic Bold", ">", ("#0000FF", "  ", "#333333"))],                  # Adding a bold italic blockquote
            ['^>+ ?.*\*\*[^*]+\*\*.*','Blockquote Bold',(f'{self.displayFontName} {self.nSize}', self.strongColor), ("Blockquote Bold", ">", ("#0000FF", "  ", "#333333"))],                                    # Adding a bold blockquote
            ['^>+ ?.*\*[^*]+\*.*','Blockquote Italic',(f'{self.displayFontName} {self.nSize}', self.strongColor), ("Blockquote Italic", ">", ("#0000FF", "  ", "#333333"))],                                    # Adding a italic blockquote
            ['^>+ ?.+?','Blockquote',(f'{self.displayFontName} {self.nSize}', self.strongColor),("Blockquote", ">", ("#0000FF", "  ", "#333333"))],                                                             # Adding a regular blockquote
            ['\*\*\*[^*]+\*\*\*','Italic & Bold',(f'{self.displayFontName} {self.nSize} bold italic', self.strongColor),("Effect", "***")],                                                                     # Adding bold italic to text
            ['\*\*[^*]+\*\*','Bold',(f'{self.displayFontName} {self.nSize} bold', self.strongColor),("Effect", "**")],                                                                                          # Adding bold to text
            ['\*[^*]+\*','Italic',(f'{self.displayFontName} {self.nSize} italic', self.strongColor),("Effect", "*")],                                                                                           # Adding italic to text
            ['`.+?`','Code Phrase',(f'{self.displayFontName} {self.nSize}', "#CC0000"),("Both Colored", "`", "#333333")],                                                                                       # Adding a Code Sentance
            ['^\t*\- ','Unsorted List',(f'{self.displayFontName} {self.nSize}', "#777777"),("Replace Left", "-", "\u2022")],                                                                                    # You can make a list without numbers
            ['^\t*\d+\. ','Sorted List',(f'{self.displayFontName} {self.nSize}', "#777777"),("Skip", "")],                                                                                                      # You can make a list with numbers
            ['^---$','Horizontal Rules',(f'{self.displayFontName} {4}', "#FFFFFF"),("Both Colored", "---", "#BBBBBB")]                                                                                          # You can make a line appear in your doc
        #   [ If broken down to this format which extends the code by another 100 lines                                                                                                                         # Syntax
        #       "Example Regex Expression",                                                                                                                                                                     # Syntax
        #       "Markdown syntax name",                                                                                                                                                                         # Syntax
        #       ("Font + Size + Special if applicable", fontColor)                                                                                                                                              # Syntax
        #       ('Name to be procees by', 'text to remove', (extra data)),                                                                                                                                      # Syntax
        #   ]                                                                                                                                                                                                   # Syntax
        ]                                                                                                                                                                                                       #
        self.urlLocations = {}                                                                                                                                                                                  # To have a precise index of anything marked as a link from a feature from basic markdown
                                                                                                                                                                                                                #
        # Binding time                                                                                                                                                                                          # This is where all of my binding for this are defined
        self.root.bind_class("basicMarkdown", '<Key>', self.markdownDetect)                                                                                                                                     # Whenever you type, all text is added to all 3 interfaces (does not detect newline)
        self.root.bind_class("basicMarkdown", '<Key>', self.d, add="+")                                                                                                                                         # Whenever you type, all text is added to all 3 interfaces (does not detect newline)
        self.root.bind_class("basicMarkdown", '<Return>', self.logicalIndent)                                                                                                                                   # Whenever you try to make a list work by pressing enter. This runs
        self.root.bind_class("basicMarkdown", '<KP_Enter>', self.logicalIndent)                                                                                                                                 # Whenever you try to make a list work by pressing Keypad-enter. This runs
        self.root.bind_class("basicMarkdown", '`', self.dupeText)                                                                                                                                               # These will enclose the cursor with ``
        self.root.bind_class("basicMarkdown", '\'', self.dupeText)                                                                                                                                              # These will enclose the cursor with ''
        self.root.bind_class("basicMarkdown", '\"', self.dupeText)                                                                                                                                              # These will enclose the cursor with ""
        self.root.bind_class("basicMarkdown", '[', lambda event: self.dupeText(event, "]"))                                                                                                                     # These will enclose the cursor with []
        self.root.bind_class("basicMarkdown", '(', lambda event: self.dupeText(event, ")"))                                                                                                                     # These will enclose the cursor with ()
        self.root.bind_class("basicMarkdown", '{', lambda event: self.dupeText(event, "}"))                                                                                                                     # These will enclose the cursor with {}
                                                                                                                                                                                                                #
        self.markdownDetect()                                                                                                                                                                                   # Update the markdown found in markdownInterface
    
    def d(self, event):                                                                                                                                                                                         # A very simple test widget to know
        """ Debug tags with keys"""                                                                                                                                                                             # the current tag the cursor is on. Used for debugging
        print(self.previewInterface.tag_names(tk.INSERT))                                                                                                                                                       #

    def cycleView(self):                                                                                                                                                                                        # This is ran change the type of interface you see when you press the button
        """ This is to permit the user to switch between 3 specific widgets from Tkinter                                                                                                                        #    
        The widgets include:                                                                                                                                                                                    #
        rawInterface (Your generic basic tkinter Text widget with nothing special happening yet)                                                                                                                #
        previewInterface (A fairly hybrid version of Markdown where as you type, Markdown magic happens)                                                                                                        #
        markdownInterface (A read only interface where it fully transforms the text to the specifications of markdown)"""                                                                                       #
        if self.current == "r":                                                                                                                                                                                 # This is allow all edits done on a document to be updated when you press the button again.
            text = self.rawInterface.get(1.0, tk.END)[:-1]                                                                                                                                                      # This is done so backspaces and mass erasure can be registered on the other interfaces
            self.rawInterface.delete(1.0, tk.END)                                                                                                                                                               # Deleting a problematic newline
            self.previewInterface.insert(1.0, text)                                                                                                                                                             # Inserting text so we can modify it with tags
            self.previewInterface.tkraise()                                                                                                                                                                     # To make the tk.Text widget to appear
            self.current = "p"                                                                                                                                                                                  # 
        elif self.current == "p":                                                                                                                                                                               # 
            self.cleanUpText(self.previewInterface)                                                                                                                                                             # To cleanup any extra tags and to fix formatting
            text = self.previewInterface.get(1.0, tk.END)[:-1]                                                                                                                                                  # To obtain the text ina  raw manner
            self.markdownInterface['state'] = tk.NORMAL                                                                                                                                                         # This is to enable me to insert text inside of the markdownInterface
            self.markdownInterface.delete(1.0, tk.END)                                                                                                                                                          # Inserting text so we can modify it with tags
            self.markdownInterface.insert(1.0, text)                                                                                                                                                            # To make the tk.Text widget to appear
            self.markdownInterface.tkraise()                                                                                                                                                                    # 
            self.current = "m"                                                                                                                                                                                  # 
        elif self.current == "m":                                                                                                                                                                               # 
            self.cleanUpText(self.previewInterface)                                                                                                                                                             #
            text = self.previewInterface.get(1.0, tk.END)[:-1]                                                                                                                                                  # Deleting a problematic newline
            self.previewInterface.delete(1.0, tk.END)                                                                                                                                                           # Inserting text so we can modify it with tags
            self.rawInterface.insert(1.0, text)                                                                                                                                                                 # To make the tk.Text widget to appear
            self.rawInterface.tkraise()                                                                                                                                                                         # 
            self.current = "r"                                                                                                                                                                                  #
        self.markdownDetect()                                                                                                                                                                                   # Make sure markdown is being updated
        self.markdownInterface['state'] = tk.DISABLED                                                                                                                                                           # Disables the interface again.

    def dupeText(self, event, realChar = None):                                                                                                                                                                 # This will act as updateText() but it has the nice feature of adding more text
        """ You ever wondered how some text editors add an extra character?                                                                                                                                     #
        Well this is how (atleast one way) where we add the extra char based on the keyboard, and move the cursor back one line                                                                                 #
        """                                                                                                                                                                                                     #
        if realChar:                                                                                                                                                                                            # To prevent an error when am adding in more custom text
            choosenChar = realChar                                                                                                                                                                              # For simplicity
        else:                                                                                                                                                                                                   #
            choosenChar = event.char                                                                                                                                                                            # For simplicity
                                                                                                                                                                                                                #
        if self.current == "m":                                                                                                                                                                                 # To prevent the markdown interface from changing anything
            return 'break'                                                                                                                                                                                      # To prevent the markdown interface from changing anything
        elif self.current == "r":                                                                                                                                                                               #
            self.rawInterface.insert(tk.INSERT, choosenChar)                                                                                                                                                    # Than add new char to rawInterface
            self.rawInterface.mark_set("insert", "insert-1c")                                                                                                                                                   # To make sure the text cursor is inside the brackets
        elif self.current == "p":                                                                                                                                                                               #
            self.rawInterface.insert(tk.INSERT, choosenChar)                                                                                                                                                    # Than add new char to rawInterface
            self.previewInterface.mark_set("insert", "insert-1c")                                                                                                                                               # To make sure the text cursor is inside the brackets
        self.markdownDetect()                                                                                                                                                                                   # Check if new markdown is detected

    def markdownDetect(self, event=None):                                                                                                                                                                       # The core function & reason why this is a class
        """ This function runs in 3 steps.                                                                                                                                                                      #
        Cleanup any of the previous work,                                                                                                                                                                       #
        Check for possible locations for tags, add them, and defined how the tag should function                                                                                                                #
        Finally, edit the physical text. Why? Look at how Blockquotes work and you will understand why                                                                                                          #
        """                                                                                                                                                                                                     #
        if self.current == "r":                                                                                                                                                                                 #
            return None                                                                                                                                                                                         # Not wanting to run this unless markdown is needed
                                                                                                                                                                                                                #
        self.cleanUpText(self.previewInterface)                                                                                                                                                                 # Removing any unwanted text/tags that may conflict
                                                                                                                                                                                                                #
        # Loop through each replacement, unpacking it fully                                                                                                                                                     #
        for pattern, name, fontData, removalData in self.markdownWritingRules:                                                                                                                                  # This loop will look at all the markdownWritingRules defined above
            # Get the location indices of the given pattern                                                                                                                                                     #
            locationsLive = self.search_re(pattern, self.previewInterface.get('1.0', tk.END), removalData)                                                                                                      #
                                                                                                                                                                                                                #
            # Add tags where the search_re function found the pattern                                                                                                                                           # Activating our first helper function to define where the markdown syntax is located.
            for start, end in locationsLive:                                                                                                                                                                    #
                self.previewInterface.tag_add(name, start, end)                                                                                                                                                 # Using the markdown syntax name as the naem of the tag
                self.markdownInterface.tag_add(name, start, end)                                                                                                                                                #
                self.previewInterface.tag_lower(name)                                                                                                                                                           # The reason we call in "tag_lower" is to prevent multiple cases in the same area to
                self.markdownInterface.tag_lower(name)                                                                                                                                                          #
            # Configure the tag to use the specified font and color                                                                                                                                             # How markdown demands fonts, color, background, foreground, styles, size, and etc.
            if removalData[0] in ["Left", "Effect", "Skip", "Replace Left"]:                                                                                                                                    # However not all categories are defined here
                self.markdownInterface.tag_config(name, font=fontData[0], foreground=fontData[1])                                                                                                               # Either from lazyness or because it was defined elsewhere
                self.previewInterface.tag_config(name, font=fontData[0], foreground=fontData[1])                                                                                                                #
            elif removalData[0] in ["Both Colored", "Multiline"]:                                                                                                                                               #
                self.markdownInterface.tag_config(name, font=fontData[0], foreground=fontData[1], background=removalData[2])                                                                                    #
                self.previewInterface.tag_config(name, font=fontData[0], foreground=fontData[1], background=removalData[2])                                                                                     #
            elif "Block" in removalData[0]:                                                                                                                                                                     #
                self.markdownInterface.tag_config(name, font=fontData[0], foreground=fontData[1], background = removalData[2][2])                                                                               #
                self.previewInterface.tag_config(name, font=fontData[0], foreground=fontData[1], background = removalData[2][2])                                                                                #
            elif removalData[0] in ["Url", "Quick Url"]:                                                                                                                                                        #
                self.markdownInterface.tag_config(name, font=fontData[0], foreground=fontData[1], underline=True)                                                                                               #
                self.previewInterface.tag_config(name, font=fontData[0], foreground=fontData[1], underline=True)                                                                                                #
                                                                                                                                                                                                                #
        # Removinng unwanted text                                                                                                                                                                               # This will look at all the markdown syntax AFTER the tags are defined
        for pattern, name, ignored, removalData in self.markdownWritingRules:                                                                                                                                   # to safely remove all extra characters for markdownInterface via our second helper function
            self.editText(pattern, removalData)                                                                                                                                                                 # We do this after since we don't have to worry about the tags themselves. And this will allow us to insert new tags in

    def search_re(self, pattern, text, removalData = [None]):                                                                                                                                                   # This is one of the 2 most important functions. Returns a list of positions for a specific tag
        """ This function is fairly heavy and important.                                                                                                                                                        #
        To put simply, this is how I know where to put the majority of the tags in tkinter                                                                                                                      #
        Because throught tags you can re-enact markdown to an extent. Some of markdown require a lil more than mear tags                                                                                        #
        """                                                                                                                                                                                                     #
        foundHere = []                                                                                                                                                                                          # It has the very simple function of finding where all the various tags belong to
        multiPosition, offset = -1, 0                                                                                                                                                                           # This is for anything requiring more than a single line and another variable for possible offset
        for i, line in enumerate(text.splitlines(), 1):                                                                                                                                                         # First we split the massive text by its newline
            for found in re.finditer(pattern, line):                                                                                                                                                            # Than we iterate throught each instance of a line with our pattern
                if self.findPrevTag(f"{i}.{found.start()}", f"{i}.{found.end()}"):                                                                                                                              # We check if a tag has been set already in where we have
                    continue                                                                                                                                                                                    # If we had, than we simply skip thta instance and move on to the next one
                if removalData[0] == "Multiline":                                                                                                                                                               # If we have data saying this expression is a "Multiline"
                    if multiPosition == -1:                                                                                                                                                                     # We begin to keep track. If its an impossible num:
                        multiPosition = i                                                                                                                                                                       # We change it to the current line number
                        offset = found.start()                                                                                                                                                                  # and where exactly in the line it was found
                        foundHere.append((f"{multiPosition}.{offset}", "end"))                                                                                                                                  # And add a possible case where it was just left open for the rest of the text
                        continue                                                                                                                                                                                # Than we continue the loop
                    foundHere.pop(-1)                                                                                                                                                                           # If we did fail the first condition, we remove the extreme case
                    difference = i - multiPosition + 1                                                                                                                                                          # Find the difference to see how many lines it were
                    foundHere.append((f"{multiPosition}.{offset}", f"{multiPosition}.{offset}+{difference}lines"))                                                                                              # Add it in ot the tags
                    multiPosition = -1                                                                                                                                                                          # Reset the condition
                elif "Block" in removalData[0] or pattern == "^---$":                                                                                                                                           # If we got either a blockquote, or a horizontal line
                    foundHere.append((f"{i}.{found.start()}", f"{i}.{found.start()}+1lines"))                                                                                                                   # than we simply declare the tag to take ALL of the line
                elif removalData[0] == "Url":                                                                                                                                                                   # If we are receiving a URL, than
                    filler = found.group(0).split("]")[0][1:]                                                                                                                                                   # we do some clever splicing to find out whats the real text to display
                    foundHere.append((f"{i}.{found.start()}", f"{i}.{found.start() + len(filler)}"))                                                                                                            # Add it to the list
                else:                                                                                                                                                                                           # If its none of those, than we simply take its lenght
                    foundHere.append((f"{i}.{found.start()}", f"{i}.{found.end()}"))                                                                                                                            # and add it to the list
        return foundHere                                                                                                                                                                                        # Return the list

    def editText(self, pattern, removalData):                                                                                                                                                                   # This is a very impoant function that defines more one-time tags and edits text
        """ This is the most important function. This handles a lot of things that markdown demands and wants to see                                                                                            #
        Of course it won't do it all correctly, or it may be overcomplicated. Thus know this funciton is a WIP but it works for now                                                                             #
        Known bugs: Italics hates me (Sometimes it wants to respond, sometimes not)                                                                                                                             #
        """                                                                                                                                                                                                     # 
        def quickRemove(newSearchText, styleType):                                                                                                                                                              # Another function that may be used more, but right now its heavily used in the URL section
            """ This function was originally meant for the URL section because I realized I wrote                                                                                                               #
            the code in a way that permits a function to execute it.                                                                                                                                            #
            """                                                                                                                                                                                                 #
            for stylePattern, tagName, font, *unnecesary in self.markdownWritingRules:                                                                                                                          # We begin by trying to find where Italics, Bold, or Italics & Bold markdown rule is stored. (Since the list is ever changing)
                if tagName == styleType:                                                                                                                                                                        # If it found it, we proceed, otherwise the loop will end itself eventually
                    count = len(re.findall(stylePattern, newSearchText))                                                                                                                                        # We first count the number of times we find the symbol once in a single word like line
                    for result in re.finditer(stylePattern, newSearchText):                                                                                                                                     # We iterate each succesful case we find from the given text
                        if self.current == "p":                                                                                                                                                                 # If we are currently in previewMode, than
                            self.previewInterface.tag_add(tagName, f"{i}.{result.start()}", f"{i}.{result.end()}")                                                                                              # we simply add the tag in
                        else:                                                                                                                                                                                   # Otherwise
                            self.markdownInterface.tag_add(tagName, f"{i}.{result.start()}", f"{i}.{result.end()-count}")                                                                                       # We add in the tag in markdownMode and remove how long it is by the count
                    self.previewInterface.tag_raise(tagName)                                                                                                                                                    # Raise so the style overrides the current tag its sitting on
                    self.markdownInterface.tag_raise(tagName)                                                                                                                                                   # Raise so the style overrides the current tag its sitting on
                                                                                                                                                                                                                #
        if self.current == "p":                                                                                                                                                                                 # If in previewMode
            text = self.previewInterface.get('1.0', "end")                                                                                                                                                      # We obtain updated Text from previewView
        elif self.current == "m":                                                                                                                                                                               # If markdownMode
            text = self.markdownInterface.get('1.0', "end")                                                                                                                                                     # We obtain updated Text from markdownView
                                                                                                                                                                                                                #
        for i, line in enumerate(text.splitlines(), 1):                                                                                                                                                         # Split all newlines into a line
            for found in re.finditer(pattern, line):                                                                                                                                                            # Look matching pattern in current line
                                                                                                                                                                                                                #
                if removalData[0] == "Left":                                                                                                                                                                    # If we are modifying text from the left, than
                    self.markdownInterface.delete(f"{i}.{found.start()}", f"{i}.{found.start() + len(removalData[1])}")                                                                                         # Simply delete the starting characters
                                                                                                                                                                                                                #
                elif removalData[0] == "Effect" or removalData[0] == "Both Colored":                                                                                                                            # If we are adding a style, or Adding a background
                    self.markdownInterface.delete(f"{i}.{found.end() - len(removalData[1])}", f"{i}.{found.end()}")                                                                                             # We remove left &
                    self.markdownInterface.delete(f"{i}.{found.start()}", f"{i}.{found.start() + len(removalData[1])}")                                                                                         # right side characters
                                                                                                                                                                                                                # 
                elif "Block" in removalData[0]:                                                                                                                                                                 # If we are doing a blockquote, pray
                    foundExtraChar = re.search(f"#+", line)                                                                                                                                                     # We first find if this is a Header blockquote
                    if foundExtraChar != None:                                                                                                                                                                  # If so
                        self.markdownInterface.delete(f"{i}.{foundExtraChar.start()}", f"{i}.{foundExtraChar.end()}")                                                                                           # Than remove all those characters once and for all
                    foundChar = re.search(f">+", line)                                                                                                                                                          # Next we begin counting how many times we pressed ">"
                    self.markdownInterface.delete(f"{i}.{foundChar.start()}", f"{i}.{foundChar.end()}")                                                                                                         # And we promptely delete those characters
                    for j in range(0, len(foundChar.group(0))*2, 2):                                                                                                                                            # Than we begin inserting 2 spaces per ">" character
                        self.previewInterface.insert(f"{i}.{0}", removalData[2][1])                                                                                                                             # On both interfaces
                        self.markdownInterface.insert(f"{i}.{0}", removalData[2][1])                                                                                                                            # Than we add two custom tags
                    for j in range(0, len(foundChar.group(0))*2, 2):                                                                                                                                            # Do the same loop again, but
                        self.previewInterface.tag_add("indentBlockShown", f"{i}.{j}", f"{i}.{j+1}")                                                                                                             # One of these tags is to make it change color, giving the illusion that its drawing on the text after ">"
                        self.previewInterface.tag_add("indentBlockHidden", f"{i}.{j+1}", f"{i}.{j+2}")                                                                                                          # Another is to ensure the background from ">" does not appear, and is instead the background color
                        self.markdownInterface.tag_add("indentBlockShown", f"{i}.{j}", f"{i}.{j+1}")                                                                                                            # Repeat
                        self.markdownInterface.tag_add("indentBlockHidden", f"{i}.{j+1}", f"{i}.{j+2}")                                                                                                         # Repeat
                                                                                                                                                                                                                #
                    self.previewInterface.tag_config("indentBlockShown", background = removalData[2][0], font=f"{self.displayFontName} {self.bSize}")                                                           # We simply define what each tag does, this one will change its background
                    self.previewInterface.tag_config("indentBlockHidden", background = self.background, font=f"{self.displayFontName} {self.bSize}")                                                            # This one will hide itself with the main background
                    self.markdownInterface.tag_config("indentBlockShown", background = removalData[2][0], font=f"{self.displayFontName} {self.bSize}")                                                          #
                    self.markdownInterface.tag_config("indentBlockHidden", background = self.background, font=f"{self.displayFontName} {self.bSize}")                                                           #
                                                                                                                                                                                                                #                    
                    self.previewInterface.tag_raise("indentBlockShown")                                                                                                                                         # We ensure they are visible
                    self.markdownInterface.tag_raise("indentBlockShown")                                                                                                                                        # We ensure they are visible
                    self.previewInterface.tag_raise("indentBlockHidden")                                                                                                                                        # We ensure they are visible
                    self.markdownInterface.tag_raise("indentBlockHidden")                                                                                                                                       # We ensure they are visible
                                                                                                                                                                                                                #
                    newerText = self.previewInterface.get(f"{i}.0",f"{i}.0+1lines")                                                                                                                             # Obtain latest text
                    if "Italic Bold" in removalData[0]:                                                                                                                                                         # If you wanted to include some italics and bolding, than this will do it
                        quickRemove(newerText, "Italic & Bold")                                                                                                                                                 # Than we simply call our helper function by giving it our current text, and style
                    elif "Bold" in removalData[0]:                                                                                                                                                              # If you wnated to include some bolding,
                        quickRemove(newerText, "Bold")                                                                                                                                                          # Than we simply call our helper function by giving it our current text, and style
                    elif "Italic" in removalData[0]:                                                                                                                                                            # If you wanted to include some italics
                        quickRemove(newerText, "Italic")                                                                                                                                                        # Than we simply call our helper function by giving it our current text, and style
                    break                                                                                                                                                                                       # A nightmare is over
                                                                                                                                                                                                                #
                elif removalData[0] == "Multiline":                                                                                                                                                             # IF we encounter a multiline
                    self.markdownInterface.delete(f"{i}.{found.start()}", f"{i}.{found.start() + len(removalData[1])}")                                                                                         # We promptly remove its characters
                    continue                                                                                                                                                                                    # And continue
                                                                                                                                                                                                                #
                elif removalData[0] == "Url":                                                                                                                                                                   # THe third most hardest thing to implement. This will accept all forms of Markdown ways to opena  hyperlink on a browser. Specifically a browers unless paid to implement a new way
                    filler = found.group(0).split("]")[0][1:].replace("*","")                                                                                                                                   # Finding the raw text that must stay after the parsing is compelate
                    if "(" in found.group(0):                                                                                                                                                                   # IF URL format matches with "()" format. THan we proceed
                        location = found.group(0).split("(")[1]                                                                                                                                                 # First we obtain the location of the non-filler stuff like URL or heading
                        ulrSearcher = re.search('^<?.+>? [\"\'\(\)]|^<?.+>?', location)                                                                                                                         # Searches for the URL
                        if not ulrSearcher:                                                                                                                                                                     #
                            break                                                                                                                                                                               # If not, than assuemt he worst
                                                                                                                                                                                                                #
                        url = ulrSearcher.group(0)                                                                                                                                                              # We save the URL
                        urlHeading = re.search('[\"\'\(\)].+[\"\'\(\)]', location)                                                                                                                              # And the heading as well
                                                                                                                                                                                                                #
                        if not urlHeading:                                                                                                                                                                      # If we lack a heading because Markdown makes it optional
                            optionalHeading = ""                                                                                                                                                                # We simply make it an empty string
                        else:                                                                                                                                                                                   # 
                            url = url[:-2]                                                                                                                                                                      # Else, we remove from the url the last two characters because Markdown
                            optionalHeading = urlHeading.group(0)[1:-1]                                                                                                                                         # And from the heading we remove the last and first character because Markdown
                    elif "]" in found.group(0).replace(" ", "").split("][")[1]:                                                                                                                                 # IF we have the second URL format, than we simply repeat what we did above, in a unique way
                        location = re.search('\d+', found.group(0))                                                                                                                                             # Repeat
                        url = self.urlLocations[location.group(0)][0]                                                                                                                                           # Repeat
                        optionalHeading = self.urlLocations[location.group(0)][1]                                                                                                                               # Repeat
                        filler += " " + found.group(0).split("]")[-1].replace("[","").lstrip().replace("*","")                                                                                                  # This is complicated because I am removing so many things
                                                                                                                                                                                                                #
                    self.markdownInterface.delete(f"{i}.{found.start()}", f"{i}.{found.end()}")                                                                                                                 # Delete the ENTIRE url location
                    self.markdownInterface.insert(f"{i}.{found.start()}", filler.replace("[",""))                                                                                                               # Insert the filler
                                                                                                                                                                                                                #
                    self.previewInterface.tag_add(removalData[2], f"{i}.{found.start()}", f"{i}.{found.end()}")                                                                                                 # Add a tag on the filler
                    self.markdownInterface.tag_add(removalData[2], f"{i}.{found.start()}", f'{i}.{found.start() + len(filler) - (1 if removalData[1] != "" else 0)}')                                           # On both interfaces
                                                                                                                                                                                                                #
                    # For later https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python                                                           #
                    self.previewInterface.tag_bind(removalData[2], "<Button-1>", lambda event: wb.open(url))                                                                                                    # Add a custom tag bind that, when clicked will open a browser based on the URL
                    self.markdownInterface.tag_bind(removalData[2], "<Button-1>", lambda event: wb.open(url))                                                                                                   # This can be done by simply clicking on the link
                                                                                                                                                                                                                #
                elif removalData[0] == "Quick Url":                                                                                                                                                             # Far simplier, we simply extarct URL
                    url = found.group(0).split(">")[0][1:]                                                                                                                                                      # Delete where it belong the "<>" symbols
                    self.markdownInterface.delete(f"{i}.{found.end()-1}")                                                                                                                                       #
                    self.markdownInterface.delete(f"{i}.{found.start()}")                                                                                                                                       #
                                                                                                                                                                                                                #
                    self.previewInterface.tag_add(removalData[2], f"{i}.{found.start()}", f"{i}.{found.end() - 2}")                                                                                             # Add a tag based on where those symbols are at
                    self.markdownInterface.tag_add(removalData[2], f"{i}.{found.start()}", f"{i}.{found.end() - 2}")                                                                                            #
                                                                                                                                                                                                                #
                    # For later https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python                                                           #
                    self.previewInterface.tag_bind(removalData[2], "<Button-1>", lambda event: wb.open(url))                                                                                                    # Add a custom tag bind to open link
                    self.markdownInterface.tag_bind(removalData[2], "<Button-1>", lambda event: wb.open(url))                                                                                                   #
                                                                                                                                                                                                                #
                elif removalData[0] == "DetectUrl":                                                                                                                                                             # This is meant for the URL style 2 format. Where we take numbers as a referance for a link thats detected here to be saved
                    filler = found.group(0).split("]")[0][1:].replace("*","")                                                                                                                                   # We sort the filler since this will be our key
                    location = found.group(0).split("]")[1][2:]                                                                                                                                                 # We obtian locaiton of the URl and heading
                    ulrSearcher = re.search('^<?.+>? [\"\'\(\)]|^<?.+>?', location)                                                                                                                             # Find URL
                    if not ulrSearcher:                                                                                                                                                                         #
                        break                                                                                                                                                                                   #
                                                                                                                                                                                                                #
                    url = ulrSearcher.group(0)                                                                                                                                                                  # Save URL
                    urlHeading = re.search('[\"\'\(\)].+[\"\'\(\)]', location)                                                                                                                                  # Find heading
                                                                                                                                                                                                                #
                    if not urlHeading:                                                                                                                                                                          # If missing heading, than we simply make it an empty line
                        optionalHeading = ""                                                                                                                                                                    #
                    else:                                                                                                                                                                                       #
                        url = url[:-2]                                                                                                                                                                          # Else we remove characters remaining
                        optionalHeading = urlHeading.group(0)[1:-1]                                                                                                                                             # on both
                                                                                                                                                                                                                #
                    self.urlLocations[filler] = (url, optionalHeading)                                                                                                                                          # We save the URL into a class variable dictionary for later use
                                                                                                                                                                                                                #
                    self.markdownInterface.delete(f"{i}.{found.start()}", f"{i}.{found.end()}")                                                                                                                 # We delete the enitre line to prevent being found. This can be changed if this is not markdown. PLease let me know
                                                                                                                                                                                                                #
                elif removalData[0] == "Replace Left":                                                                                                                                                          # If we want to simply replace the left character isnetad of deleting it compleately.
                    amount = found.group(0).count("\t")*'\t'                                                                                                                                                    # Yes this is for the unsorted lists
                    self.markdownInterface.delete(f"{i}.{found.start()}", f"{i}.{found.start() + len(removalData[1])+1}")                                                                                       #
                    self.markdownInterface.insert(f"{i}.{found.start()}", amount+removalData[2])                                                                                                                #
                                                                                                                                                                                                                #
                elif removalData[0] == "Skip":                                                                                                                                                                  # A simple skip if nothing is needed from it.
                    break                                                                                                                                                                                       #

    def findPrevTag(self, start, end):                                                                                                                                                                          # This was made so I can begin avoiding deleting the entire interface because I added a new character and now it has to be checked for Markdown
        """ To find the previous tags that have already been made in markdownDetect.                                                                                                                            #
        To avoid tags on top of tags. Since tkinter is going to have to remember a lot of tags as the text file increases.                                                                                      #
        However their is an exception for things that has a specific function ike hyperlinks                                                                                                                    #
        """                                                                                                                                                                                                     #
        currentPos = start.split(".")[0]                                                                                                                                                                        # Obtain the current position
        for i in range(int(start.split(".")[1]), int(end.split(".")[1])):                                                                                                                                       # We begin a loop to check for all positions based on the position if a tag is present
            if self.previewInterface.tag_names(f"{currentPos}.{i}") and self.current == "p":                                                                                                                    # If we do detect one, we simply check if its true and what interface it belongs to
                prevTag = self.previewInterface.tag_names(f"{currentPos}.{i}")                                                                                                                                  # We save where the tag is for simplicity
                if "Hyper" in prevTag or "Quick Hyperlink" in prevTag or "Blocks" in prevTag:                                                                                                                   # If the tag begins with the words "Hyper", or "Quick Hyperlink" or, "Blocks" we ignore the tag
                    continue                                                                                                                                                                                    #
                return True                                                                                                                                                                                     # Otherwise we let the search_re() that the current tag should be skipped and ignored for change
            elif self.markdownInterface.tag_names(f"{currentPos}.{i}") and self.current == "m":                                                                                                                 # Repeat
                prevTag = self.markdownInterface.tag_names(f"{currentPos}.{i}")                                                                                                                                 # Repeat
                if "Hyper" in prevTag or "Blocks" in prevTag:                                                                                                                                                   # Repeat
                    continue                                                                                                                                                                                    # Repeat
                return True                                                                                                                                                                                     # Repeat
        return False                                                                                                                                                                                            # Otherwise, if all good, than we let search_re() know that the current tag is safe to be used since the text is fresh.

    def cleanUpText(self, interface):                                                                                                                                                                           # Meant to clean up both interfaces that uses Markdown.
        """ To remove any extra info from the previous scan.                                                                                                                                                    #
        Originally made for the blockquotes.                                                                                                                                                                    #
        """                                                                                                                                                                                                     #
        for i in reversed(interface.tag_ranges("indentBlockShown")):                                                                                                                                            # For all tags left with "indentBlockShown"
            interface.delete(str(i))                                                                                                                                                                            # Delete the spaces
        for i in reversed(interface.tag_ranges("indentBlockHidden")):                                                                                                                                           # For all tags left with "indentBlockHidden"
            interface.delete(str(i))                                                                                                                                                                            # Delete the spaces
        for tag in self.previewInterface.tag_names():                                                                                                                                                           # Now we simply delete all the remaining tags
            self.previewInterface.tag_delete(tag, "1.0", "end")                                                                                                                                                 # from start to end
        for tag in self.markdownInterface.tag_names():                                                                                                                                                          # On both interfaces
            self.markdownInterface.tag_delete(tag, "1.0", "end")                                                                                                                                                # Otherwise it will cause funky text to start to appear once you press your keyboard


    def logicalIndent(self, event):                                                                                                                                                                             # Not done with this function, thus not commenting with verboosity
        currentPos = int(event.widget.index(f"{tk.INSERT}").split(".")[0])
        currentText = event.widget.get(f"{currentPos-1}.{0}", f"{currentPos-1}.{tk.END}")
        currentDash = re.search('^\t*- |^\t*\u2022 ', currentText)
        currentNumeric = re.search('^\t*\d+\. ', currentText)
        if not currentDash and not currentNumeric:
            codeBlocks1 = re.search('^\t*\[.*', currentText)
            codeBlocks2 = re.search('^\t*\{.*', currentText)
            if codeBlocks1 or codeBlocks2:
                event.widget.insert(f"{tk.INSERT}", currentText.count("\t")*"\t"+" \t")
                return 'break'
            # Add in code when searching for ] or }
            return None

        if currentDash:
            event.widget.insert(f"{tk.INSERT}", currentText.count("\t")*"\t"+"- ")
            return 'break'

        if currentNumeric:
            num = int(currentText.replace("\n", "").split(".")[0]) + 1
            event.widget.insert(f"{tk.INSERT}", currentText.count("\t")*"\t"+str(num)+". ")

            # Defining a custom regex pattern that scales with the current line
            counted = currentText.count('\t')
            pattern = "^"
            for i in range(0, counted):
                pattern += '\t'
            pattern += "\d+\. "

            currentPos += 1
            nextNum = event.widget.get(f"{currentPos}.{0}", f"{currentPos}.{tk.END}")
            match = re.search(pattern, nextNum)
            while(match):
                replaceNum = int(nextNum.replace("\n", "").split(".")[0])
                if replaceNum-1 != num:
                    event.widget.delete(f"{currentPos}.{match.start()}",f"{currentPos}.{match.end()}")
                    event.widget.insert(f"{currentPos}.{match.start()}", counted*"\t"+str(num+1)+". ")
                currentPos += 1
                num += 1
                nextNum = event.widget.get(f"{currentPos}.{0}", f"{currentPos}.{tk.END}")
                match = re.search(pattern, nextNum)
            return 'break'

    def changeColor(self, pallet):                                                                                                                                                                              # Not done with this function, thus not commenting with verboosity
        pass
   
    def setColor(self, pallet):                                                                                                                                                                                 # This is to simply update all the colors used here, as
        """ A simple function to update all                                                                                                                                                                     # this will allow the user to freely change
        Those colors that I will be slowly adding here                                                                                                                                                          # any color without having to reset the app
        """                                                                                                                                                                                                     # Which can be neat.
        self.textColor = pallet[0]                                                                                                                                                                              # Foreground color
        self.background = pallet[1]                                                                                                                                                                             # Background Color
        self.strongColor = pallet[2]                                                                                                                                                                            # Bold/Header Color

    # Pass these as the commands                                                                                                                                                                                # I originally ran into a problem of having to update all 3 interfaces scrollbar
    def setScrollY(self, command):                                                                                                                                                                              # when only one was directly being affected by the user
        """ To set multiple widgets to be                                                                                                                                                                       # Then it came to me. Why not set a function to do all 3
        controlled by one scrollbar                                                                                                                                                                             # And thus I did
        """                                                                                                                                                                                                     # And it shows how python. Nothing is "private" because this should not be possible I think
        self.previewInterface.configure(yscrollcommand=command)                                                                                                                                                 # as a class I think should not be able to directly reference a class thats outside of scope
        self.markdownInterface.configure(yscrollcommand=command)                                                                                                                                                # or maybe I overthinked it
        self.rawInterface.configure(yscrollcommand=command)                                                                                                                                                     #
    
    def setScrollX(self):                                                                                                                                                                                       # Not done with this function, thus not commenting with verboosity
        pass
    
    # Pass these as the commands                                                                                                                                                                                # And whenever the scrollbar is running, it needs to send those inputs to a function
    def getScrollY(self, *args):                                                                                                                                                                                # Thus repeat from before and here we are.
        """ So anything the scrollbar is doing                                                                                                                                                                  #
        Can be relayed here to update the widgets                                                                                                                                                               #
        """                                                                                                                                                                                                     #
        self.previewInterface.yview(*args)                                                                                                                                                                      #
        self.markdownInterface.yview(*args)                                                                                                                                                                     #
        self.rawInterface.yview(*args)                                                                                                                                                                          #

    # Pass these as the commands                                                                                                                                                                                # I never use this, but its nice to have it as an option
    def getScrollX(self, *args):                                                                                                                                                                                #
        """ So anything the scrollbar is doing                                                                                                                                                                  #
        Can be relayed here to update the widgets                                                                                                                                                               #
        """                                                                                                                                                                                                     #
        self.previewInterface.xview(*args)                                                                                                                                                                      #
        self.markdownInterface.xview(*args)                                                                                                                                                                     #
        self.rawInterface(*args)                                                                                                                                                                                #

    def getText(self):                                                                                                                                                                                          # This is primarely used by word counter.
        """ A simple function that returns all                                                                                                                                                                  # And the reason why it uses rawInterface
        of the text stored inside                                                                                                                                                                               # is because the tricks I do to re-enact markdown should
        """                                                                                                                                                                                                     # not be counted as a word nor char. Otherwise
        return self.rawInterface.get('1.0', 'end')                                                                                                                                                              # this metric becomes misleading

if __name__ == "__main__":
    root = tk.Tk()
    testText = """#Heading 1
##Heading 2
###Heading 3
####Heading 4
#####Heading 5
######Heading 6

This is a *italic move* with a future **move**
This is a **bold** move with a reminder of *italic*
This is just ***both*** of *italic* and **bold**

Some nice blockquotes;
> Hey their
>> I am inside
>>> I am further
>>>>>>> Weee

That even works with all the above elements
>> ## Look at me!
>>> **I am spicy** little ***BOLD TEXT***

---

Just remember:
1. This is markdown
2. It can be quite easy to change
\t- You just mearly need some learning
\t- And probably remember the syntax
3. But once thats done, You can transform the hard to sort text to something more pretty.
(Maybe)
4. And keep scrolling
4. And keep seeing that it repeats?
4. Than simply press enter to make this fix itself
1. Yeah

---

Oh and we got `some fancy highlighting code text`, but don't worry if thats not your style.
I did bother to include this: ```
Which took a bit,
Someone pay me to include syntax highlighting

```

---

But does not blindly replace everything like # or *  in seperate lines
However it tries its best to not replace all characters. 
Like so: **#** : * as you can see.

My github: [Melody-Annotator](https://github.com/PhantomData87/Melody-Annotator "The thign you are using right now!") as one can see
Yet another github *[PhantomData87](https://github.com/PhantomData87)*
Or here as well **[Melody-Annotator][1] or here**
Or here as well ***[Melody-Annotator] [2] or their***

Original Link: <https://github.com/PhantomData87/Melody-Annotator>
[1]: https://github.com/PhantomData87/Melody-Annotator
[2]: https://github.com/PhantomData87/Melody-Annotator 'The thing you are using right now'

 - Markdown Editor -

""" 
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    mView = markdownView(root, testText, (0,0), (100, 10))
    button = tk.Button(root, command=lambda: mView.cycleView())
    button.grid(row=0, column=0)
    root.mainloop()