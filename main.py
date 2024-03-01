#importing necessary modules
from tkinter import *
from tkinter import ttk
from login import Login
from tools.calculator import Calculator
from tools.notepad import Notepad
from tabs.addCustomer import AddCustomer
from tabs.addFile import AddFile
from config.colorConfig import MAINFRAMECOLOR, TOOLFRAMECOLOR, TABCOLOR, TOOLFRAMECOLOR, STATUSBARCOLOR

class Finoshok:
    def __init__(self, root):
        #making a menubar
        mainMenubar = Menu(root)
        mainMenubar.add_command(label="hello")

        #making submenubarss
        submenu = Menu(mainMenubar, tearoff=0)
        submenu.add_command(label="Add Customer", command=self.addCustomer)
        self.aCustomerCount = 0 #making it so that user can create multiple add customer tabs

        submenu.add_checkbutton(label="rajj")
        submenu.add_command(label="Add new file", command=self.addFile)
        self.aFileCount = 0 #making it so that user can create multiple add new file tabs

        #adding submenu in mainmenybar
        mainMenubar.add_cascade(menu=submenu, label="File")

        #configuring the menu in root as mainmenubar
        root.config(menu=mainMenubar)

        #creating toolFrame in root

        toolFrame = Frame(root, bg=TOOLFRAMECOLOR)
        toolFrame.pack(side="left", fill="y")

        noteFrame = Frame(toolFrame, bg=TOOLFRAMECOLOR, borderwidth=2, relief="groove")
        noteFrame.pack(side="top", fill="both", expand=True)

        calculatorFrame = Frame(toolFrame, bg=TOOLFRAMECOLOR, borderwidth=2, relief="groove")
        calculatorFrame.pack(side="bottom")
        

        #binding widgets to keyBoardHandler for key event
        calc = Calculator(calculatorFrame)
        root.bind("<Key>", calc.keyBoardHandler)
        for child in root.winfo_children():
            child.bind("<Key>", calc.keyBoardHandler)

        #create mini notepad
        notepad = Notepad(noteFrame, 200, 200)

        #CREATING main frame in root

        mainFrame = Frame(root, bg=MAINFRAMECOLOR)
        mainFrame.pack(fill="both", expand=True)

        #creating a notebook of tabs in mainframe

        self.myNotebook = ttk.Notebook(mainFrame)
        self.myNotebook.pack(fill="both", expand=True)

        #making a dictionary to hold tabs by their names so that we can manipulate and navigate to tabs without any confustion later
        self.tabsDictionary = {}

        #creating a status bar
        statusBar = Frame(root, bg=STATUSBARCOLOR)
        statusBar.pack(side="bottom", fill="x")

    #method or function to add tabs in myNotebook, it takes one parameter tabName which has store tab's name
    def addTab(self, tabName):
        #check if the tab is already present in tabsDictionary so that we do not create the same tab again
        if(tabName not in self.tabsDictionary.keys()):
            #tabframe to hold contents of the tab
            tabFrame = Frame(self.myNotebook, bg=TABCOLOR)
            tabFrame.pack(fill="both", expand=True)

            #appending tab in the dictionary with their tab names
            self.tabsDictionary[tabName]=tabFrame

            #now adding the frame as a tab in myNotebook
            self.myNotebook.add(tabFrame, text=tabName)
            return True
        else:
            #return false if tab already exists
            return False
    
    #this adds a customer tab in the notebook
    def addCustomer(self):
        #it calls addtab function to add tab named Add Customer + count
        self.addTab("Add Customer"+f" {self.aCustomerCount}")

        #now we update the self.tabsDictionary to keep track of tabs
        AddCustomer(self.tabsDictionary["Add Customer"+f" {self.aCustomerCount}"])
        self.aCustomerCount+=1 #here now we increment corresponding count

    #this adds a new file tab in notebook
    def addFile(self):
        #it calls addtab function to add tab named Add File + count
        self.addTab("Add File"+f" {self.aFileCount}")

        #now we update the self.tabsDictionary to keep track of tabs
        AddFile(self.tabsDictionary["Add File"+f" {self.aFileCount}"])
        self.aFileCount+=1 #here now we increment the corresponding count


if __name__=="__main__":
    #login window 
    login_window = Tk()
    login_window.title("Login")
    login_window.geometry("200x200")
    login_window.resizable(False, False)
    
    #passing login_window to login class to make working login window
    Login(login_window)
    login_window.mainloop()

    # checking if the credentials are correct
    if(login_window.result):
        #initiating the gui
        root = Tk()
        root.geometry("400x400")
        root.title("finoshok")
        Finoshok(root)

        root.mainloop()