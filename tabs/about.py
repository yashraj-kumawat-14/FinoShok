from tkinter import *
from tkinter import messagebox as message

#this class is 'About' which has one 3 parameter one is title , information, menubar 
# It takes a Menu object and creates append command in that meny along with a function showmessage to display info

class About:
    def __init__(self, menubar, title="About", information="The software is under development"):
        #you can also the change content of showmessage dynamically

        self.aboutTitle = title
        self.aboutInformation = information
        menubar.add_command(label="About", command=self.showMessage)

    #function to show information.
    def showMessage(self):
        message.showinfo(self.aboutTitle, self.aboutInformation)
