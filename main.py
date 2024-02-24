#importing necessary modules
from tkinter import Tk, Frame, Label, Menu

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

#creating a status bar
statusBar = Frame(root, bg=statusBarColor)
statusBar.pack(side="bottom", fill="x")

root.mainloop()