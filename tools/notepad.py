from tkinter import *


#here is a Notepad class which can be used to make a simple notepad to open save and write text files
# it takes parameter as Tk window or Fram, fixedWidhth, fixedHeight

class Notepad:
    def __init__(self, noteWindow, fixedWidth=700, fixedHeight=400, wrap=True):

        #here is the mainframe which is spread fully  into the notewindow. it contains everything of notepad object

        mainFrame = Frame(noteWindow, bg="grey", width=fixedWidth, height=fixedHeight)
        mainFrame.pack(fill="both", expand=True)
        mainFrame.pack_propagate(0)

        #here is yscrollbar widget which controls the scrolling in y direction
        yScrollBar = Scrollbar(mainFrame)
        yScrollBar.pack(side="right", fill="y")

        #here is used Text widget of tkinter to allow user write on the window
        note = Text(mainFrame)
        note.pack(fill="both", expand=True)

        #configuring commnad of yScrollbar widget as note.yview which will provide functionality scoll up and down
        yScrollBar.config(command=note.yview)
        #here note is configured to have yscollcommand parameter to the yScrollbar.set
        note.config(yscrollcommand=yScrollBar.set)

        #check if wrap is False then make xscrollbar to scroll in x direction
        if(not wrap):
            #here is defined the scrollbar for x direction xScrollbar
            xScrollBar = Scrollbar(mainFrame, orient="horizontal")#orient is set to horizontal. default value is vertical we overwrite it 
            xScrollBar.pack(side="bottom", fill="x")

            #configuring command of xScrollbar to control note.xview for controlling the x direction scrolling  
            xScrollBar.config(command=note.xview)

            #configuring note's xcrollcommand to xScrollbar.set, and wrap to none so the words do not get wrapped.
            note.config(xscrollcommand=xScrollBar.set, wrap="none")
        
        
if __name__ == "__main__":      
    root = Tk()
    root.geometry("499x499")
    Notepad(root, wrap=False)
    root.mainloop()