from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from sys import path
path.append(r"D:\projects\finoshok\finoshok\model")
#now we can import Customer and Request class successfully from customer model and Rewusts model respectively
from Customer import Customer
from Request import Request
from tkinter.messagebox import showinfo

#AddFile class needs a parameter either a tk window or frame
class AddLoanRequest:
    def __init__(self, addFileWindow, parentUpdateStatus=None):
        #assigining the parentUpdateStatus function to self.parentUpdateStatus variable
        self.parentUpdateStatus = parentUpdateStatus
        self.data = Customer().readAllData()
        self.customerId = None

        #heading label of the tab
        addLoanRequestLabel = Label(addFileWindow, text="Add New loan request", font="COPPER 15", fg="yellow", bg="black")
        addLoanRequestLabel.pack(side="top", fill=X, ipady=20)
        
        self.instructionLabel = Label(addFileWindow, text="", font="COPPER 13", fg="red", bg="black")
        self.instructionLabel.pack(side="top", fill="x",ipady=10)

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

        #save button allows to save credit requuset into database
        saveButton = ttk.Button(mainFrame, text="Save", command=self.save)
        saveButton.grid(row=1, column=0)
    
    #saves details in request table
    def save(self):
        #checking if the fields are filled properly
        if((not self.clientVar.get())):
            requirementsFilled=False
            instructionText = "Please enter existing customer aadhar \n field correctly."
        elif((len(self.aadharVar.get())!=12) or (not self.aadharVar.get().isdigit())):
            requirementsFilled=False
            instructionText = "Please Fill Right Format of Aadhar"
        elif((not self.loanVar.get()) or (not str(self.loanVar.get()).isdigit())):
            requirementsFilled=False
            instructionText = "Please enter correct loan amount in digits."
        elif(not self.dateOfRequestEntry.get()):
            requirementsFilled=False
            instructionText = "Please enter date on which loan was requested"
        elif(not self.purposeVar.get()):
            requirementsFilled=False
            instructionText = "Please enter the purpose of loan"
        else:
            requirementsFilled=True

        #saving details only if requirementsFilled is true and self.customerId is defined
        if(requirementsFilled and self.customerId):
            #creating a requests object to insert data
            obj = Request()
            #result true means successfull insertion and false meanse unsuccessfull insertion
            result = obj.insertData(customer_id = self.customerId, requested_amount = self.loanVar.get(), purpose=self.purposeVar.get(), date = self.dateOfRequestEntry.get())
            
            #if result is true then show messafe that credit request added and set the values of fields to their default
            if(result):
                self.aadharVar.set("")
                self.clientVar.set("")
                self.loanVar.set(0)
                self.purposeVar.set("")
                self.instructionLabel.config(text="")
                instructionText = f"Loan request for {self.clientVar.get()} has added successfully."
                showinfo("Loan request added", instructionText)
                self.updateStatus()
            else:
                #instruct teh user that loan request cannot be added if result is false
                self.instructionLabel.config(text="Loan request addition unsuccessfull.", fg="red")

        #if requirementfilled is false then show the instructionText
        elif(not requirementsFilled):
            self.instructionLabel.config(text=instructionText, fg="red")
    
    #updateStatus function used for letting the parentWindow get update with the changes made in this window
    def updateStatus(self, **kwargs):
        #running parentUpdateStatus method only if it is defined
        if(self.parentUpdateStatus):
            self.parentUpdateStatus()
            
        
if __name__=="__main__":
    root = Tk()
    root.geometry("599x499")
    root.title("add new file")
    AddLoanRequest(root)
    root.mainloop()
