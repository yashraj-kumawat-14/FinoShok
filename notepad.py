from tkinter import *

class Notepad:
    def __init__(self, noteWindow, fixedWidth=700, fixedHeight=400, wrap=True):
        mainFrame = Frame(noteWindow, bg="grey", width=fixedWidth, height=fixedHeight)
        mainFrame.pack(fill="both", expand=True)
        mainFrame.pack_propagate(0)

        yScrollBar = Scrollbar(mainFrame)
        yScrollBar.pack(side="right", fill="y")

        note = Text(mainFrame)
        note.pack(fill="both", expand=True)

        yScrollBar.config(command=note.yview)
        note.config(yscrollcommand=yScrollBar.set)

        try:
            if(not wrap):
                xScrollBar = Scrollbar(mainFrame, orient="horizontal")
                xScrollBar.pack(side="bottom", fill="x")

                xScrollBar.config(command=note.xview)
                note.config(xscrollcommand=xScrollBar.set, wrap="none")
        except:
            pass
        
        
if __name__ == "__main__":      
    root = Tk()
    root.geometry("499x499")
    Notepad(root, wrap=False)
    root.mainloop()