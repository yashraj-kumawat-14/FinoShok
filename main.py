#importing necessary modules
from tkinter import *
from tkinter import ttk
#colors used in gui
mainFrameColor = "grey"
statusBarColor = "red"
toolFrameColor = "green"

#initiating the gui
root = Tk()
root.geometry("400x400")
root.title("finoshok")

#making a menubar
mainMenubar = Menu(root)
mainMenubar.add_command(label="hello")
#making submenubarss
submenu = Menu(mainMenubar, tearoff=0)
submenu.add_command(label="raj")
submenu.add_checkbutton(label="rajj")

#adding submenu in mainmenybar
mainMenubar.add_cascade(menu=submenu, label="gile")

#configuring the menu in root as mainmenubar
root.config(menu=mainMenubar)

#creating toolFrame in root

toolFrame = Frame(root, bg=toolFrameColor)
toolFrame.pack(side="left", fill="y")

#CREATING main frame in root

mainFrame = Frame(root, bg=mainFrameColor)
mainFrame.pack(fill="both", expand=True)

#creating a notebook of tabs in mainframe

my_notebook = ttk.Notebook(mainFrame)
my_notebook.pack(fill="both", expand=True)

#creating tabs in notebook

tab1 = Frame(my_notebook, bg=mainFrameColor)
tab2 = Frame(my_notebook, bg=toolFrameColor)
tab1.pack(fill="both", expand=True)
tab2.pack(fill="both", expand=True)

my_notebook.add(tab1, text="yashraj")
my_notebook.add(tab2, text="kumawat")

#navigation buttons for tabs
def hide():
    my_notebook.hide(1)
def show():
    my_notebook.add(tab2, text="kumawat")
def select():
    my_notebook.select(1)
hideButton = Button(tab1, text="hide tab 2", command=hide)
hideButton.pack()

showButton = Button(tab1, text="show tab 2", command=show)
showButton.pack()

selectButton = Button(tab1, text="select tab 2", command=select)
selectButton.pack()

#creating a status bar
statusBar = Frame(root, bg=statusBarColor)
statusBar.pack(side="bottom", fill="x")

root.mainloop()