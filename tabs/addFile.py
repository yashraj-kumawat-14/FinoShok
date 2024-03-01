from tkinter import *
from tkinter import ttk


#AddFile class needs a parameter either a tk window or frame
class AddFile:
    def __init__(self, addFileWindow):

        #heading label of the tab
        addFileLabel = Label(addFileWindow, text="Add New File", font="COPPER 15", fg="yellow", bg="black")
        addFileLabel.pack(side="top", fill=X, ipady=20)

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
        borrowerNameLabel = Label(subFrame, text="Borrower : ", fg=labelFgColor, bg=labelBgColor)
        borrowerNameLabel.grid(row=0, column=0)

        lenderBranchLabel = Label(subFrame, text="Lender Branch : ", fg=labelFgColor, bg=labelBgColor)
        lenderBranchLabel.grid(row=1, column=0)

        loanAmtLabel = Label(subFrame, text="Loan Amount : ", fg=labelFgColor, bg=labelBgColor)
        loanAmtLabel.grid(row=2, column=0)

        interestLabel = Label(subFrame, text="Interest Rate % : ", fg=labelFgColor, bg=labelBgColor)
        interestLabel.grid(row=3, column=0)

        timePeriodLabel = Label(subFrame, text="Time Period : ", fg=labelFgColor, bg=labelBgColor)
        timePeriodLabel.grid(row=4, column=0)

        totalEmiLabel = Label(subFrame, text="Total Emi's : ", fg=labelFgColor, bg=labelBgColor)
        totalEmiLabel.grid(row=5, column=0)

        emiAmtLabel = Label(subFrame, text="Emi amount : ", fg=labelFgColor, bg=labelBgColor)
        emiAmtLabel.grid(row=6, column=0)

        #created combobox and entries in subframe

        #combobox is a ttk themed widget which is combination of list box and entry widget used to make a dropdown
        borrowerVar = StringVar()
        borrowerCombobox = ttk.Combobox(subFrame, textvariable=borrowerVar, values=["yashraj", "kundan", "raj", "bhavesh"], state="readonly")
        borrowerCombobox.grid(row=0, column=1)

        lenderVar = StringVar()
        lenderCombobox = ttk.Combobox(subFrame, textvariable=lenderVar, values=["hariom", "bob", "sbi"], state="readonly")
        lenderCombobox.grid(row=1, column=1)

        loanVar = IntVar()
        loanVar.set(96000)
        loanAmtEntry = Entry(subFrame, width=23, textvariable=loanVar, justify="right")
        loanAmtEntry.grid(row=2, column=1)

        interestVar = IntVar()
        interestVar.set(2)
        interestEntry = Entry(subFrame, width=23, textvariable=interestVar, justify="right")
        interestEntry.grid(row=3, column=1)

        timeVar = StringVar()
        timeCombobox = ttk.Combobox(subFrame, textvariable=timeVar, values=["1 month", "2 month", "3 month", "type mannually"], state="readonly")
        timeCombobox.grid(row=4, column=1)

        eminumVar = StringVar()
        eminumVar.set(6)
        eminumCombobox = ttk.Combobox(subFrame, textvariable=eminumVar, values=["1", "2", "3","6", "type mannually"], state="readonly")
        eminumCombobox.grid(row=5, column=1)

        emiAmtVar = IntVar()
        emiAmtVar.set(eval(f"{float(loanVar.get())/float(eminumVar.get())}"))
        emiAmtEntry = Entry(subFrame, width=23, textvariable=emiAmtVar, justify="right")
        emiAmtEntry.grid(row=6, column=1)

        nextButton = ttk.Button(mainFrame, text="Next")
        nextButton.grid(row=1, column=0)

        

        

if __name__=="__main__":
    root = Tk()
    root.geometry("599x499")
    root.title("add new file")
    AddFile(root)
    root.mainloop()
