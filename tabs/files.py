#importing necessary modules and components and clases
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from sys import path

path.append(r"D:\projects\finoshok\finoshok\model")

from File import File
from Customer import Customer
from Ledger import Ledger
import tkinter.messagebox as message

class Files:
    def __init__(self, parentWindow):
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

        self.headingFrame = Frame(self.subFrame1, border=1, relief="groove")
        self.headingFrame.pack(fill="x")


        #work under subframe1 start here
        
        self.searchFilesFrame = Frame(self.subFrame1, border=2, relief="groove", bg="black")
        self.searchFilesFrame.pack(fill="x", pady=5, ipadx=5, padx=5, ipady=1)

        #work of search frame starts here

        self.searchFilesFrame.rowconfigure(0, weight=1)
        self.searchFilesFrame.columnconfigure(2, weight=1)

        self.searchFilesLabel = Label(self.searchFilesFrame, text="Search : ", font="COPPER 13", bg="black", fg="white")
        self.searchFilesLabel.grid(row=0, column=0, sticky="e")

        self.searchFilesVar = StringVar()
        self.searchFilesEntry = Entry(self.searchFilesFrame, textvariable=self.searchFilesVar)
        self.searchFilesEntry.grid(row=0, column=1, sticky="w")

        self.refreshButton = Button(self.searchFilesFrame, text=u"\u21BB", bg="orange", fg="white", font="COPPER 13 bold", border=0, command=self.refresh)
        self.refreshButton.grid(row=0, column=2, ipadx=3, sticky="e", ipady=0)

        self.filesTableFrame = Frame(self.subFrame1, border=1, relief="groove")
        self.filesTableFrame.pack(fill="both", expand=True, pady=2, ipadx=5, padx=5, ipady=5)

        self.filesTable = ttk.Treeview(self.filesTableFrame)

        self.filesTable["columns"] = ("s.no.", "fileId", "fileAmount", "dateApproved", "customerName", "status")
        
        self.filesTable.column("#0", width=0, minwidth=0, stretch=False)
        self.filesTable.column("s.no.", width=40, minwidth=40, anchor="center", stretch=False)
        self.filesTable.column("fileId", width=100, minwidth=100, anchor="center")
        self.filesTable.column("fileAmount", width=100, minwidth=100, anchor="center")
        self.filesTable.column("dateApproved", width=100, minwidth=100, anchor="center")
        self.filesTable.column("customerName", width=100, minwidth=100, anchor="center")
        self.filesTable.column("status", width=80, minwidth=80, anchor="center")

        self.filesTable.heading("s.no.", text="S.No.", anchor="center")
        self.filesTable.heading("fileId", text="File Id", anchor="center")
        self.filesTable.heading("fileAmount", text="File Amount", anchor="center")
        self.filesTable.heading("dateApproved", text="Date Approved", anchor="center")
        self.filesTable.heading("customerName", text="Customer Name", anchor="center")
        self.filesTable.heading("status", text="Status", anchor="center")

        self.filesTableScrollX = Scrollbar(self.filesTable, orient="horizontal", command=self.filesTable.xview)
        self.filesTableScrollX.pack(fill="x", side="bottom")

        self.filesTableScrollY = Scrollbar(self.filesTable, orient="vertical", command=self.filesTable.yview)
        self.filesTableScrollY.pack(fill="y", side="right")

        self.filesTable.pack(fill="both", expand=True)
        self.filesTable.config(yscrollcommand=self.filesTableScrollY.set, xscrollcommand=self.filesTableScrollX.set)

        #work of subframe1 ends here

        #work of subframe2 starts here

        self.subFrame2.rowconfigure(1 , weight=1)
        self.subFrame2.columnconfigure(0, weight=1)

        self.instructionFrame = Frame(self.subFrame2, border=1, relief="groove")
        self.instructionFrame.grid(row=0, column=0, sticky="nsew")

        self.fileDetailsFrameInner = Frame(self.subFrame2)
        self.fileDetailsFrameInner.grid(row=1, column=0)

        self.statusLabel = Label(self.fileDetailsFrameInner, text="Status : NULL  ")
        self.statusLabel.grid(row=0, column=0, pady=8, sticky="e")

        self.loanTypeLabel = Label(self.fileDetailsFrameInner, text="Loan Type : NULL")
        self.loanTypeLabel.grid(row=0, column=1, pady=8)

        self.amountApprovedLabel = Label(self.fileDetailsFrameInner, text="Amount Approved : ")
        self.amountApprovedLabel.grid(row=1, column=0, sticky="e")

        self.rupeesLabel1 = Label(self.fileDetailsFrameInner, text="₹")
        self.rupeesLabel1.grid(row=1, column=2, sticky="e")

        self.interestLabel = Label(self.fileDetailsFrameInner, text="Interest : ")
        self.interestLabel.grid(row=2, column=0, sticky="e")

        self.interestPercentLabel = Label(self.fileDetailsFrameInner, text="% per annum")
        self.interestPercentLabel.grid(row=2, column=2, sticky="e")

        self.numOfEmi = Label(self.fileDetailsFrameInner, text="Num EMI : ")
        self.numOfEmi.grid(row=3, column=0, sticky="e")

        self.loanPeriodLabel = Label(self.fileDetailsFrameInner, text="Loan Period : ")
        self.loanPeriodLabel.grid(row=4, column=0, sticky="e")

        self.loanTimeLabel = Label(self.fileDetailsFrameInner, text="In months")
        self.loanTimeLabel.grid(row=4, column=2, sticky="e")

        self.installmentAmtLabel = Label(self.fileDetailsFrameInner, text="EMI Amount : ")
        self.installmentAmtLabel.grid(row=5, column=0, sticky="e")

        self.rupeesLabel2 = Label(self.fileDetailsFrameInner, text="₹ per 30 days")
        self.rupeesLabel2.grid(row=5, column=2, sticky="e")

        self.dateApprovedLabel = Label(self.fileDetailsFrameInner, text="Date Approved : ")
        self.dateApprovedLabel.grid(row=6, column=0, sticky="e")

        self.loanPurposeLabel = Label(self.fileDetailsFrameInner, text="Purpose : ")
        self.loanPurposeLabel.grid(row=7, column=0, sticky="e")

        self.amountApprovedVar = StringVar()
        self.amountApprovedEntry = Entry(self.fileDetailsFrameInner, textvariable=self.amountApprovedVar, justify="center", state="readonly")
        self.amountApprovedEntry.grid(row=1, column=1, sticky="e")

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

        self.viewLedgerButton = Button(self.fileDetailsFrameInner, text="View Ledger", bg='grey', fg="white")
        self.viewLedgerButton.grid(row=8, column=0, columnspan=3, sticky="we", pady=10)

        self.filesTable.bind("<<TreeviewSelect>>", self.dynamicFileDetailsController)
        self.searchFilesEntry.bind("<KeyRelease>", self.searchFiles)
        
        #end of subframe2 work here

        self.filesController()

    def dynamicFileDetailsController(self, event=None):
        if(self.tempFilesData):
            iid = self.filesTable.selection()[0]
            values = self.filesTable.item(iid, "values")
            index = int(iid)-1

            self.amountApprovedVar.set(self.tempFilesData[index][2])
            self.interestVar.set(self.tempFilesData[index][3])
            self.numOfEmiVar.set(self.tempFilesData[index][7])
            self.loanPeriodVar.set(self.tempFilesData[index][4])
            self.installmentAmtVar.set(self.tempFilesData[index][6])

            self.dateApprovedEntry.config(state='normal')
            self.dateApprovedEntry.set_date(self.tempFilesData[index][9])
            self.dateApprovedEntry.config(state='disabled')

            self.loanPurposeEntry.config(state='normal')
            self.loanPurposeEntry.delete("1.0", "end")
            self.loanPurposeEntry.insert("end", self.tempFilesData[index][8])
            self.loanPurposeEntry.config(state='disabled')
            
            self.statusLabel.config(text="Status: Active" if (self.tempFilesData[index][5]==1) else "Status: Inactive", bg="light green" if (self.tempFilesData[index][5]==1) else "red")

            self.loanTypeLabel.config(text="vehicle loan" if (self.tempFilesData[index][11]=="Loan on vehicles") else "Personal Loan")
            
            self.viewLedgerButton.config(state="normal")
        
        else:
            self.amountApprovedVar.set("")
            self.interestVar.set("")
            self.numOfEmiVar.set("")
            self.loanPeriodVar.set("")
            self.installmentAmtVar.set("")

            self.dateApprovedEntry.config(state='normal')
            self.dateApprovedEntry.set_date("1995-1-1")
            self.dateApprovedEntry.config(state='disabled')

            self.loanPurposeEntry.config(state='normal')
            self.loanPurposeEntry.delete("1.0", "end")
            self.loanPurposeEntry.insert("end", "")
            self.loanPurposeEntry.config(state='disabled')
            
            self.statusLabel.config(text="Status: NULL")

            self.loanTypeLabel.config(text="Loan Type : NULL")
            self.disableAll()
            self.searchFilesEntry.config(state="normal")
            self.refreshButton.config(state="normal")

    def filesController(self):
        self.filesTable.delete(*self.filesTable.get_children())

        self.fileObject = File()
        self.filesData = self.fileObject.readAllData()
            
        if(not self.filesData):
            self.disableAll()
            return None
            
        self.customerObject = Customer()

        lengthOfFiles = len(self.filesData)
        for i in range(lengthOfFiles):
            customerName = self.customerObject.whereData(id=self.filesData[i][1])[0][1]

            self.filesTable.insert(parent="", iid=i+1, index="end", text="", values=(i+1, self.filesData[i][0], self.filesData[i][2], self.filesData[i][9], customerName, self.filesData[i][5]))
        
        self.filesTable.selection_set(1)
        self.searchFiles()

    def disableAll(self):
        self.searchFilesEntry.config(state="disabled")
        self.refreshButton.config(state="disabled")
        self.interestEntry.config(state="disabled")
        self.numOfEmiEntry.config(state="disabled")
        self.loanPeriodEntry.config(state="disabled")
        self.viewLedgerButton.config(state="disabled")
        self.amountApprovedEntry.config(state="disabled")
        self.installmentAmtEntry.config(state="disabled")
        self.loanPurposeEntry.config(state="disabled")
        self.dateApprovedEntry.config(state="disabled")

    def enableAll(self):
        self.searchFilesEntry.config(state="normal")
        self.refreshButton.config(state="normal")
        self.interestEntry.config(state="normal")
        self.numOfEmiEntry.config(state="normal")
        self.loanPeriodEntry.config(state="normal")
        self.viewLedgerButton.config(state="normal")
        self.amountApprovedEntry.config(state="normal")
        self.installmentAmtEntry.config(state="normal")
        self.loanPurposeEntry.config(state="normal")
        self.dateApprovedEntry.config(state="normal")
    
    def searchFiles(self, event=None):
        searchData = self.searchFilesVar.get()
        self.filesTable.delete(*self.filesTable.get_children())
        lengthOfFiles = len(self.filesData)
        if(not searchData):
            self.tempFilesData = self.filesData
            
            for i in range(lengthOfFiles):
                customerName = self.customerObject.whereData(id=self.filesData[i][1])[0][1]
                self.filesTable.insert(parent="", iid=i+1, index="end", text="", values=(i+1, self.filesData[i][0], self.filesData[i][2], self.filesData[i][9], customerName, self.filesData[i][5]))

            self.filesTable.selection_set(1)
            self.dynamicFileDetailsController()  
            return None

        
        self.tempFilesData = []
        count=0
        for i in range(lengthOfFiles):
            customerName = self.customerObject.whereData(id=self.filesData[i][1])[0][1]
            if(searchData in str(self.filesData[i][0]) or searchData in str(self.filesData[i][2]) or searchData in str(self.filesData[i][9]) or searchData.lower() in str(customerName).lower() or searchData in str(self.filesData[i][5])):
                self.filesTable.insert(parent="", iid=count+1, index="end", text="", values=(count+1, self.filesData[i][0], self.filesData[i][2], self.filesData[i][9], customerName, self.filesData[i][5]))
                self.tempFilesData.append(self.filesData[i])
                count+=1

        if(not self.tempFilesData):
            self.tempFilesData = []
            self.dynamicFileDetailsController()
            return None
        
        self.filesTable.selection_set(1)
        self.dynamicFileDetailsController()
        
    def refresh(self):
        self.initialStage()
        self.filesController()

    def initialStage(self):
        self.enableAll()
        self.searchFilesVar.set("")
        self.filesTable.delete(*self.filesTable.get_children())
        self.tempFilesData=[]
        self.dynamicFileDetailsController()



if __name__=="__main__":
    root = Tk()
    root.title("Files List ")
    root.geometry("1000x700")
    files = Files(root)
    root.mainloop()