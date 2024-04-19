from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from sys import path
path.append(r"D:\projects\finoshok\finoshok\model")
#now we can import Customer and Requests class successfully from customer model and Rewusts model respectively
from Customer import Customer
from Requests import Requests

#AddFile class needs a parameter either a tk window or frame
class AddLoanRequest:
    def __init__(self, addFileWindow):

        self.data = Customer().readAllData()
        self.customerId = None

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
        aadharLabel = Label(subFrame, text="Aadhar : ", fg=labelFgColor, bg=labelBgColor)
        aadharLabel.grid(row=0, column=0, sticky="e")

        clientNameLabel = Label(subFrame, text="Borrower : ", fg=labelFgColor, bg=labelBgColor)
        clientNameLabel.grid(row=1, column=0, sticky="e")

        loanAmtLabel = Label(subFrame, text="Loan Amount : ", fg=labelFgColor, bg=labelBgColor)
        loanAmtLabel.grid(row=2, column=0, sticky="e")

        rupeesLabel = Label(subFrame, text="₹", fg=labelFgColor, bg=labelBgColor)
        rupeesLabel.grid(row=2, column=2, sticky="e")

        dateOfRequestLabel = Label(subFrame, text="Requested Date : ", fg=labelFgColor, bg=labelBgColor)
        dateOfRequestLabel.grid(row=3, column=0, sticky="e")

        purposeLabel = Label(subFrame, text="Loan Purpose : ", fg=labelFgColor, bg=labelBgColor)
        purposeLabel.grid(row=4, column=0, sticky="e")


        #created entries in subframe

        self.aadharVar = StringVar()
        self.aadharEntry = Entry(subFrame, textvariable=self.aadharVar, width=23, justify="center")
        self.aadharEntry.grid(row=0, column=1)

        #event handler for aadhar entry to restrict user from entering more than 12 digits or letters, character and to insert name of client / borrower dynamically
        def aadharEntryEventHandler(event):
            tempString = ""
            for char in self.aadharEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char
            
            if(len(tempString)>12):
                tempString = tempString[0:12]
                self.aadharVar.set(tempString)
            else:
                self.aadharVar.set(tempString)

            if(len(self.aadharVar.get())==12):
                for i in self.data:
                    if(tempString==str(i[6])):
                        self.clientVar.set(i[1])
                        self.customerId = i[0]
                        break
            else:
                self.clientVar.set("")
            

        #binding the aadharentry to KeyRelease event with function as aadharentrtyevnthandler
        self.aadharEntry.bind("<KeyRelease>", aadharEntryEventHandler)

        self.clientVar = StringVar()
        self.clientCombobox = Entry(subFrame, textvariable=self.clientVar, width=23, justify="center", state="readonly")
        self.clientCombobox.grid(row=1, column=1)

        self.loanVar = IntVar()
        self.loanVar.set("")
        self.loanAmtEntry = Entry(subFrame, width=23, textvariable=self.loanVar, justify="center")
        self.loanAmtEntry.grid(row=2, column=1)

        #evetn handiling function tro handle keyrelease event of loanamtentry to restrict user from entering non digit characters
        def loanAmtEntryHandler(event):
            tempString = ""
            for char in self.loanAmtEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char

            self.loanVar.set(tempString)

        #binding Keyrelease event of loanamtentry with loanamtentryevetnhandler
        self.loanAmtEntry.bind("<KeyRelease>", loanAmtEntryHandler)

        self.dateOfRequestEntry = DateEntry(subFrame, width=20, date_pattern="yyyy-mm-dd", justify="center")
        self.dateOfRequestEntry.grid(row=3, column=1)
        
        self.purposeVar = StringVar()
        self.purposeEntry = Entry(subFrame, textvariable=self.purposeVar, width=23, justify="center")
        self.purposeEntry.grid(row=4, column=1)

        saveButton = ttk.Button(mainFrame, text="Save", command=self.save)
        saveButton.grid(row=1, column=0)
    
    #saves details in request table
    def save(self):
        if(self.aadharVar.get() and self.loanVar.get() and self.clientVar.get() and self.dateOfRequestEntry.get() and self.customerId):
            obj = Requests()
            result = obj.insertData(customer_id = self.customerId, requested_amount = self.loanVar.get(), purpose=self.purposeVar.get(), date = self.dateOfRequestEntry.get())
            if(result):
                print("success")
        
if __name__=="__main__":
    root = Tk()
    root.geometry("599x499")
    root.title("add new file")
    AddLoanRequest(root)
    root.mainloop()
