from tkinter import *

#here is the class HelpMenu which takes one parameter menybar and create menu items and submenu items in it accordingley

class HelpMenu:
    def __init__(self, menubar):
        #creating submeny
        self.helpMenu = Menu(menubar, tearoff=False)
        
        #creating menu items in submenu
        self.helpMenu.add_command(label="Documentaion")
        self.helpMenu.add_command(label="Tutorial And Guide")
        self.helpMenu.add_command(label="FAQ's")
        self.helpMenu.add_command(label="Online Help & Support")
        
        #registering the submenu in menubar
        menubar.add_cascade(menu=self.helpMenu, label="Help")

if __name__ == "__main__":
    root = Tk()
    root.title("Help window")
    root.geometry("500x400")
    menubar = Menu(root)
    HelpMenu(menubar)
    root.config(menu=menubar)
    root.mainloop()