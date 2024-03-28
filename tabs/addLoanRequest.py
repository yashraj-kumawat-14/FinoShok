from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

#AddFile class needs a parameter either a tk window or frame
class AddLoanRequest:
    def __init__(self, addFileWindow):

        #heading label of the tab
        addLoanRequestLabel = Label(addFileWindow, text="Add New loan request", font="COPPER 15", fg="yellow", bg="black")
        addLoanRequestLabel.pack(side="top", fill=X, ipady=20)

        #created mainFrame which will hold everything of AddCustomer page
        mainFrameColor="black"
        subFrameColor = "black"

        mainFrame = Frame(addFileWindow, bg=mainFrameColor)
        mainFrame.pack(fill="both", expand=True)

        #congiguring row 0, 1 and column 0 to make the center in the frame
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)

        #created subframe
        subFrame = Frame(mainFrame, bg=subFrameColor,width=200, height=200)
        subFrame.grid(row=0, column=0)

        labelFgColor = "yellow"
        labelBgColor = "black"

        #naming labels creation in the subframe
        clientNameLabel = Label(subFrame, text="Borrower : ", fg=labelFgColor, bg=labelBgColor)
        clientNameLabel.grid(row=0, column=0)

        loanAmtLabel = Label(subFrame, text="Loan Amount : ", fg=labelFgColor, bg=labelBgColor)
        loanAmtLabel.grid(row=1, column=0)

        dateOfRequestLabel = Label(subFrame, text="Requested Date : ", fg=labelFgColor, bg=labelBgColor)
        dateOfRequestLabel.grid(row=2, column=0)

        #created combobox and entries in subframe

        #combobox is a ttk themed widget which is combination of list box and entry widget used to make a dropdown
        clientVar = StringVar()
        clientCombobox = ttk.Combobox(subFrame, textvariable=clientVar, values=["yashraj", "kundan", "raj", "bhavesh"], state="readonly", justify="center")
        clientCombobox.grid(row=0, column=1)

        loanVar = IntVar()
        loanVar.set(96000)
        loanAmtEntry = Entry(subFrame, width=23, textvariable=loanVar, justify="center")
        loanAmtEntry.grid(row=1, column=1)

        dateOfRequestEntry = DateEntry(subFrame, width=20, date_pattern="d/m/y", justify="center")
        dateOfRequestEntry.grid(row=2, column=1)

        saveButton = ttk.Button(mainFrame, text="Save")
        saveButton.grid(row=1, column=0)

        
if __name__=="__main__":
    root = Tk()
    root.geometry("599x499")
    root.title("add new file")
    AddLoanRequest(root)
    root.mainloop()
