#statusBar 
from tkinter import *

#class statusbar for basic status bar
class StatusBar:
    def __init__(self, statusWindow):
        
        #mainframe which holds everything inside
        mainFrame = Frame(statusWindow, bg="red")
        mainFrame.pack(side="bottom", fill="x")

        #labeld and pseudo enties i.e labelEntries
        statusLabel = Label(mainFrame, text="Status : ", bg="red", fg="white")
        statusLabel.grid(row=0, column=0)

        statusEntyLabel = Label(mainFrame, text="", bg="red", fg="white")
        statusEntyLabel.grid(row=0, column=1)

if __name__ == "__main__":
    root = Tk()
    root.geometry("500x500")
    root.title("status bar")
    StatusBar(root)
    root.mainloop()