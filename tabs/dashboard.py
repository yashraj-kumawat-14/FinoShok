from tkinter import *

class Dashboard:
    def __init__(self, dashboardWindow):

        mainFrameColor="black"
        #create mainframe containing everything
        mainFrame = Frame(dashboardWindow, bg=mainFrameColor)
        mainFrame.pack(fill="both", expand=True)

        #columnconfigure() resizes the grid vertically, while rowconfigure() resizes the grid horizontally. The width of a grid column is equal to the width of its widest cell.
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=1)
        
        subFrame1Color = "red"
        subFrame2Color = "blue"
        subFrame3Color = "green"
        subFrame4Color = "pink"

        #created subframes for showing different graphs and data
        
        #The sticky parameter in the .grid() method of Tkinter is used to define how a widget should expand to fill the space allocated to it within a grid cell.
        subFrame1 = Frame(mainFrame, bg=subFrame1Color)
        subFrame1.grid(row=0, column=0, sticky="ewns")

        subFrame2 = Frame(mainFrame, bg=subFrame2Color)
        subFrame2.grid(row=0, column=1, sticky="ewns")
        
        subFrame3 = Frame(mainFrame, bg=subFrame3Color)
        subFrame3.grid(row=1, column=0, sticky="ewns")

        subFrame4 = Frame(mainFrame, bg=subFrame4Color)
        subFrame4.grid(row=1, column=1, sticky="ewns")


if __name__ == "__main__":
    root = Tk()
    root.geometry("499x499")
    Dashboard(root)
    root.mainloop()