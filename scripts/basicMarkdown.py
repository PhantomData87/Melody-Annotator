from tkinter import Text as T
import webbrowser as wb
import tkinter as tk
import re



class markdownView():                                                                                                                                                                                           # Welcome to more verboose comments. Again run the function found in melodyCore.py to remove them
    def __init__(self, root, startText, pad, location, colorPallet = ("#AAAAAA", "#272738", "#DDDDDD")):                                                                                                        # We only want to take in the bare minimum.
        self.setColor(colorPallet)                                                                                                                                                                              # Thus we mearly take in a set of colors
        self.displayFontName = 'Calibri'                                                                                                                                                                        # A font
        self.current = "r"                                                                                                                                                                                      # A variable to help us simplify the code
        self.nSize = 10                                                                                                                                                                                         # Size of the normal text
        self.root = root                                                                                                                                                                                        # And where melodyCore is at
                                                                                                                                                                                                                #
        self.markdownInterface = T(root, background = self.background, foreground = self.textColor, highlightthickness = 0, borderwidth = 0, wrap = tk.WORD, padx = pad[0], pady = pad[1], relief=tk.FLAT)      # Here we display markdown, however we remove symbols
        self.previewInterface = T(root, background = self.background, foreground = self.textColor, highlightthickness = 0, borderwidth = 0, wrap = tk.WORD, padx = pad[0], pady = pad[1], relief=tk.FLAT)       # This interface is meant to be a hybrid of rawInterface and markdownInterface. Symbols are kept here
        self.rawInterface = T(root, background = self.background, foreground = self.textColor, highlightthickness = 0, borderwidth = 0, wrap = tk.WORD, padx = pad[0], pady = pad[1], relief=tk.FLAT)           # Nothing fancy will happen here, and symbols are not removed
                                                                                                                                                                                                                #
        self.previewInterface.insert("1.0", startText)                                                                                                                                                          # In case we need to load a file, or for testing purposes
                                                                                                                                                                                                                #
        self.markdownInterface.grid(row=location[0], column=location[1], sticky='nswe')                                                                                                                         # Initializing on frame
        self.markdownInterface.bindtags(self.markdownInterface.bindtags() + ("basicMarkdown",))                                                                                                                 # Adding a custom tag so we can bind_class it
        self.markdownInterface['state'] = tk.DISABLED                                                                                                                                                           # Ensuring the user cannot edit the interface
        self.previewInterface.grid(row=location[0], column=location[1], sticky='nswe')                                                                                                                          # Initializing on frame
        self.previewInterface.bindtags(self.previewInterface.bindtags() + ("basicMarkdown",))                                                                                                                   # Adding a custom tag so we can bind_class it
        self.rawInterface.grid(row=location[0], column=location[1], sticky='nswe')                                                                                                                              # Initializing on frame
        self.rawInterface.bindtags(self.rawInterface.bindtags() + ("basicMarkdown",))                                                                                                                           # Adding a custom tag so we can bind_class it
        self.rawInterface.tkraise()                                                                                                                                                                             # Making this the frame to appear
        self.rawInterface.focus_set()                                                                                                                                                                           # Setting the focus so tkinter knows which to respond first
                                                                                                                                                                                                                #
        self.markdownRules = [                                                                                                                                                                                  # Here we are defining a variety of Markdown's variosu rules. All of basic syntax is supported, as defined here. (https://www.markdownguide.org/basic-syntax/)
            ['```','Fenced Code Block',(f'{self.displayFontName} {self.nSize}', "#CC0000"),("Multiline", "```", "#333333")],                                                                                    # The only advanced syntax implemented so far, oh and this list follows a hierarchy
            ['^\[\d+\]: .+','Hyperlink Site', (f'{self.displayFontName} {self.nSize}', "#0000FF"), ('DetectUrl', "")],                                                                                          # This is used to reference the rest of the Hyperlinks
            ['\*\*\*\[.+\] ?\([^""]+.*\)\*\*\*','Hyperlink Italic Bold', (f'{self.displayFontName} {self.nSize} bold italic', "#0000FF"), ('Url', "***", 'Hyperlink Italic Bold', "#0000FF")],                  # Making sure you can Italic bold a hyperlink
            ['\*\*\*\[.+\] ?\[\d+\]\*\*\*','Hyperlink Italic Bold', (f'{self.displayFontName} {self.nSize} bold italic', "#0000FF"), ('Url', "***", 'Hyperlink Italic Bold', "#0000FF")],                       # Making sure you can bold a hyperlink
            ['\*\*\[.+\] ?\([^""]+.*\)\*\*','Hyperlink Bold', (f'{self.displayFontName} {self.nSize} bold', "#0000FF"), ('Url', "**", 'Hyperlink Bold', "#0000FF")],                                            # Making sure you can Italic a hyperlink
            ['\*\*\[.+\] ?\[\d+\]\*\*','Hyperlink Bold', (f'{self.displayFontName} {self.nSize} bold', "#0000FF"), ('Url', "**", 'Hyperlink Bold', "#0000FF")],                                                 # Making sure you can Italic bold a hyperlink
            ['\*\[.+\] ?\([^""]+.*\)\*','Hyperlink Italic', (f'{self.displayFontName} {self.nSize} italic', "#0000FF"), ('Url', "*", 'Hyperlink Italic', "#0000FF")],                                           # Making sure you can bold a hyperlink
            ['\*\[.+\] ?\[\d+\]\*','Hyperlink Italic', (f'{self.displayFontName} {self.nSize} italic', "#0000FF"), ('Url', "*", 'Hyperlink Italic', "#0000FF")],                                                # Making sure you can Italic a hyperlink
            ['\[.+\] ?\([^""]+.*\)','Hyperlink', (f'{self.displayFontName} {self.nSize}', "#0000FF"), ('Url', "", 'Hyperlink', "#0000FF")],                                                                     # Ye regular hyperlink in one style
            ['\[.+\] ?\[\d+\]','Hyperlink', (f'{self.displayFontName} {self.nSize}', "#0000FF"), ('Url', "", "Hyperlink", "#0000FF")],                                                                          # Another style for hyperlinks, but this uses indexes
            ['<.*(@.)*.>', 'Quick Hyperlink', (f'{self.displayFontName} {self.nSize}', "#0000FF"), ('Quick Url', "", "QuickLink")],                                                                             # A quick version to add a hyperlink
            ['^######[\S\s]+?$','Header 6',(f'{self.displayFontName} {self.nSize}', self.strongColor),("Left", "######")],                                                                                      # Adding the smallest header
            ['^#####[\S\s]+?$','Header 5',(f'{self.displayFontName} {15}', self.strongColor),("Left", "#####")],                                                                                                # Adding a bigger header
            ['^####[\S\s]+?$','Header 4',(f'{self.displayFontName} {20}', self.strongColor),("Left", "####")],                                                                                                  # Adding a bigger header
            ['^###[\S\s]+?$','Header 3',(f'{self.displayFontName} {25}', self.strongColor),("Left", "###")],                                                                                                    # Adding a bigger header
            ['^##[\S\s]+?$','Header 2',(f'{self.displayFontName} {30}', self.strongColor),("Left", "##")],                                                                                                      # Adding a bigger header
            ['^#[\S\s]+?$','Header 1',(f'{self.displayFontName} {40}', self.strongColor),("Left", "#")],                                                                                                        # Adding the biggest header
            ['\*\*\*.+?\*\*\*','Italic & Bold',(f'{self.displayFontName} {self.nSize} bold italic', self.strongColor),("Both", "***")],                                                                         # Adding bold italic to text
            ['\*\*.+?\*\*','Bold',(f'{self.displayFontName} {self.nSize} bold', self.strongColor),("Both", "**")],                                                                                              # Adding bold to text
            ['\*.+?\*','Italic',(f'{self.displayFontName} {self.nSize} italic', self.strongColor),("Both", "*")],                                                                                               # Adding italic to text
            ['`.+?`','Code Phrase',(f'{self.displayFontName} {self.nSize}', "#CC0000"),("Both Colored", "`", "#333333")],                                                                                       # Adding a Code Sentance
            ['^>+ ######[\S\s]+?$','Blockquote Header 6',(f'{self.displayFontName} {self.nSize}', self.strongColor),("Blocks", "> ######", ("#0000FF", "  ", "#333333"))],                                      # Adding the smallest header for blockquotes
            ['^>+ #####[\S\s]+?$','Blockquote Header 5',(f'{self.displayFontName} {15}', self.strongColor),("Blocks", "> #####", ("#0000FF", "  ", "#333333"))],                                                # Adding a bigger header for blockquotes
            ['^>+ ####[\S\s]+?$','Blockquote Header 4',(f'{self.displayFontName} {20}', self.strongColor),("Blocks", "> ####", ("#0000FF", "  ", "#333333"))],                                                  # Adding a bigger header for blockquotes
            ['^>+ ###[\S\s]+?$','Blockquote Header 3',(f'{self.displayFontName} {25}', self.strongColor),("Blocks", "> ###", ("#0000FF", "  ", "#333333"))],                                                    # Adding a bigger header for blockquotes
            ['^>+ ##[\S\s]+?$','Blockquote Header 2',(f'{self.displayFontName} {30}', self.strongColor),("Blocks", "> ##", ("#0000FF", "  ", "#333333"))],                                                      # Adding a bigger header for blockquotes
            ['^>+ #[\S\s]+?$','Blockquote Header 1',(f'{self.displayFontName} {40}', self.strongColor),("Blocks", "> #", ("#0000FF", "  ", "#333333"))],                                                        # Adding the biggest header for blockquotes
            ['^>+ [\S\s]*?$','Blockquote',(f'{self.displayFontName} {self.nSize}', self.strongColor),("Blocks", ">", ("#0000FF", "  ", "#333333"))],                                                            # Adding a regular blockquote
            ['^\t*\d+\. ','Sorted List',(f'{self.displayFontName} {self.nSize}', "#777777"),("Indent", "")],                                                                                                    # You can make a list with numbers
            ['^\t*\- ','Unsorted List',(f'{self.displayFontName} {self.nSize}', "#777777"),("Indent", "")],                                                                                                     # You can make a list without numbers
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
    
    def cycleView(self):                                                                                                                                                                                        # This is ran change the type of interface you see when you press the button
        if self.current == "r":                                                                                                                                                                                 # This is allow all edits done on a document to be updated when you press the button again.
            text = self.rawInterface.get(1.0, tk.END)[:-1]                                                                                                                                                      # This is done so backspaces and mass erasure can be registered on the other interfaces
            self.rawInterface.delete(1.0, tk.END)                                                                                                                                                               # Deleting a problematic newline
            self.previewInterface.insert(1.0, text)                                                                                                                                                             #
            self.previewInterface.tkraise()                                                                                                                                                                     # 
            self.current = "p"                                                                                                                                                                                  # 
        elif self.current == "p":                                                                                                                                                                               # 
            self.markdownInterface.tkraise()                                                                                                                                                                    # 
            self.current = "m"                                                                                                                                                                                  # 
        elif self.current == "m":                                                                                                                                                                               # 
            text = self.previewInterface.get(1.0, tk.END)[:-1]                                                                                                                                                  # Deleting a problematic newline                                                                                                                                              #
            self.previewInterface.delete(1.0, tk.END)                                                                                                                                                           #
            self.rawInterface.insert(1.0, text)                                                                                                                                                                 #
            self.rawInterface.tkraise()                                                                                                                                                                         # 
            self.current = "r"                                                                                                                                                                                  #
        self.markdownDetect()                                                                                                                                                                                   # Make sure markdown is being updated

    def dupeText(self, event, realChar = None):                                                                                                                                                                 # This will act as updateText() but it has the nice feature of adding more text
        if realChar:                                                                                                                                                                                            # To prevent an error when am adding in more custom text
            choosenChar = realChar                                                                                                                                                                              # For simplicity
        else:                                                                                                                                                                                                   #
            choosenChar = event.char                                                                                                                                                                            # For simplicity                                                                                                                                                                                                        #
                                                                                                                                                                                                                #
        if self.current == "m":                                                                                                                                                                                 # To prevent the markdown interface from changing anything
            return 'break'                                                                                                                                                                                      # To prevent the markdown interface from changing anything
        elif self.current == "r":                                                                                                                                                                               #
            self.rawInterface.insert(tk.INSERT, choosenChar)                                                                                                                                                    # Than add new char to rawInterface
            self.rawInterface.mark_set("insert", "insert-1c")                                                                                                                                                   # To make sure the text cursor is inside the brackets
        elif self.current == "p":                                                                                                                                                                               #
            self.rawInterface.insert(tk.INSERT, choosenChar)                                                                                                                                                    # Than add new char to rawInterface
            self.previewInterface.mark_set("insert", "insert-1c")                                                                                                                                               # To make sure the text cursor is inside the brackets
        self.markdownDetect()                                                                                                                                                                                   # Check if new markdown is detected                                                                                                                                                                                           # End the event

    def markdownDetect(self, event=None):                                                                                                                                                                       # The core function & reason why this is a class
        if self.current == "r":                                                                                                                                                                                 #
            return None                                                                                                                                                                                         # Not wanting to run this unless markdown is needed
                                                                                                                                                                                                                #     
        self.markdownInterface['state'] = tk.NORMAL                                                                                                                                                             # This function was originally based on a guide to add markdown (no imports) and they simply deleted all text from one interface
                                                                                                                                                                                                                # Eventually this will change
        # Clear the Display Area                                                                                                                                                                                #
        self.markdownInterface.delete(1.0, tk.END)                                                                                                                                                              #
                                                                                                                                                                                                                #
        # To remove any of the blockquotes in markdown from the previous scan                                                                                                                                   # This is made for blockquotes as they linger in previewInterface if one does not delete them manually
        allBlockTags = self.previewInterface.tag_ranges("indentBlock")                                                                                                                                          # after removing the blockquote char
        for i in reversed(range(0, len(self.previewInterface.tag_ranges("indentBlock")), 2)):                                                                                                                   # For all tags left with "indentBlock"
            splitText = str(allBlockTags[i+1]).split(".")                                                                                                                                                       # Find where the original text is at
            self.previewInterface.delete(str(allBlockTags[i]), f"{splitText[0]}.{str(int(str(splitText[1]))+1)}")                                                                                               # Delete the spaces
        self.previewInterface.tag_delete("indentBlock")                                                                                                                                                         # Ones that is done just delete the tag
                                                                                                                                                                                                                #
        # Obtaining text and saving them seperately per editor                                                                                                                                                  # Making a copy of the text
        semiOriginalText = self.previewInterface.get('1.0', tk.END)                                                                                                                                             #
                                                                                                                                                                                                                #
        # So updates can happen on the screen                                                                                                                                                                   # We have to insert the text early into the markdownInterface or otherwise the tags will not stick
        self.markdownInterface.insert(1.0, semiOriginalText)                                                                                                                                                    # And that would nullify the rest of the function.
                                                                                                                                                                                                                #
        # Loop through each replacement, unpacking it fully                                                                                                                                                     #
        for pattern, name, fontData, removalData in self.markdownRules:                                                                                                                                         #This loop will look at all the markdownRules defined above
            # Removing previous tags                                                                                                                                                                            # Not sure if needed
            self.markdownInterface.tag_delete(name)                                                                                                                                                             # Not sure if needed
            self.previewInterface.tag_delete(name)                                                                                                                                                              # Not sure if needed
                                                                                                                                                                                                                #
            # Get the location indices of the given pattern                                                                                                                                                     #
            locationsLive = self.search_re(pattern, semiOriginalText, removalData)                                                                                                                              #
                                                                                                                                                                                                                #
            # Add tags where the search_re function found the pattern                                                                                                                                           # Activating our first helper function to define where the markdown syntax is located.
            for start, end in locationsLive:                                                                                                                                                                    #
                self.previewInterface.tag_add(name, start, end)                                                                                                                                                 # Using the markdown syntax name as the naem of the tag
                self.markdownInterface.tag_add(name, start, end)                                                                                                                                                #
                self.previewInterface.tag_lower(name)                                                                                                                                                           # The reason we call in "tag_lower" is to prevent multiple cases in the same area to
                self.markdownInterface.tag_lower(name)                                                                                                                                                          # nullify one of the more important syntax. Like fenced code blocks has nothing but itself inside
                                                                                                                                                                                                                #
            # Configure the tag to use the specified font and color                                                                                                                                             # How markdown demands fonts, color, background, foreground, styles, size, and etc.
            # to this every time to delete the previous tags                                                                                                                                                    # Requires all of these different categories to act a little diffrently.
            if removalData[0] == "Left" or removalData[0] == "Both":                                                                                                                                            # However not all categories are defined here
                self.markdownInterface.tag_config(name, font=fontData[0], foreground=fontData[1])                                                                                                               # Either from lazyness or because it was defined elsewhere
                self.previewInterface.tag_config(name, font=fontData[0], foreground=fontData[1])                                                                                                                #
            elif removalData[0] == "Both Colored" or removalData[0] == "Multiline":                                                                                                                             #
                self.markdownInterface.tag_config(name, font=fontData[0], foreground=fontData[1], background=removalData[2])                                                                                    #
                self.previewInterface.tag_config(name, font=fontData[0], foreground=fontData[1], background=removalData[2])                                                                                     #
            elif removalData[0] == "Blocks":                                                                                                                                                                    #
                self.markdownInterface.tag_config(name, font=fontData[0], foreground=fontData[1], background = removalData[2][2])                                                                               #
                self.previewInterface.tag_config(name, font=fontData[0], foreground=fontData[1], background = removalData[2][2])                                                                                #
            elif removalData[0] == "Indent":                                                                                                                                                                    #
                self.markdownInterface.tag_config(name, font=fontData[0], foreground=fontData[1])                                                                                                               #
                self.previewInterface.tag_config(name, font=fontData[0], foreground=fontData[1])                                                                                                                #
            elif removalData[0] == "Url" or removalData[0] == "Quick Url":                                                                                                                                      #
                self.markdownInterface.tag_config(name, font=fontData[0], foreground=fontData[1], underline=True)                                                                                               #
                self.previewInterface.tag_config(name, font=fontData[0], foreground=fontData[1], underline=True)                                                                                                #
                                                                                                                                                                                                                #
        # Removinng unwanted text                                                                                                                                                                               # This will look at all the markdown syntax AFTER the tags are defined
        for pattern, name, ignored, removalData in self.markdownRules:                                                                                                                                          # to safely remove all extra characters for markdownInterface via our second helper function
            self.editText(pattern, removalData)                                                                                                                                                                 #
                                                                                                                                                                                                                #
        self.markdownInterface['state'] = tk.DISABLED                                                                                                                                                           # Disables the interface again.

    def search_re(self, pattern, text, removalData):                                                                                                                                                            # Not done with this function, thus not commenting with verboosity
        foundHere = []
        multiPosition, offset = -1, 0
        prevLine = ""
        for i, line in enumerate(text.splitlines(), 1):
            for found in re.finditer(pattern, line):
                if removalData[0] == "Multiline":
                    if multiPosition == -1:
                        multiPosition = i 
                        offset = found.start()
                        foundHere.append((f"{multiPosition}.{offset}", "end"))
                        continue
                    foundHere.pop(-1)
                    difference = i - multiPosition + 1
                    foundHere.append((f"{multiPosition}.{offset}", f"{multiPosition}.{offset}+{difference}lines"))
                    multiPosition = -1
                elif removalData[0] == "Blocks" or pattern == "^---$":
                    foundHere.append((f"{i}.{found.start()}", f"{i}.{found.start()}+1lines"))
                elif removalData[0] == "Url":
                    filler = found.group(0).split("]")[0][1:]
                    foundHere.append((f"{i}.{found.start()}", f"{i}.{found.start() + len(filler)}"))
                else:
                    foundHere.append((f"{i}.{found.start()}", f"{i}.{found.end()}"))
            prevLine = line
        return foundHere

    def editText(self, pattern, removalData):                                                                                                                                                                   # Not done with this function, thus not commenting with verboosity
        text = self.markdownInterface.get('1.0', "end")
        prevLine = ""
        for i, line in enumerate(text.splitlines(), 1):
            while re.search(pattern, line) != None:
                found = re.search(pattern, line)
                if removalData[0] == "Left":
                    self.markdownInterface.delete(f"{i}.{found.start()}", f"{i}.{found.start() + len(removalData[1])}")
                    line = line.replace(removalData[1], "", 1)
                elif removalData[0] == "Both" or removalData[0] == "Both Colored":
                    self.markdownInterface.delete(f"{i}.{found.end() - len(removalData[1])}", f"{i}.{found.end()}")
                    self.markdownInterface.delete(f"{i}.{found.start()}", f"{i}.{found.start() + len(removalData[1])}")
                    line = line.replace(removalData[1], "", 2)
                elif removalData[0] == "Blocks":
                    self.previewInterface.insert(f"{i}.{0}", removalData[2][1])
                    self.markdownInterface.insert(f"{i}.{0}", removalData[2][1]+" ")

                    if re.search(f">", self.markdownInterface.get(f"{i}.0",f"{i+1}.0")) != None:            # Alternative; get("1.0",f"1.{a.count(1.0, 2.0)[0]}")
                        foundChar = re.search(f">", self.markdownInterface.get(f"{i}.0",f"{i+1}.0"))  # Removing '>'
                        foundExtraChar = re.search(f"#+", self.markdownInterface.get(f"{i}.0",f"{i+1}.0")) # Removing '#'

                        if foundExtraChar != None:
                            self.markdownInterface.delete(f"{i}.{foundExtraChar.start()}", f"{i}.{foundExtraChar.end()}") # Removing all '#' in one swift move
                        self.markdownInterface.delete(f"{i}.{foundChar.start()}")

                    line = line.replace(">", "", 1)

                    self.previewInterface.tag_add("indentBlock", f"{i}.{0}", f"{i}.{1}")
                    self.markdownInterface.tag_add("indentBlock", f"{i}.{0}", f"{i}.{1}")

                    self.previewInterface.tag_config("indentBlock", background = removalData[2][0])
                    self.markdownInterface.tag_config("indentBlock", background = removalData[2][0])

                    self.previewInterface.tag_lower("indentBlock")
                    self.markdownInterface.tag_lower("indentBlock")

                elif removalData[0] == "Multiline":
                    self.markdownInterface.delete(f"{i}.{found.start()}", f"{i}.{found.start() + len(removalData[1])}")
                    line = line.replace(removalData[1], "", 1)
                    continue

                elif removalData[0] == "Url":
                    filler = found.group(0).split("]")[0][1:]
                    if "(" in found.group(0):
                        location = found.group(0).split("(")[1]
                        ulrSearcher = re.search('^<?.+>? [\"\'\(\)]|^<?.+>?', location)
                        if not ulrSearcher:
                            break

                        url = ulrSearcher.group(0)
                        urlHeading = re.search('[\"\'\(\)].+[\"\'\(\)]', location)

                        if not urlHeading:
                            optionalHeading = ""
                        else:
                            url = url[:-2]
                            optionalHeading = urlHeading.group(0)[1:-1]
                    elif "]" in found.group(0).replace(" ", "").split("][")[1]:
                        location = found.group(0).replace(" ", "", 1).split("][")[1].replace("]","").replace("*","")
                        url = self.urlLocations[location][0]
                        optionalHeading = self.urlLocations[location][1]

                    self.markdownInterface.delete(f"{i}.{found.start()}", f"{i}.{found.end()}")                
                    self.markdownInterface.insert(f"{i}.{found.start()}", filler[len(removalData[1]):])

                    line = line.replace(found.group(0), "")

                    self.previewInterface.tag_add(removalData[2], f"{i}.{found.start()}", f"{i}.{found.start() + len(filler) + 2}")
                    self.markdownInterface.tag_add(removalData[2], f"{i}.{found.start()}", f"{i}.{found.start() + len(filler)}")

                    # For later https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
                    self.previewInterface.tag_bind(removalData[2], "<Button-1>", lambda event: wb.open(url))
                    self.markdownInterface.tag_bind(removalData[2], "<Button-1>", lambda event: wb.open(url))

                    self.previewInterface.tag_lower(removalData[2])
                    self.markdownInterface.tag_lower(removalData[2])

                elif removalData[0] == "Quick Url":
                    url = found.group(0).split(">")[0][1:]
                    self.markdownInterface.delete(f"{i}.{found.end()}")
                    self.markdownInterface.delete(f"{i}.{found.start()}")

                    line = line.replace(found.group(0), "")

                    self.previewInterface.tag_add(removalData[2], f"{i}.{found.start()}", f"{i}.{found.end() - 1}")
                    self.markdownInterface.tag_add(removalData[2], f"{i}.{found.start()}", f"{i}.{found.end() - 1}")

                    # For later https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
                    self.previewInterface.tag_bind(removalData[2], "<Button-1>", lambda event: wb.open(url))
                    self.markdownInterface.tag_bind(removalData[2], "<Button-1>", lambda event: wb.open(url))

                elif removalData[0] == "DetectUrl":
                    filler = found.group(0).split("]")[0][1:].replace("*","")
                    location = found.group(0).split("]")[1][2:]
                    ulrSearcher = re.search('^<?.+>? [\"\'\(\)]|^<?.+>?', location)
                    if not ulrSearcher:
                        break

                    url = ulrSearcher.group(0)
                    urlHeading = re.search('[\"\'\(\)].+[\"\'\(\)]', location)

                    if not urlHeading:
                        optionalHeading = ""
                    else:
                        url = url[:-2]
                        optionalHeading = urlHeading.group(0)[1:-1]

                    self.urlLocations[filler] = (url, optionalHeading)

                    self.markdownInterface.delete(f"{i}.{found.start()}", f"{i}.{found.end()}")

                    line = ""

                elif removalData[0] == "Indent":
                    break
            prevLine = line

    def logicalIndent(self, event):                                                                                                                                                                             # Not done with this function, thus not commenting with verboosity
        currentPos = int(event.widget.index(f"{tk.INSERT}").split(".")[0])
        currentText = event.widget.get(f"{currentPos-1}.{0}", f"{currentPos-1}.{tk.END}")
        currentDash = re.search('^\t*- ', currentText)
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
   
    def setScrollX(self):                                                                                                                                                                                       # Not done with this function, thus not commenting with verboosity
        pass

    def setScrollY(Self):                                                                                                                                                                                       # Not done with this function, thus not commenting with verboosity
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

This is a *italic move*
This is a **bold** move
This is just ***both***

Some nice blockquotes;
> Hey their
>> I am inside
>>> I am further
>>>>>>> Weee

That even works with all the above elements
>> ## Look at me!
>>> **I am spicy**

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
However it will replace them when used in the same line. 
Like so: **#**  : * as you can see.

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