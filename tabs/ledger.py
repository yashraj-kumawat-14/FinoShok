#importing necessary modules and components and clases
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from sys import path

path.append(r"D:\projects\finoshok\finoshok\model")

from File import File
from Ledger import Ledger
import tkinter.messagebox as message


#AddFile class needs a parameter either a tk window or frame
class Ledgers:
    def __init__(self, parentWindow, fileId=None):

        self.fileId = fileId

        #create mainframe containing everything
        self.mainFrame = Frame(master=parentWindow)
        self.mainFrame.pack(fill="both", expand=True)

        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.columnconfigure(1, weight=1)
        self.mainFrame.columnconfigure(2, weight=1)

        self.subFrame1 = Frame(master=self.mainFrame, border=2, relief="groove", width=100, height=100)
        self.subFrame1.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.subFrame1.grid_propagate(False)
        self.subFrame1.pack_propagate(False)

        self.subFrame2 = Frame(master=self.mainFrame, border=2, relief="groove", width=50, height=100)
        self.subFrame2.grid(row=0, column=2, sticky="nsew")
        self.subFrame2.grid_propagate(False)
        self.subFrame2.pack_propagate(False)

        self.headingFrame = Frame(master=self.subFrame1, border=1, relief="groove", bg="black")
        self.headingFrame.pack(side="top", fill="x", ipady=5)

        self.headingFrame.rowconfigure(0, weight=1)
        self.headingFrame.columnconfigure(0, weight=1)
        self.headingFrame.columnconfigure(1, weight=1)
        self.headingFrame.columnconfigure(2, weight=1)

        self.ledgerLabel = Label(master=self.headingFrame, text="Ledger", font="COPPER 20 bold", bg="black", fg="orange")
        self.ledgerLabel.grid(row=0, column=0)

        self.customerNameLabel = Label(master=self.headingFrame, text="Customer : ", font="COPPER 13 bold", fg="orange", bg="black")
        self.customerNameLabel.grid(row=0, column=1)

        #creating a treeview table which will hold ledger data
        self.ledgerTable = ttk.Treeview(self.subFrame1)

        #creating table columns
        self.ledgerTable["columns"] = ("ledgerId", "emiDate", "emiAmount", "paidAmount", "penalty", "paidDate", "remainingAmount", "paidBy", "paidVia", "note", "status")

        self.ledgerTable.column("#0", width=0, minwidth=0, stretch=False)
        self.ledgerTable.column("ledgerId", width=35, minwidth=35, stretch=False, anchor="center")
        self.ledgerTable.column("emiDate", width=90, minwidth=90, anchor="center")
        self.ledgerTable.column("emiAmount", width=90, minwidth=90, anchor="center")
        self.ledgerTable.column("paidAmount", width=90, minwidth=90, anchor="center")
        self.ledgerTable.column("penalty", width=90, minwidth=90, anchor="center")
        self.ledgerTable.column("paidDate", width=90, minwidth=90, anchor="w")
        self.ledgerTable.column("remainingAmount", width=90, minwidth=90, anchor="center")
        self.ledgerTable.column("paidBy", width=90, minwidth=90, anchor="center")
        self.ledgerTable.column("paidVia", width=90, minwidth=90, anchor="center")
        self.ledgerTable.column("note", width=90, minwidth=90, anchor="center")
        self.ledgerTable.column("status", width=90, minwidth=90, anchor="center")

        self.ledgerTable.heading("ledgerId", text="Id", anchor="center")
        self.ledgerTable.heading("emiDate", text="Date", anchor="center")
        self.ledgerTable.heading("emiAmount", text="Amount", anchor="center")
        self.ledgerTable.heading("paidAmount", text="Paid amt", anchor="center")
        self.ledgerTable.heading("penalty", text="Penalty", anchor="center")
        self.ledgerTable.heading("paidDate", text="Paid Date", anchor="w")
        self.ledgerTable.heading("remainingAmount", text="Remaining Amt", anchor="w")
        self.ledgerTable.heading("paidBy", text="Paid By", anchor="center")
        self.ledgerTable.heading("paidVia", text="Paid Via", anchor="center")
        self.ledgerTable.heading("note", text="Note", anchor="center")
        self.ledgerTable.heading("status", text="Status", anchor="center")

        #setting up scrollbars for table to view data easily if neeeded
        self.ledgerTableScrollY = Scrollbar(self.subFrame1, orient="vertical", command=self.ledgerTable.yview)
        self.ledgerTableScrollY.pack(side="right", fill="y")

        self.ledgerTableScrollX = Scrollbar(self.subFrame1, orient="horizontal", command=self.ledgerTable.xview)
        self.ledgerTableScrollX.pack(side="bottom", fill="x")

        self.ledgerTable.pack(fill="both", expand=True, pady=5, padx=5)
        self.ledgerTable.config(yscrollcommand=self.ledgerTableScrollY.set, xscrollcommand=self.ledgerTableScrollX.set)

        #frame containing label file details for display purpose only
        self.fileDetailsLabelFrame = Frame(self.subFrame2, border=1, relief="groove", bg="black")
        self.fileDetailsLabelFrame.pack(side="top", fill="x", ipady=8, ipadx=8)

        self.fileDetailsLabelFrame.rowconfigure(0, weight=1)
        self.fileDetailsLabelFrame.columnconfigure(0, weight=1)

        #it is the label file details
        self.fileDetailsLabel = Label(master=self.fileDetailsLabelFrame, text="File Details", font="COPPER 16 bold", bg="black", fg="orange")
        self.fileDetailsLabel.grid(row=0, column=0)

        #now creating two equal sized frames one containing file details and other one ledger details along with edit opdtions
        self.fileDetailsFrame = Frame(self.subFrame2, relief="groove", border=1, width=100, height=100)
        self.fileDetailsFrame.pack(fill="both", expand=True)
        self.fileDetailsFrame.pack_propagate(False)
        self.fileDetailsFrame.grid_propagate(False)

        self.ledgerDetailsFrame = Frame(self.subFrame2, relief="groove", border=1, width=100, height=100)
        self.ledgerDetailsFrame.pack(fill="both", expand=True)
        self.ledgerDetailsFrame.pack_propagate(False)
        self.ledgerDetailsFrame.grid_propagate(False)

        #work of filedetailsframe starts here
        self.fileDetailsFrame.rowconfigure(0, weight=1)
        self.fileDetailsFrame.columnconfigure(0, weight=1)

        self.fileDetailsFrameInner = Frame(self.fileDetailsFrame)
        self.fileDetailsFrameInner.grid(row=0, column=0)

        self.statusLabel = Label(self.fileDetailsFrameInner, text="Status : NULL")
        self.statusLabel.grid(row=0, column=0, pady=8)

        self.loanTypeLabel = Label(self.fileDetailsFrameInner, text="Loan Type : NULL")
        self.loanTypeLabel.grid(row=0, column=1, pady=8)

        self.amountApprovedLabel = Label(self.fileDetailsFrameInner, text="Amount Approved : ")
        self.amountApprovedLabel.grid(row=1, column=0)

        self.rupeesLabel1 = Label(self.fileDetailsFrameInner, text="₹")
        self.rupeesLabel1.grid(row=1, column=2)

        self.interestLabel = Label(self.fileDetailsFrameInner, text="Interest : ")
        self.interestLabel.grid(row=2, column=0)

        self.interestPercentLabel = Label(self.fileDetailsFrameInner, text="% per annum")
        self.interestPercentLabel.grid(row=2, column=2)

        self.numOfEmi = Label(self.fileDetailsFrameInner, text="Num EMI : ")
        self.numOfEmi.grid(row=3, column=0)

        self.loanPeriodLabel = Label(self.fileDetailsFrameInner, text="Loan Period : ")
        self.loanPeriodLabel.grid(row=4, column=0)

        self.loanTimeLabel = Label(self.fileDetailsFrameInner, text="In months")
        self.loanTimeLabel.grid(row=4, column=2)

        self.installmentAmtLabel = Label(self.fileDetailsFrameInner, text="EMI Amount : ")
        self.installmentAmtLabel.grid(row=5, column=0)

        self.rupeesLabel2 = Label(self.fileDetailsFrameInner, text="₹ per 30 days")
        self.rupeesLabel2.grid(row=5, column=2)

        self.dateApprovedLabel = Label(self.fileDetailsFrameInner, text="Date Approved : ")
        self.dateApprovedLabel.grid(row=6, column=0)

        self.loanPurposeLabel = Label(self.fileDetailsFrameInner, text="Purpose : ")
        self.loanPurposeLabel.grid(row=7, column=0)

        self.amountApprovedVar = StringVar()
        self.amountApprovedEntry = Entry(self.fileDetailsFrameInner, textvariable=self.amountApprovedVar, justify="center", state="readonly")
        self.amountApprovedEntry.grid(row=1, column=1)

        self.interestVar = StringVar()
        self.interestEntry = Entry(self.fileDetailsFrameInner, textvariable=self.interestVar, justify="center", state="readonly")
        self.interestEntry.grid(row=2, column=1)

        self.numOfEmiVar = StringVar()
        self.numOfEmiEntry = Entry(self.fileDetailsFrameInner, textvariable=self.numOfEmiVar, justify="center", state="readonly")
        self.numOfEmiEntry.grid(row=3, column=1) 

        self.loanPeriodVar = StringVar()
        self.loanPeriodEntry = Entry(self.fileDetailsFrameInner, textvariable=self.loanPeriodVar, justify="center", state="readonly")
        self.loanPeriodEntry.grid(row=4, column=1)

        self.installmentAmtVar = StringVar()
        self.installmentAmtEntry = Entry(self.fileDetailsFrameInner, textvariable=self.installmentAmtVar, justify="center", state="readonly")
        self.installmentAmtEntry.grid(row=5, column=1)

        self.dateApprovedEntry = DateEntry(self.fileDetailsFrameInner, width=17, date_pattern="yyyy-mm-dd", justify="center", state="disable", selectmode="day")
        self.dateApprovedEntry.grid(row=6, column=1)

        self.loanPurposeEntry = Text(self.fileDetailsFrameInner, height=1, width=15, state="disabled")
        self.loanPurposeEntry.grid(row=7, column=1, pady=3)

        #work of self.fileDetailsFrame ends here

        #work of self.ledgerDetailsFrame starts here
        self.ledgerDetailsFrame.rowconfigure(0, weight=1)
        self.ledgerDetailsFrame.columnconfigure(0, weight=1)
        
        self.ledgerDetailsFrameInner = Frame(self.ledgerDetailsFrame)
        self.ledgerDetailsFrameInner.grid(row=0, column=0)

        self.ledgerEmiNoteLabel = Label(self.ledgerDetailsFrameInner, text="Note : ", font="COPPER 10 bold")
        self.ledgerEmiNoteLabel.grid(row=6, column=0)

        self.rupeesLabel3 = Label(self.ledgerDetailsFrameInner, text="  ₹")
        self.rupeesLabel3.grid(row=4, column=2)

        self.rupeesLabel4 = Label(self.ledgerDetailsFrameInner, text="  ₹")
        self.rupeesLabel4.grid(row=1, column=2)

        self.rupeesLabel5 = Label(self.ledgerDetailsFrameInner, text="  ₹")
        self.rupeesLabel5.grid(row=7, column=2)

        self.ledgerEmiPaidDateLabel = Label(self.ledgerDetailsFrameInner, text="Paid Date : ", font="COPPER 10 bold")
        self.ledgerEmiPaidDateLabel.grid(row=0, column=0)

        self.ledgerEmiPaidByLabel = Label(self.ledgerDetailsFrameInner, text="Paid By : ", font="COPPER 10 bold")
        self.ledgerEmiPaidByLabel.grid(row=3, column=0)

        self.ledgerEmiStatusLabel = Label(self.ledgerDetailsFrameInner, text="Paid Status : ", font="COPPER 10 bold")
        self.ledgerEmiStatusLabel.grid(row=2, column=0)

        self.ledgerEmiPenaltyLabel = Label(self.ledgerDetailsFrameInner, text="Penalty : ", font="COPPER 10 bold")
        self.ledgerEmiPenaltyLabel.grid(row=4, column=0)

        self.ledgerEmiPaidAmountLabel = Label(self.ledgerDetailsFrameInner, text="Paid Amount : ", font="COPPER 10 bold")
        self.ledgerEmiPaidAmountLabel.grid(row=1, column=0)

        self.ledgerEmiPaidViaLabel = Label(self.ledgerDetailsFrameInner, text="Paid Via : ", font="COPPER 10 bold")
        self.ledgerEmiPaidViaLabel.grid(row=5, column=0)

        self.ledgerEmiRemainingAmountLabel = Label(self.ledgerDetailsFrameInner, text="Remaining Amt : ", font="COPPER 10 bold")
        self.ledgerEmiRemainingAmountLabel.grid(row=7, column=0)

        #entries
        self.ledgerEmiPaidDateEntry = DateEntry(self.ledgerDetailsFrameInner, width=17, date_pattern="yyyy-mm-dd", justify="center", state="disable", selectmode="day")
        self.ledgerEmiPaidDateEntry.grid(row=0, column=1)

        self.ledgerEmiPaidAmountVar = StringVar()
        self.ledgerEmiPaidAmountEntry = Entry(self.ledgerDetailsFrameInner, textvariable=self.ledgerEmiPaidAmountVar)
        self.ledgerEmiPaidAmountEntry.grid(row=1, column=1)

        #eventhandler for ledgerEmiPaidAmountEntry
        def ledgerEmiPaidAmountEntryEventHandler(event):
            tempString = ""
            for char in self.ledgerEmiPaidAmountEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char

            tempString = tempString.lstrip("0")
            if(tempString==""):
                tempString="0"

            self.ledgerEmiPaidAmountEntry.delete(0, "end")
            self.ledgerEmiPaidAmountEntry.insert("end", tempString)

        self.ledgerEmiPaidAmountEntry.bind("<KeyRelease>", ledgerEmiPaidAmountEntryEventHandler)

        self.ledgerEmiStatusVar = IntVar()
        self.ledgerEmiStatusEntry = Checkbutton(self.ledgerDetailsFrameInner, variable=self.ledgerEmiStatusVar)
        self.ledgerEmiStatusEntry.grid(row=2, column=1, sticky="w")

        self.ledgerEmiPaidByVar = StringVar()
        self.ledgerEmiPaidByEntry = Entry(self.ledgerDetailsFrameInner, textvariable=self.ledgerEmiPaidByVar)
        self.ledgerEmiPaidByEntry.grid(row=3, column=1)

        self.ledgerEmiPenaltyVar = StringVar()
        self.ledgerEmiPenaltyEntry = Entry(self.ledgerDetailsFrameInner, textvariable=self.ledgerEmiPenaltyVar)
        self.ledgerEmiPenaltyEntry.grid(row=4, column=1)

        #eventhandler for ledgerEmiPenaltyEntry
        def ledgerEmiPenaltyEntryEventHandler(event):
            tempString = ""
            for char in self.ledgerEmiPenaltyEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char
            
            self.ledgerEmiPenaltyEntry.delete(0, "end")

            tempString = tempString.lstrip("0")
            if(tempString==""):
                tempString="0"

            self.ledgerEmiPenaltyEntry.insert("end", tempString)
        
        self.ledgerEmiPenaltyEntry.bind("<KeyRelease>", ledgerEmiPenaltyEntryEventHandler)

        self.ledgerEmiPaidViaVar = StringVar()
        self.ledgerEmiPaidViaEntry = Entry(self.ledgerDetailsFrameInner, textvariable=self.ledgerEmiPaidViaVar)
        self.ledgerEmiPaidViaEntry.grid(row=5, column=1)

        self.ledgerEmiNoteEntry = Text(self.ledgerDetailsFrameInner, width=15, height=1)
        self.ledgerEmiNoteEntry.grid(row=6, column=1)

        self.ledgerEmiRemainingAmountVar = StringVar()
        self.ledgerEmiRemainingAmountEntry = Entry(self.ledgerDetailsFrameInner, textvariable=self.ledgerEmiRemainingAmountVar, state="disabled")
        self.ledgerEmiRemainingAmountEntry.grid(row=7, column=1)

        #buttons 
        self.editLedgerButton = Button(self.ledgerDetailsFrameInner, text="Edit", bg="grey", fg="white", command=self.edit)
        self.editLedgerButton.grid(row=8, column=0, sticky="we", pady=5, padx=3)

        self.cancelLedgerButton = Button(self.ledgerDetailsFrameInner, text="Cancel", command=self.cancel)
        self.cancelLedgerButton.grid(row=8, column=1, sticky="we", pady=5, padx=3)

        self.saveLedgerButton = Button(self.ledgerDetailsFrameInner, text="Save", bg="light green", fg="black", command=self.save)
        self.saveLedgerButton.grid(row=8, column=2, sticky="we", pady=5, padx=3, ipadx=10)

        self.ledgerTable.bind("<<TreeviewSelect>>", self.dynamicLedgerDetailsController)
        self.ledgerController()

    def ledgerController(self):
        if(self.fileId==None):
            self.disableAll()
            return None
        items = self.ledgerTable.get_children()
        self.ledgerTable.delete(*items)
        self.fileObject = File()
        self.fileData = self.fileObject.whereData(id=self.fileId)

        if(self.fileData):
            print(self.fileData)
            self.amountApprovedVar.set(self.fileData[0][2])
            self.interestVar.set(self.fileData[0][3])
            self.numOfEmiVar.set(self.fileData[0][7])
            self.loanPeriodVar.set(self.fileData[0][4])
            self.installmentAmtVar.set(self.fileData[0][6])
            self.dateApprovedEntry.config(state='normal')
            self.dateApprovedEntry.set_date(self.fileData[0][9])
            self.dateApprovedEntry.config(state='disabled')
            self.loanPurposeEntry.config(state='normal')
            self.loanPurposeEntry.delete("1.0", "end")
            self.loanPurposeEntry.insert("end", self.fileData[0][8])
            self.loanPurposeEntry.config(state='disabled')
            self.statusLabel.config(text="Status : Active" if (self.fileData[0][5]==1) else "Status : Inactive", bg="light green" if (self.fileData[0][5]==1) else "red")

            self.ledgerObject = Ledger()
            self.ledgerData = self.ledgerObject.whereData(fileId=self.fileId)
            lengthOfLedger = len(self.ledgerData)

            for i in range(lengthOfLedger):
                self.ledgerTable.insert(parent="", text="", iid=i+1, index="end", values=(self.ledgerData[i][0], self.ledgerData[i][4], self.ledgerData[i][5], self.ledgerData[i][8], self.ledgerData[i][7], self.ledgerData[i][6], self.ledgerData[i][12],self.ledgerData[i][10], self.ledgerData[i][11], self.ledgerData[i][9], self.ledgerData[i][3]))
            
            self.ledgerTable.selection_set(1)
            self.dynamicLedgerDetailsController()
        else:
            self.disableAll()
        
    
    def dynamicLedgerDetailsController(self, event=None):
        iid = self.ledgerTable.selection()[0]
        values = self.ledgerTable.item(iid, "values")
        self.enableAll()
        print(values[5])
        if(values[5]!="None") :
            self.ledgerEmiPaidDateEntry.set_date(values[5])
        else:
            self.ledgerEmiPaidDateEntry.set_date("1995-1-1")

        self.ledgerEmiPaidAmountVar.set(values[3])if(values[3]!="None") else self.ledgerEmiPaidAmountVar.set("")
        self.ledgerEmiStatusVar.set(values[10])if(values[9]!="None") else self.ledgerEmiStatusVar.set("")
        self.ledgerEmiPaidByVar.set(values[7])if(values[6]!="None") else self.ledgerEmiPaidByVar.set("")
        self.ledgerEmiPenaltyVar.set(values[4])if(values[4]!="None") else self.ledgerEmiPenaltyVar.set("")
        self.ledgerEmiPaidViaVar.set(values[8])if(values[7]!="None") else self.ledgerEmiPaidViaVar.set("")

        self.ledgerEmiRemainingAmountVar.set(values[6])if(values[6]!="None") else self.ledgerEmiRemainingAmountVar.set("")

        # self.ledgerEmiRemainingAmountVar.set()
        if(values[9]!="None"):
            self.ledgerEmiNoteEntry.delete("1.0", "end")
            self.ledgerEmiNoteEntry.insert("end", values[9])
            self.disableAll()
            self.editLedgerButton.config(state="normal")
        else:
            self.ledgerEmiNoteEntry.delete("1.0", "end")
            self.ledgerEmiNoteEntry.insert("end", "")
            self.disableAll()
            self.editLedgerButton.config(state="normal")

    def edit(self):
        self.enableAll()
        self.editLedgerButton.config(state="disable")
        self.saveLedgerButton.config(state="normal")
        self.cancelLedgerButton.config(state="normal")
    
    def cancel(self):
        self.ledgerController()
    
    def save(self):
        sure=message.askyesno("Are you sure ?", "are you sure you want to\nmake this change ?")
        if(sure):
            paidDate = str(self.ledgerEmiPaidDateEntry.get_date().year)+"/"+str(self.ledgerEmiPaidDateEntry.get_date().month)+"/"+str(self.ledgerEmiPaidDateEntry.get_date().day)

            updateSuccessfully = self.ledgerObject.updateData(id=self.ledgerTable.item(self.ledgerTable.selection()[0], "values")[0], status = self.ledgerEmiStatusVar.get(), paidDate=paidDate, penalty=self.ledgerEmiPenaltyVar.get(), paidAmount=self.ledgerEmiPaidAmountVar.get(), Note=self.ledgerEmiNoteEntry.get("1.0", "end"), paidBy=self.ledgerEmiPaidByVar.get(), paidVia=self.ledgerEmiPaidViaVar.get())

            if(updateSuccessfully):
                self.ledgerController()
                message.showinfo("info", "Ledger Updated successfully.")

    def disableAll(self):
        self.ledgerEmiPaidAmountEntry.config(state="disabled")
        self.ledgerEmiPaidViaEntry.config(state="disabled")
        self.ledgerEmiNoteEntry.config(state="disabled")
        self.ledgerEmiStatusEntry.config(state="disabled")
        self.ledgerEmiPenaltyEntry.config(state="disabled")
        self.ledgerEmiPaidDateEntry.config(state="disabled")
        self.ledgerEmiPaidByEntry.config(state="disabled")
        self.editLedgerButton.config(state="disabled")
        self.saveLedgerButton.config(state="disabled")
        self.cancelLedgerButton.config(state="disabled")

    def enableAll(self):
        self.ledgerEmiPaidAmountEntry.config(state="normal")
        self.ledgerEmiPaidViaEntry.config(state="normal")
        self.ledgerEmiNoteEntry.config(state="normal")
        self.ledgerEmiStatusEntry.config(state="normal")
        self.ledgerEmiPenaltyEntry.config(state="normal")
        self.ledgerEmiPaidDateEntry.config(state="normal")
        self.ledgerEmiPaidByEntry.config(state="normal")
        self.editLedgerButton.config(state="normal")
        self.saveLedgerButton.config(state="normal")
        self.cancelLedgerButton.config(state="normal")


if __name__=="__main__":
    root = Tk()
    root.title("Ledgers List ")
    root.geometry("1000x700")
    ledgers = Ledgers(root, fileId=3)
    root.mainloop()