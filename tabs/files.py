#importing necessary modules and components and clases
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from sys import path

path.append(r"D:\projects\finoshok\finoshok\model")

from File import File
from Ledger import Ledger
import tkinter.messagebox as message

class Files:
    def __init__(self, parentWindow):
        #create mainframe containing everything
        self.mainFrame = Frame(master=parentWindow)
        self.mainFrame.pack(fill="both", expand=True)

        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.columnconfigure(1, weight=1)
        self.mainFrame.columnconfigure(2, weight=1)

        self.subFrame1 = Frame(master=self.mainFrame, border=2, relief="groove", width=100, height=100)
        self.subFrame1.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.subFrame1.grid_propagate(False)
        self.subFrame1.pack_propagate(False)

        self.subFrame2 = Frame(master=self.mainFrame, border=2, relief="groove", width=50, height=100)
        self.subFrame2.grid(row=0, column=2, sticky="nsew")
        self.subFrame2.grid_propagate(False)
        self.subFrame2.pack_propagate(False)

        #work under subframe1 start here

if __name__=="__main__":
    root = Tk()
    root.title("Files List ")
    root.geometry("1000x700")
    files = Files(root)
    root.mainloop()