from sys import path
import os
#adding this path search so that interpreter can search modules and import it from this directory 
path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../config")
from pathConfig import ALLPATHS
path.extend(ALLPATHS)
from pathConfig import CUSTOMERPHOTOPATH, GUARRANTERPHOTOPATH, DEFAULTIMAGEPATH

#profile module shows the whole details and informations related to particular customer and its prvious, ongoing files

#importing necessary modules nad theier components
from tkinter import *
from PIL import Image, ImageTk
from Customer import Customer
from File import File
from Guarranter import Guarranter
from Vehicle import Vehicle
from Ledger import Ledger
from Document import Document
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as message
import shutil
from tkinter import ttk
from tkcalendar import DateEntry


#Profile class takes one tk Window or a Frame and aadharNumber of the particular customer to show it s profile

class Profile:
    def __init__(self, profileWindow, aadharNumber, updateStatus = None):
        #now assinging the value of aadharNumber to self.aadharNumber so that we can use it throughout the class without making it global
        self.aadharNumber = aadharNumber
        self.fileId=None

        #initially assing the function updateStatus if given to self.updateStatus so to use it across the class
        self.updateStatus = updateStatus
        
        #mainFrame holds everything , content of the profile
        mainFrame = Frame(profileWindow, bg="black")
        mainFrame.pack(fill="both", expand=True)

        #configuring rows and columns so to make responsive grid system
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=2)
        # mainFrame.rowconfigure(2, weight=1)
        # mainFrame.rowconfigure(2, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=2)
        # mainFrame.columnconfigure(2, weight=1)
        
        #creting two subframes in mainframe
        subFrame1 = Frame(mainFrame, borderwidth=3, relief="groove", width=100, height=100)
        subFrame1.grid(row=0, column=0, sticky="nsew")
        subFrame1.pack_propagate(False)
        subFrame1.grid_propagate(False)
        # subFrame1.grid_propagate(False)

        subFrame2 = Frame(mainFrame, borderwidth=3, relief="groove", width=100, height=100)
        subFrame2.grid(row=1, column=0, sticky="nsew", rowspan=2)
        subFrame2.pack_propagate(False)
        subFrame2.grid_propagate(False)

        subFrame3 = Frame(mainFrame, borderwidth=3, relief="groove")
        subFrame3.grid(row=0, column=1, sticky="nsew", rowspan=2)

        #subframe1 work starts here
        profileDetailsLabel = Label(subFrame1, text="Profile Details", font="COPPER 20", bg="orange")
        profileDetailsLabel.pack(fill="x")

        self.detailsFrame = Frame(subFrame1, bg="black")
        self.detailsFrame.pack(fill="both", expand=True)

        #getting data relavent to customer with aadharnumber stored in self.aadharNuber
        self.customerObject = Customer()
        self.data = self.customerObject.whereData(aadhar=str(self.aadharNumber))
        self.customerId = self.data[0][0] if(self.data) else None

        #getting files data of customer with customerId = self.customerId
        self.fileObject = File()
        self.filesData = self.fileObject.whereData(customerId=self.customerId)

        #getting guarranter data
        self.guarranterObject = Guarranter()
        self.guarranterdata = None

        #getting vehicle data
        self.vehicleObject = Vehicle()
        self.vehicleData = None

        #getting documente data
        self.documentObject = Document()
        self.documentData = None

        #getting ledger data
        self.ledgerObject = Ledger()
        
        #subframe1 work ends here

        #now invoking detailsConstroller method initiallly
        self.detailsFrameController()

        #subframe2 work starts here

        self.fileScrollY = Scrollbar(subFrame2, orient="vertical")
        self.fileScrollY.pack(side="right", fill='y')

        self.fileScrollX = Scrollbar(subFrame2, orient="horizontal")
        self.fileScrollX.pack(side="bottom", fill='x')
        
        self.filesTable = ttk.Treeview(subFrame2)
        self.filesTable.pack(fill="both", expand=True)

        self.filesTable["columns"]=("s.no", "fileDate", "fileAmount", "loanType", "status")
        self.filesTable.column("#0", width=0, minwidth=0, stretch=False)
        self.filesTable.column("s.no", width=35, minwidth=35, anchor="center", stretch=False)
        self.filesTable.column("fileDate", width=70, minwidth=70, anchor="center")
        self.filesTable.column("fileAmount", width=100, minwidth=100, anchor="center")
        self.filesTable.column("loanType", width=70, minwidth=70, anchor="center")
        self.filesTable.column("status", width=70, minwidth=70, anchor="center")

        self.filesTable.heading("s.no", text="S.No.", anchor="center")
        self.filesTable.heading("fileDate", text="Date", anchor="center")
        self.filesTable.heading("fileAmount", text="File Amount", anchor="center")
        self.filesTable.heading("loanType", text="Loan Type", anchor="center")
        self.filesTable.heading("status", text="Status", anchor="center")

        #configuring and setting scrollbar with filetable
        self.fileScrollY.config(command=self.filesTable.yview)
        self.fileScrollX.config(command=self.filesTable.xview)
        self.filesTable.config(yscrollcommand=self.fileScrollY.set, xscrollcommand=self.fileScrollX.set)

        lengthFile = len(self.filesData)
        for i in range(lengthFile):
            self.filesTable.insert(parent="", text="", iid=i+1, index="end", values=(str(i+1)+".", self.filesData[i][9], self.filesData[i][2], self.filesData[i][11], "active"if (self.filesData[i][5]==1) else 'inactive'))

        self.filesTable.bind("<<TreeviewSelect>>", self.dynamicFileDetailsController)

        if(lengthFile):
            self.filesTable.selection_set(1)

        #subframe 2 work ends here

        #subframe 3 work starts here 
        subFrame3.rowconfigure(0, weight=1)
        subFrame3.rowconfigure(1, weight=1)
        subFrame3.rowconfigure(2, weight=1)
        subFrame3.columnconfigure(0, weight=1)

        self.fileFrame = Frame(subFrame3, borderwidth=2, relief="groove")
        self.fileFrame.grid(row=0, column=0, sticky="nsew")

        self.vehicleFrame = Frame(subFrame3, borderwidth=2, relief="groove")
        self.vehicleFrame.grid(row=1, column=0, sticky="nsew", rowspan=2)

        #work of fileFrame starts here
        self.fileFrame.rowconfigure(0, weight=1)
        self.fileFrame.columnconfigure(0, weight=1)
        self.fileFrame.columnconfigure(1, weight=1)

        self.fileDetailsFrame = Frame(self.fileFrame, border=1, relief="groove", width=100, height=100)
        self.fileDetailsFrame.grid(row=0, column=0, sticky="nsew")
        self.fileDetailsFrame.grid_propagate(False)

        self.documentsFrame = Frame(self.fileFrame, border=1, relief="groove")
        self.documentsFrame.grid(row=0, column=1, sticky="nsew")

        #work of filesDetailsFrame starts here
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

        self.viewLedgerButton = Button(self.fileDetailsFrameInner, text="View Ledger", bg='light green')
        self.viewLedgerButton.grid(row=8, column=0, columnspan=2, sticky="we", pady=2)

        self.deleteFileButton = Button(self.fileDetailsFrameInner, text="Delete File ", bg="red", command=self.deleteFile)
        self.deleteFileButton.grid(row=8, column=2, pady=2, padx=2)

        #fileDetails frame work ends here

        #work of documentsFrame starts here
        self.documentsFrame.config(width=100, height=100)
        self.documentsFrame.grid_propagate(False)
        self.documentsFrame.pack_propagate(False)

        self.documentsFrame.rowconfigure(0, weight=1)
        self.documentsFrame.columnconfigure(0, weight=1)

        self.documentsFrameInner=Frame(self.documentsFrame)
        self.documentsFrameInner.grid(row=0, column=0)

        self.documentsLabel = Label(self.documentsFrameInner, text="Documents", font="COPPER 12 bold")
        self.documentsLabel.grid(row=0, column=0)

        self.docRequireLabel = Label(self.documentsFrameInner, text="Required", font="COPPER 12 bold")
        self.docRequireLabel.grid(row=0, column=1)

        self.docVerifiedLabel = Label(self.documentsFrameInner, text="Verified", font="COPPER 12 bold")
        self.docVerifiedLabel.grid(row=0, column=2)

        self.aadharDocLabel = Label(self.documentsFrameInner, text="Aadhar")
        self.aadharDocLabel.grid(row=1, column=0)

        self.pancardDocLabel = Label(self.documentsFrameInner, text="Pancard")
        self.pancardDocLabel.grid(row=2, column=0)
        
        self.chequeDocLabel = Label(self.documentsFrameInner, text="Cheque")
        self.chequeDocLabel.grid(row=3, column=0)

        self.stampDocLabel = Label(self.documentsFrameInner, text="Stamp")
        self.stampDocLabel.grid(row=4, column=0)

        # self.mobileDocLabel = Label(self.documentsFrameInner, text="Mobile no.")
        # self.mobileDocLabel.grid(row=5, column=0)

        self.rcDocLabel = Label(self.documentsFrameInner, text="RC")
        self.rcDocLabel.grid(row=5, column=0)

        self.aadharReqVar = IntVar()
        self.aadharReqCheck = Checkbutton(self.documentsFrameInner, variable=self.aadharReqVar)
        self.aadharReqCheck.grid(row=1, column=1)

        self.aadharVerifyVar = IntVar()
        self.aadharVerifyCheck = Checkbutton(self.documentsFrameInner, variable=self.aadharVerifyVar)
        self.aadharVerifyCheck.grid(row=1, column=2)

        self.pancardReqVar = IntVar()
        self.pancardReqCheck = Checkbutton(self.documentsFrameInner, variable=self.pancardReqVar)
        self.pancardReqCheck.grid(row=2, column=1)

        self.pancardVerifyVar = IntVar()
        self.pancardVerifyCheck = Checkbutton(self.documentsFrameInner, variable=self.pancardVerifyVar)
        self.pancardVerifyCheck.grid(row=2, column=2)

        self.chequeReqVar = IntVar()
        self.chequeReqCheck = Checkbutton(self.documentsFrameInner, variable=self.chequeReqVar)
        self.chequeReqCheck.grid(row=3, column=1)

        self.chequeVerifyVar = IntVar()
        self.chequeVerifyCheck = Checkbutton(self.documentsFrameInner, variable=self.chequeVerifyVar)
        self.chequeVerifyCheck.grid(row=3, column=2)

        self.stampReqVar = IntVar()
        self.stampReqCheck = Checkbutton(self.documentsFrameInner, variable=self.stampReqVar)
        self.stampReqCheck.grid(row=4, column=1)

        self.stampVerifyVar = IntVar()
        self.stampVerifyCheck = Checkbutton(self.documentsFrameInner, variable=self.stampVerifyVar)
        self.stampVerifyCheck.grid(row=4, column=2)

        # self.mobileReqVar = IntVar()
        # self.mobileReqCheck = Checkbutton(self.documentsFrameInner, variable=self.mobileReqVar)
        # self.mobileReqCheck.grid(row=5, column=1)

        # self.mobileVerifyVar = IntVar()
        # self.mobileVerifyCheck = Checkbutton(self.documentsFrameInner, variable=self.mobileVerifyVar)
        # self.mobileVerifyCheck.grid(row=5, column=2)

        self.rcReqVar = IntVar()
        self.rcReqCheck = Checkbutton(self.documentsFrameInner, variable=self.rcReqVar)
        self.rcReqCheck.grid(row=5, column=1)

        self.rcVerifyVar = IntVar()
        self.rcVerifyCheck = Checkbutton(self.documentsFrameInner, variable=self.rcVerifyVar)
        self.rcVerifyCheck.grid(row=5, column=2)

        self.editDocumentsButton = Button(self.documentsFrameInner, text=' Edit ', command=self.enableDocument)
        self.editDocumentsButton.grid(row=7, column=0, sticky="ew")

        self.cancelDocumentsButton = Button(self.documentsFrameInner, text=' Cancel ', command=self.documentDetailsController)
        self.cancelDocumentsButton.grid(row=7, column=1, sticky="ew")

        self.saveDocumentsButton = Button(self.documentsFrameInner, text=' Save ', command=self.saveDocument)
        self.saveDocumentsButton.grid(row=7, column=2, sticky="ew")

        #documentFrame work ends here

        #fileFrame work ends here

        #vehicle Frame work start here
        self.vehicleFrame.rowconfigure(0, weight=1)
        self.vehicleFrame.columnconfigure(0, weight=1)
        self.vehicleFrame.columnconfigure(1, weight=1)

        self.vehicleDetailsFrame = Frame(self.vehicleFrame, borderwidth=1, relief="groove", width=100, height=100)
        self.vehicleDetailsFrame.grid(row=0, column=0, sticky="nsew")
        self.vehicleDetailsFrame.grid_propagate(False)
        self.vehicleDetailsFrame.pack_propagate(False)

        self.guarranterDetailsFrame = Frame(self.vehicleFrame, borderwidth=1, relief="groove", width=100, height=100)
        self.guarranterDetailsFrame.grid(row=0, column=1, sticky="nsew")
        self.guarranterDetailsFrame.grid_propagate(False)
        self.guarranterDetailsFrame.pack_propagate(False)

        #vehicleDetailsFrame work start here
        self.vehicleDetailsFrame.rowconfigure(0, weight=1)
        self.vehicleDetailsFrame.columnconfigure(0, weight=1)

        self.vehicleDetailsFrameInner = Frame(self.vehicleDetailsFrame)
        self.vehicleDetailsFrameInner.grid(row=0, column=0)

        self.vNameLable = Label(self.vehicleDetailsFrameInner, text="Vehicle Name : ", font="COPPER 7 bold", justify="right")
        self.vNameLable.grid(row=0, column=0)

        self.modelLabel = Label(self.vehicleDetailsFrameInner, text="Model : ", font="COPPER 7 bold", justify="right")
        self.modelLabel.grid(row=1, column=0)

        self.manufaturerLabel = Label(self.vehicleDetailsFrameInner, text="Manufact : ", font="COPPER 7 bold", justify="right")
        self.manufaturerLabel.grid(row=2, column=0)

        self.fuelUsedLabel = Label(self.vehicleDetailsFrameInner, text="Fuel: ", font="COPPER 7 bold", justify="right")
        self.fuelUsedLabel.grid(row=3, column=0)

        self.engineCCLabel = Label(self.vehicleDetailsFrameInner, text="Engine(CC) : ", font="COPPER 7 bold", justify="right")
        self.engineCCLabel.grid(row=4, column=0)

        self.horsePowerLabel = Label(self.vehicleDetailsFrameInner, text="Horse Pow(bhp) : ", font="COPPER 7 bold", justify="right")
        self.horsePowerLabel.grid(row=5, column=0)

        self.numCyilendersLabel = Label(self.vehicleDetailsFrameInner, text="Cyilenders : ", font="COPPER 7 bold", justify="right")
        self.numCyilendersLabel.grid(row=0, column=2, padx=10)

        self.fuelCapacityLabel = Label(self.vehicleDetailsFrameInner, text="Fuel Capac(l) : ", font="COPPER 7 bold", justify="right")
        self.fuelCapacityLabel.grid(row=1, column=2)

        self.seatingCapacityLabel = Label(self.vehicleDetailsFrameInner, text="Seats : ", font="COPPER 7 bold", justify="right")
        self.seatingCapacityLabel.grid(row=2, column=2)

        self.vehicleWeightLabel = Label(self.vehicleDetailsFrameInner, text="Weight(Kg) : ", font="COPPER 7 bold", justify="right")
        self.vehicleWeightLabel.grid(row=3, column=2)

        self.numberPlateLabel = Label(self.vehicleDetailsFrameInner, text="Number plate : ", font="COPPER 7 bold", justify="right")
        self.numberPlateLabel.grid(row=4, column=2)

        self.vNameVar = StringVar()
        self.vNameEntry = Entry(self.vehicleDetailsFrameInner, textvariable=self.vNameVar, width=10, justify="center")
        self.vNameEntry.grid(row=0, column=1, pady=10)

        self.modelVar = StringVar()
        self.modelEntry = Entry(self.vehicleDetailsFrameInner, textvariable=self.modelVar, width=10, justify="center")
        self.modelEntry.grid(row=1, column=1, pady=10)

        self.manufacturerVar = StringVar()
        self.manufacturerEntry = ttk.Combobox(self.vehicleDetailsFrameInner, state="readonly", values=["Hero", "Honda", "Suzuki"], textvariable=self.manufacturerVar, width=7, justify="center")
        self.manufacturerEntry.grid(row=2, column=1, pady=10)

        self.fuelUsedVar = StringVar()
        self.fuelUsedEntry = ttk.Combobox(self.vehicleDetailsFrameInner, state="readonly", values=["Petrol", "Diesel"], textvariable=self.fuelUsedVar, width=7, justify="center")
        self.fuelUsedEntry.grid(row=3, column=1, pady=10)

        self.engineCCVar = StringVar()
        self.engineCCEntry = Entry(self.vehicleDetailsFrameInner, textvariable=self.engineCCVar, width=10, justify="center")
        self.engineCCEntry.grid(row=4, column=1, pady=10)

        self.horsePowerVar = StringVar()
        self.horsePowerEntry = Entry(self.vehicleDetailsFrameInner, textvariable=self.horsePowerVar, width=10, justify="center")
        self.horsePowerEntry.grid(row=5, column=1, pady=10)

        self.numCyilendersVar = StringVar()
        self.numCyilendersEntry = Entry(self.vehicleDetailsFrameInner, textvariable=self.numCyilendersVar, width=10, justify="center")
        self.numCyilendersEntry.grid(row=0, column=3, pady=10)

        self.fuelCapacityVar = StringVar()
        self.fuelCapacityEntry = Entry(self.vehicleDetailsFrameInner, textvariable=self.fuelCapacityVar, width=10, justify="center")
        self.fuelCapacityEntry.grid(row=1, column=3, pady=10)

        self.seatingCapacityVar = StringVar()
        self.seatingCapacityEntry = Entry(self.vehicleDetailsFrameInner, textvariable=self.seatingCapacityVar, width=10, justify="center")
        self.seatingCapacityEntry.grid(row=2, column=3, pady=10)

        self.vehicleWeightVar = StringVar()
        self.vehicleWeightEntry = Entry(self.vehicleDetailsFrameInner, textvariable=self.vehicleWeightVar, width=10, justify="center")
        self.vehicleWeightEntry.grid(row=3, column=3, pady=10)

        self.numberPlateVar = StringVar()
        self.numberPlateEntry = Entry(self.vehicleDetailsFrameInner, textvariable=self.numberPlateVar, width=10, justify="center")
        self.numberPlateEntry.grid(row=4, column=3, pady=10)

        self.editVehicleButton=Button(self.vehicleDetailsFrameInner, text="edit", bg="orange", command=self.enableVehicleDetails)
        self.editVehicleButton.grid(row=6, column=0, pady=5, sticky="ew")

        self.cancelVehicleButton=Button(self.vehicleDetailsFrameInner, text="cancel", state="disabled", command=self.disableVehicleDetails)
        self.cancelVehicleButton.grid(row=6, column=1, pady=5, sticky="ew")

        self.saveVehicleButton=Button(self.vehicleDetailsFrameInner, text="save", bg="orange", state="disabled", command=self.saveVehicleDetails)
        self.saveVehicleButton.grid(row=6, column=2, pady=5, sticky="ew")
        self.guarranterDetailsFrameController()
        self.vehicleDetailsFrameController()
        self.filePageController()
        self.documentDetailsController()
        #work of vehicledetailsframe ends here

        #work of guarranterframe starts here 

    
        
    def enableDocument(self):
        self.aadharReqCheck.config(state="normal")
        self.aadharVerifyCheck.config(state="normal")
        self.pancardReqCheck.config(state="normal")
        self.pancardVerifyCheck.config(state="normal")
        self.chequeReqCheck.config(state="normal")
        self.chequeVerifyCheck.config(state="normal")
        self.stampReqCheck.config(state="normal")
        self.stampVerifyCheck.config(state="normal")   
        self.rcReqCheck.config(state="normal")
        self.rcVerifyCheck.config(state="normal")
        self.editDocumentsButton.config(state="disabled")
        self.cancelDocumentsButton.config(state="normal")
        self.saveDocumentsButton.config(state="normal")

    def saveDocument(self):
        sure = message.askyesno("Are you sure ?", "Are you sure to overwrite \nthe document details ?")
        if(sure):
            for item in self.documentData:
                if("aadhar" in item):
                    self.documentObject.updateData(id=item[0], required=int(self.aadharReqVar.get()), verified=int(self.aadharVerifyVar.get()))

                if("pancard" in item):
                    self.documentObject.updateData(id=item[0], required=int(self.pancardReqVar.get()), verified=int(self.pancardVerifyVar.get()))

                if("cheque" in item):
                    self.documentObject.updateData(id=item[0], required=int(self.chequeReqVar.get()), verified=int(self.chequeVerifyVar.get()))

                if("stamp" in item):
                    self.documentObject.updateData(id=item[0], required=int(self.stampReqVar.get()), verified=int(self.stampVerifyVar.get()))

                if("rc" in item):
                    self.documentObject.updateData(id=item[0], required=int(self.rcReqVar.get()), verified=int(self.rcVerifyVar.get()))

            self.documentDetailsController()   

    def documentDetailsController(self):
        self.documentData = self.documentObject.whereData(file_Id=self.fileId)
        print(self.documentData)
        for item in self.documentData:

            if("aadhar" in item):
                self.aadharReqVar.set(item[7])
                self.aadharVerifyVar.set(item[8])
                
            if("pancard" in item):
                self.pancardReqVar.set(item[7])
                self.pancardVerifyVar.set(item[8])
                
            if("cheque" in item):
                self.chequeReqVar.set(item[7])
                self.chequeVerifyVar.set(item[8])
                
            if("stamp" in item):
                self.stampReqVar.set(item[7])
                self.stampVerifyVar.set(item[8])
                
            if("rc" in item):
                self.rcReqVar.set(item[7])
                self.rcVerifyVar.set(item[8])

        if(not self.documentData):
            self.aadharReqVar.set(0)
            self.aadharVerifyVar.set(0)
            self.stampReqVar.set(0)
            self.stampVerifyVar.set(0)
            self.rcReqVar.set(0)
            self.rcVerifyVar.set(0)
            self.chequeReqVar.set(0)
            self.chequeVerifyVar.set(0)
            self.pancardReqVar.set(0)
            self.pancardVerifyVar.set(0)
            
        self.disableDocument()       
        self.editDocumentsButton.config(state="normal")if(self.customerId and self.fileId)else self.editDocumentsButton.config(state="disabled")
        self.cancelDocumentsButton.config(state="disabled")
        self.saveDocumentsButton.config(state="disabled")

    def disableDocument(self):
        self.aadharReqCheck.config(state="disable")
        self.aadharVerifyCheck.config(state="disable")
        self.rcReqCheck.config(state="disable")
        self.rcVerifyCheck.config(state="disable")
        self.stampReqCheck.config(state="disable")
        self.stampVerifyCheck.config(state="disable")
        self.chequeReqCheck.config(state="disable")
        self.chequeVerifyCheck.config(state="disable")
        self.pancardReqCheck.config(state="disable")
        self.pancardVerifyCheck.config(state="disable")
    
    def refresh(self):
        self.filesData = self.fileObject.whereData(customerId=self.customerId)
        self.filesTable.delete(*self.filesTable.get_children())
        lengthFile = len(self.filesData)
        for i in range(lengthFile):
            self.filesTable.insert(parent="", text="", iid=i+1, index="end", values=(str(i+1)+".", self.filesData[i][9], self.filesData[i][2], self.filesData[i][11], "active"if (self.filesData[i][5]==1) else 'inactive'))
        
        self.guarranterDetailsFrameController()
        self.vehicleDetailsFrameController()
        self.filePageController()
        self.documentDetailsController()


    def guarranterDetailsFrameController(self):
        
        #first things is to delete all the widgets present in self.detailsFrame
        children  = self.guarranterDetailsFrame.winfo_children()

        for child in children:
            child.destroy()

        self.customerId = self.customerObject.whereData(aadhar=self.aadharEntryVar.get())[0][0]if(self.customerObject.whereData(aadhar=self.aadharEntryVar.get())) else None
        self.dateApproved = self.filesTable.item(self.filesTable.selection()[0], "values")[1]if(self.filesData) else "1000-12-1"
        
        self.guarranterId = self.fileObject.whereData(customerId=self.customerId, dateApproved=self.dateApproved)[0][10] if self.fileObject.whereData(customerId=self.customerId, dateApproved=self.dateApproved) else None
        self.guarranterdata = self.guarranterObject.whereData(id=self.guarranterId)

        self.fileId = self.fileObject.whereData(customerId=self.customerId, dateApproved=self.dateApproved)[0][0] if self.fileObject.whereData(customerId=self.customerId, dateApproved=self.dateApproved) else None

        if(self.guarranterdata):
            #extracting data from self.data property of object which was defined in __init__ method
            guarranterdata = {"name":self.guarranterdata[0][2], "aadhar":self.guarranterdata[0][7], "mobile":self.guarranterdata[0][4], "father":self.guarranterdata[0][3], "homeAddress":self.guarranterdata[0][5], "workAddress":self.guarranterdata[0][6]}

        else:
            #if self.data is empty then default value of customerData is created
            guarranterdata = {"name":"", "aadhar":"", "mobile":"", "father":"", "homeAddress":"", "workAddress":""}

        self.guarranterDetailsFrame.rowconfigure(0, weight=1)
        self.guarranterDetailsFrame.columnconfigure(0, weight=1)

        self.guarranterDetailsFrameInner = Frame(self.guarranterDetailsFrame)
        self.guarranterDetailsFrameInner.grid(row=0, column=0)
                
        #creating two frames PhotoFrame and Details inside self.customerDetailsFrame
        PhotoFrame = Frame(self.guarranterDetailsFrameInner, relief="groove", border=3)
        PhotoFrame.grid(row=0, column=0, sticky="nsew")

        Details = Frame(self.guarranterDetailsFrameInner, relief="groove", border=3)
        Details.grid(row=0, column=1, sticky="nsew")

        #creating responsive PhotoFrame
        PhotoFrame.rowconfigure(0, weight=1)
        PhotoFrame.columnconfigure(0, weight=1)

        #creating a PIL image object
            
        #if error found during imaging loading then use default image
        #now integrating the image into label widget and positioning it via grid 
        self.guarranterPhotoLabel = Label(PhotoFrame)
        self.guarranterPhotoLabel.grid(row=0, column=0)
        try:
            if(self.guarranterId):
                self.guarranterphotoPath = f"{GUARRANTERPHOTOPATH}/{self.guarranterId}.jpg"
                img=Image.open(self.guarranterphotoPath)
                
                #resizing the image
                img=img.resize((82,120))

                #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
                self.guarranterPhoto = ImageTk.PhotoImage(img)
                self.guarranterPhotoLabel.config(image=self.guarranterPhoto)
            else:
                self.guarranterphotoPath = f"{DEFAULTIMAGEPATH}/user.jpg"
                img=Image.open(self.guarranterphotoPath)
                
                #resizing the image
                img=img.resize((82,120))

                #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
                self.guarranterPhoto = ImageTk.PhotoImage(img)
                self.guarranterPhotoLabel.config(image=self.guarranterPhoto)
        except:
            self.guarranterphotoPath = f"{DEFAULTIMAGEPATH}/user.jpg"
            img=Image.open(self.guarranterphotoPath)
            
            #resizing the image
            img=img.resize((82,120))

            #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
            self.guarranterPhoto = ImageTk.PhotoImage(img)
            self.guarranterPhotoLabel.config(image=self.guarranterPhoto)
            
        finally:
            self.guarranterdataphotoPath = None

        #creating responsive sec3Details frame
        Details.rowconfigure(0, weight=1)
        Details.columnconfigure(0, weight=1)
            
        #creating a inner subFramee detailsInnerFrame inside sec3details
        detailsInnerFrame = Frame(Details)
        detailsInnerFrame.grid(row=0, column=0)

        #creating labels static
        guarranterNameLabel = Label(detailsInnerFrame, text="Name : ")
        guarranterNameLabel.grid(row=0, column=0)

        aadharLabel = Label(detailsInnerFrame, text="Aadhar : ")
        aadharLabel.grid(row=1, column=0)

        mobileLabel = Label(detailsInnerFrame, text="Mobile : ")
        mobileLabel.grid(row=2, column=0)

        fatherLabel = Label(detailsInnerFrame, text="Father : ")
        fatherLabel.grid(row=3, column=0)

        homeAddressLabel = Label(detailsInnerFrame, text="Home Address : ")
        homeAddressLabel.grid(row=4, column=0)

        workAddressLabel = Label(detailsInnerFrame, text="Work Address : ")
        workAddressLabel.grid(row=5, column=0)

        #creating labels dynamic
        self.guarranterEntryVar = StringVar()
        self.guarranterEntryVar.set(guarranterdata["name"])
        guarranterEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.guarranterEntryVar)
        guarranterEntry.grid(row=0, column=1)

        self.guarranterAadharEntryVar = StringVar()
        self.guarranterAadharEntryVar.set(guarranterdata["aadhar"])
        self.guarranterAadharEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.guarranterAadharEntryVar)
        self.guarranterAadharEntry.grid(row=1, column=1)

        #event handler for aadhar entry to restrict user from entering more than 12 digits or letters, character
        def guarranterAadharEntryEventHandler(event):
            tempString = ""
            for char in self.aadharEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char
            
            if(len(tempString)>12):
                tempString = tempString[0:12]
                self.guarranterAadharEntry.delete(0, "end")
                self.guarranterAadharEntry.insert("end", tempString)
            else:
                self.aadharEntry.delete(0, "end")
                self.aadharEntry.insert("end", tempString)

        self.guarranterAadharEntry.bind("<KeyRelease>", guarranterAadharEntryEventHandler)

        self.guarranterMobileEntryVar = StringVar()
        self.guarranterMobileEntryVar.set(guarranterdata["mobile"])
        self.guarranterMobileEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.guarranterMobileEntryVar)
        self.guarranterMobileEntry.grid(row=2, column=1)

         #event handler for mobile entry to restrict user from entering more than 12 digits or letters, character
        def guarranterMobileEntryEventHandler(event):
            tempString = ""
            for char in self.mobileEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char
            
            if(len(tempString)>10):
                tempString = tempString[0:10]
                self.guarranterMobileEntry.delete(0, "end")
                self.guarranterMobileEntry.insert("end", tempString)
            else:
                self.guarranterMobileEntry.delete(0, "end")
                self.guarranterMobileEntry.insert("end", tempString)

        self.guarranterMobileEntry.bind("<KeyRelease>", guarranterMobileEntryEventHandler)

        self.guarranterFatherEntryVar = StringVar()
        self.guarranterFatherEntryVar.set(guarranterdata["father"])
        guarranterFatherEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.guarranterFatherEntryVar)
        guarranterFatherEntry.grid(row=3, column=1)

        self.guarranterHomeAddressEntryVar = StringVar()
        self.guarranterHomeAddressEntryVar.set(guarranterdata["homeAddress"])
        guarranterHomeAddressEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.guarranterHomeAddressEntryVar)
        guarranterHomeAddressEntry.grid(row=4, column=1)

        self.guarranterWorkAddressEntryVar = StringVar()
        self.guarranterWorkAddressEntryVar.set(guarranterdata["workAddress"])
        guarranterWorkAddressEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.guarranterWorkAddressEntryVar)
        guarranterWorkAddressEntry.grid(row=5, column=1)

        # state of entries depends of emptiness of self.data
        state = ("normal")if(self.guarranterdata) else ("disable")

        #addign sll entries inside a list
        entryList = [guarranterWorkAddressEntry, guarranterFatherEntry, guarranterEntry, guarranterHomeAddressEntry, self.guarranterMobileEntry, self.guarranterAadharEntry]
            
        #operation frame
        self.guarranterOperationFrame = Frame(self.guarranterDetailsFrameInner, bg="red")
        self.guarranterOperationFrame.grid(row=1, column=0, columnspan=2, sticky="we")

        #configuring grid area
        self.guarranterOperationFrame.rowconfigure(0, weight=1)
        for i in range(4):
            self.guarranterOperationFrame.columnconfigure(i, weight=1)

        #This button allows user to interact with entries and edit them
        editButton = Button(self.guarranterDetailsFrameInner, text="Edit", state=state, bg="orange")
        editButton.grid(row=1, column=0, columnspan=2, sticky="nsew")

        #configuring commmand for editButton as self.edit()
        editButton.config(command=lambda entryList=entryList, editButton=editButton: self.editGuarranter(entryList, editButton))

    
    #thsi edite function changes state of entries to normal and allows user to edit them and save them
    def editGuarranter(self, entryList, editButton):
        #changing state to normal
        for entry in entryList:
            entry.config(state="normal")
        editButton.destroy()

        #opens a filedialog box to select replacement image of client
        changePhotoButton = Button(self.guarranterOperationFrame, text="change", command=self.changePhotoGuarranter)
        changePhotoButton.grid(row=0, column=0, sticky="we")

        #cancelButton to exit from edit mode and go to read mode
        cancelButton = Button(self.guarranterOperationFrame, text="Cancel", command=self.guarranterDetailsFrameController)
        cancelButton.grid(row=0, column=1, sticky="ew")

        #saves the changes made in edit mode by user
        saveButton = Button(self.guarranterOperationFrame, text="Save", command=self.saveGuarranter)
        saveButton.grid(row=0, column=2, sticky="we")

        #deletes the customer ,but not its relations with files
        deleteButton = Button(self.guarranterOperationFrame, text="Delete", bg="red")
        deleteButton.grid(row=0, column=3, sticky="we") 
    
    def changePhotoGuarranter(self):
            self.guarranterphotoPath = askopenfilename(title="Select Guarranter's Photo", initialdir="/",filetypes=(("PNG", "*.png"),("JPG", "jpg")), multiple=False)
            #if self.photoPath is not empty then only it will proceed
            if(self.guarranterphotoPath):
                #creating a PIL image object
                img=Image.open(self.guarranterphotoPath)
                #resizing the image
                img=img.resize((82,120))

                #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
                self.guarranterPhoto = ImageTk.PhotoImage(img)

                self.guarranterPhotoLabel.config(image=self.guarranterPhoto)
            else:
                self.guarranterphotoPath= None
    
    #this functions saves the changes made by user in edit mode and save it to the database
    def saveGuarranter(self):
        #checking if the fields are filled properly
        if((not self.guarranterEntryVar.get())):
            requirementsFilled=False
            instructionText = "Please fill Guarranter's Name Field"
        elif(((not self.guarranterAadharEntryVar.get().isdigit()) or (len(self.guarranterAadharEntryVar.get())!=12))):
            requirementsFilled=False
            instructionText = "Please Fill Right Format of Aadhar"
        elif((not self.guarranterMobileEntryVar.get().isdigit()) or (len(self.guarranterMobileEntryVar.get())!=10)):
            requirementsFilled=False
            instructionText = "Please Fill Right Format of Mobile"
        elif((not self.guarranterFatherEntryVar.get())):
            requirementsFilled=False
            instructionText = "Please fill Father's Name Field"
        elif((not self.guarranterHomeAddressEntryVar.get())):
            requirementsFilled=False
            instructionText = "Please fill Home Address Field"
        elif((not self.guarranterWorkAddressEntryVar.get())):
            requirementsFilled=False
            instructionText = "Please fill work address Field"
        else:
            requirementsFilled=True
            instructionText = ""

        if(requirementsFilled):
            #asking if user wants to really save changes
            if(message.askyesno("Save Changes", "Do you want save the changes ?")):
                #updating customer data by takin customer id as reference 
                self.guarranterObject.updateData(id=self.guarranterId, name=self.guarranterEntryVar.get(), father=self.guarranterFatherEntryVar.get(), mobile=self.guarranterMobileEntryVar.get(), home_address=self.guarranterHomeAddressEntryVar.get(), work_address=self.guarranterWorkAddressEntryVar.get(), aadhar=self.guarranterAadharEntryVar.get())

                #if self.photopath is defined then copying image to the customerPhoto, it will replace the previous image with same name
                try:
                    if(self.guarranterphotoPath):
                        shutil.copy(self.guarranterphotoPath, f"{GUARRANTERPHOTOPATH}/{self.guarranterdata[0][0]}.jpg")
                        self.guarranterphotoPath=None
                except:
                    self.guarranterphotoPath=None
                #updating self.data 
                self.guarranterdata = self.guarranterObject.whereData(id=self.guarranterId)

                #now calling detailsFrameController to show new customerDetails in readmode
                self.guarranterDetailsFrameController()
                
        else:
            message.showerror("Error", instructionText)

    #vehicledetailsFrameController
    def enableVehicleDetails(self):
        self.vNameEntry.config(state="normal")
        self.numberPlateEntry.config(state="normal")
        self.vehicleWeightEntry.config(state="normal")
        self.seatingCapacityEntry.config(state="normal")
        self.fuelCapacityEntry.config(state="normal")
        self.numCyilendersEntry.config(state="normal")
        self.horsePowerEntry.config(state="normal")
        self.engineCCEntry.config(state="normal")
        self.fuelUsedEntry.config(state="normal")
        self.manufacturerEntry.config(state="normal")
        self.modelEntry.config(state="normal")
        self.cancelVehicleButton.config(state="normal")
        self.saveVehicleButton.config(state="normal")
        self.editVehicleButton.config(state="disabled")
    
    def disableVehicleDetails(self):
        self.vNameEntry.config(state="disabled")
        self.numberPlateEntry.config(state="disabled")
        self.vehicleWeightEntry.config(state="disabled")
        self.seatingCapacityEntry.config(state="disabled")
        self.fuelCapacityEntry.config(state="disabled")
        self.numCyilendersEntry.config(state="disabled")
        self.horsePowerEntry.config(state="disabled")
        self.engineCCEntry.config(state="disabled")
        self.fuelUsedEntry.config(state="disabled")
        self.manufacturerEntry.config(state="disabled")
        self.modelEntry.config(state="disabled")
        self.editVehicleButton.config(state="normal")
        self.cancelVehicleButton.config(state="disabled")
        self.saveVehicleButton.config(state="disabled")

    def vehicleDetailsFrameController(self):
        self.vehicleData = self.vehicleObject.whereData(fileId=self.fileId)
        self.enableVehicleDetails()

        if(self.vehicleData):
            self.vNameVar.set(self.vehicleData[0][2])
            self.numberPlateVar.set(self.vehicleData[0][3])
            self.vehicleWeightVar.set(self.vehicleData[0][13])
            self.seatingCapacityVar.set(self.vehicleData[0][12])
            self.fuelCapacityVar.set(self.vehicleData[0][11])
            self.numCyilendersVar.set(self.vehicleData[0][10])
            self.horsePowerVar.set(self.vehicleData[0][9])
            self.engineCCVar.set(self.vehicleData[0][8])
            self.fuelUsedVar.set(self.vehicleData[0][7])
            self.manufacturerVar.set(self.vehicleData[0][5])
            self.modelVar.set(self.vehicleData[0][4])
            self.disableVehicleDetails()
        else:
            self.vNameVar.set("")
            self.numberPlateVar.set("")
            self.vehicleWeightVar.set("")
            self.seatingCapacityVar.set("")
            self.fuelCapacityVar.set("")
            self.numCyilendersVar.set("")
            self.horsePowerVar.set("")
            self.engineCCVar.set("")
            self.fuelUsedVar.set("")
            self.manufacturerVar.set("")
            self.modelVar.set("")
            self.disableVehicleDetails()
            self.editVehicleButton.config(state="disabled")
            self.cancelVehicleButton.config(state="disabled")
            self.saveVehicleButton.config(state="disabled")

    def saveVehicleDetails(self):
        sure = message.askyesno("Are you sure ?", "Are you sure to change\n vehicle details")
        if(sure):
            vehicleId = self.vehicleData[0][0]
            self.vehicleObject.updateData(id=vehicleId, name=self.vNameVar.get(), plateNum=self.numberPlateVar.get(),model=self.modelVar.get(), manufacturer=self.manufacturerVar.get(), fuel=self.fuelUsedVar.get(), engineCC=self.engineCCVar.get(), horsePowerBHP=self.horsePowerVar.get(), cyilenders=self.numCyilendersVar.get() ,fuelCapacity=self.fuelCapacityVar.get() ,seatingCapacity=self.seatingCapacityVar.get(), vehicleWeightKG=self.vehicleWeightVar.get())
            
            self.vehicleDetailsFrameController()

    def filePageController(self):
        fileInfo = self.filesData[int(self.filesTable.selection()[0])-1]if(self.filesData) else None
        if(fileInfo):
            self.fileId = self.filesData[int(self.filesTable.selection()[0])-1][0]
            self.statusLabel.config(text="Status : Active" if(fileInfo[5]==1) else "Status : Inactive", bg="light green"if(fileInfo[5]==1) else "red")
            self.loanTypeLabel.config(text="Loan Type : Loan on vehicle" if(fileInfo[11]=="Loan on vehicles") else "Loan Type : Personal Loan")
            self.amountApprovedVar.set(fileInfo[2])
            self.interestVar.set(fileInfo[3])
            self.numOfEmiVar.set(fileInfo[7])
            self.loanPeriodVar.set(fileInfo[4])
            self.installmentAmtVar.set(fileInfo[6])
            self.dateApprovedEntry.config(state="normal")
            self.dateApprovedEntry.set_date(fileInfo[9])
            self.dateApprovedEntry.config(state="disable")
            self.loanPurposeEntry.config(state="normal")
            self.loanPurposeEntry.delete("1.0", "end")
            self.loanPurposeEntry.insert("end", fileInfo[8])

            self.viewLedgerButton.config(state="normal")
            self.deleteFileButton.config(state="normal")
            # self.loanPurposeEntry.config(state="disable")
        else:
            self.statusLabel.config(text="Status : NULL")
            self.loanTypeLabel.config(text="Loan Type : NULL")
            self.amountApprovedVar.set("")
            self.interestVar.set("")
            self.numOfEmiVar.set("")
            self.loanPeriodVar.set("")
            self.installmentAmtVar.set("")
            self.dateApprovedEntry.config(state="disable")
            self.loanPurposeEntry.config(state="normal")
            self.loanPurposeEntry.delete("1.0", "end")
            self.loanPurposeEntry.insert("end", "")
            self.viewLedgerButton.config(state="disable")
            self.deleteFileButton.config(state="disable")
    
    def deleteFile(self):
        sure = message.askyesno("Are you sure ?", "Are you sure about deleting this \nfile. All data related to this file \nwill be deleted like vehicle details, ledger\n and guarranter details ? ")
        
        if(sure):
            #ask password code
            message.showwarning("Warning", "The file will be deleted\n permanently.")
            fileDeleted = self.fileObject.deleteRow(id=self.fileId) if (self.fileId) else None
            if(fileDeleted):
                self.vehicleObject.deleteRow(id=self.vehicleData[0][0]) if (self.vehicleData) else None
                self.guarranterObject.deleteRow(id=self.guarranterId) if (self.guarranterId) else None
                ledgerData = self.ledgerObject.whereData(fileId=self.fileId)
                print(ledgerData)
                for i in range(len(ledgerData)):
                    self.ledgerObject.deleteRow(id=ledgerData[i][0])
                
                self.filePageController()
                self.refresh()
            else:
                message.showerror("Error","file didn't delete successfully.")
                self.refresh()

    def dynamicFileDetailsController(self, event):
        self.filePageController()
        self.documentDetailsController()

    def detailsFrameController(self):

        #first things is to delete all the widgets present in self.detailsFrame
        children  = self.detailsFrame.winfo_children()

        for child in children:
            child.destroy()

        if(self.data):
            #extracting data from self.data property of object which was defined in __init__ method
            customerData = {"name":self.data[0][1], "aadhar":self.data[0][6], "mobile":self.data[0][3], "father":self.data[0][2], "homeAddress":self.data[0][4], "workAddress":self.data[0][5]}

        else:
            #if self.data is empty then default value of customerData is created
            customerData = {"name":"", "aadhar":"", "mobile":"", "father":"", "homeAddress":"", "workAddress":""}

        self.detailsFrame.rowconfigure(0, weight=1)
        self.detailsFrame.columnconfigure(0, weight=1)

        self.customerDetailsFrame = Frame(self.detailsFrame)
        self.customerDetailsFrame.grid(row=0, column=0)
                
        #creating two frames PhotoFrame and Details inside self.customerDetailsFrame
        PhotoFrame = Frame(self.customerDetailsFrame, relief="groove", border=3)
        PhotoFrame.grid(row=0, column=0, sticky="nsew")

        Details = Frame(self.customerDetailsFrame, relief="groove", border=3)
        Details.grid(row=0, column=1, sticky="nsew")

        #creating responsive PhotoFrame
        PhotoFrame.rowconfigure(0, weight=1)
        PhotoFrame.columnconfigure(0, weight=1)

        #creating a PIL image object
            
        #if error found during imaging loading then use default image
        #now integrating the image into label widget and positioning it via grid 
        self.customerPhotoLabel = Label(PhotoFrame)
        self.customerPhotoLabel.grid(row=0, column=0)
        try:
            self.photoPath = f"{CUSTOMERPHOTOPATH}/{self.data[0][0]}.jpg"
            img=Image.open(self.photoPath)
            
            #resizing the image
            img=img.resize((82,120))

            #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
            self.customerPhoto = ImageTk.PhotoImage(img)
            self.customerPhotoLabel.config(image=self.customerPhoto)
        except:
            self.photoPath = f"{DEFAULTIMAGEPATH}/user.jpg"
            img=Image.open(self.photoPath)
            
            #resizing the image
            img=img.resize((82,120))

            #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
            self.customerPhoto = ImageTk.PhotoImage(img)
            self.customerPhotoLabel.config(image=self.customerPhoto)
            
        finally:
            self.photoPath = None

        #creating responsive sec3Details frame
        Details.rowconfigure(0, weight=1)
        Details.columnconfigure(0, weight=1)
            
        #creating a inner subFramee detailsInnerFrame inside sec3details
        detailsInnerFrame = Frame(Details)
        detailsInnerFrame.grid(row=0, column=0)

        #creating labels static
        customerNameLabel = Label(detailsInnerFrame, text="Name : ")
        customerNameLabel.grid(row=0, column=0)

        aadharLabel = Label(detailsInnerFrame, text="Aadhar : ")
        aadharLabel.grid(row=1, column=0)

        mobileLabel = Label(detailsInnerFrame, text="Mobile : ")
        mobileLabel.grid(row=2, column=0)

        fatherLabel = Label(detailsInnerFrame, text="Father : ")
        fatherLabel.grid(row=3, column=0)

        homeAddressLabel = Label(detailsInnerFrame, text="Home Address : ")
        homeAddressLabel.grid(row=4, column=0)

        workAddressLabel = Label(detailsInnerFrame, text="Work Address : ")
        workAddressLabel.grid(row=5, column=0)

        #creating labels dynamic
        self.customerEntryVar = StringVar()
        self.customerEntryVar.set(customerData["name"])
        customerEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.customerEntryVar)
        customerEntry.grid(row=0, column=1)

        self.aadharEntryVar = StringVar()
        self.aadharEntryVar.set(customerData["aadhar"])
        self.aadharEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.aadharEntryVar)
        self.aadharEntry.grid(row=1, column=1)

        #event handler for aadhar entry to restrict user from entering more than 12 digits or letters, character
        def aadharEntryEventHandler(event):
            tempString = ""
            for char in self.aadharEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char
            
            if(len(tempString)>12):
                tempString = tempString[0:12]
                self.aadharEntry.delete(0, "end")
                self.aadharEntry.insert("end", tempString)
            else:
                self.aadharEntry.delete(0, "end")
                self.aadharEntry.insert("end", tempString)

        self.aadharEntry.bind("<KeyRelease>", aadharEntryEventHandler)

        self.mobileEntryVar = StringVar()
        self.mobileEntryVar.set(customerData["mobile"])
        self.mobileEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.mobileEntryVar)
        self.mobileEntry.grid(row=2, column=1)

         #event handler for mobile entry to restrict user from entering more than 12 digits or letters, character
        def mobileEntryEventHandler(event):
            tempString = ""
            for char in self.mobileEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char
            
            if(len(tempString)>10):
                tempString = tempString[0:10]
                self.mobileEntry.delete(0, "end")
                self.mobileEntry.insert("end", tempString)
            else:
                self.mobileEntry.delete(0, "end")
                self.mobileEntry.insert("end", tempString)

        self.mobileEntry.bind("<KeyRelease>", mobileEntryEventHandler)

        self.fatherEntryVar = StringVar()
        self.fatherEntryVar.set(customerData["father"])
        fatherEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.fatherEntryVar)
        fatherEntry.grid(row=3, column=1)

        self.homeAddressEntryVar = StringVar()
        self.homeAddressEntryVar.set(customerData["homeAddress"])
        homeAddressEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.homeAddressEntryVar)
        homeAddressEntry.grid(row=4, column=1)

        self.workAddressEntryVar = StringVar()
        self.workAddressEntryVar.set(customerData["workAddress"])
        workAddressEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.workAddressEntryVar)
        workAddressEntry.grid(row=5, column=1)

        # state of entries depends of emptiness of self.data
        state = ("normal")if(self.data) else ("disable")

        #addign sll entries inside a list
        entryList = [workAddressEntry, fatherEntry, customerEntry, homeAddressEntry, self.mobileEntry, self.aadharEntry]
            
        #operation frame
        self.operationFrame = Frame(self.customerDetailsFrame, bg="red")
        self.operationFrame.grid(row=1, column=0, columnspan=2, sticky="we")

        #configuring grid area
        self.operationFrame.rowconfigure(0, weight=1)
        for i in range(4):
            self.operationFrame.columnconfigure(i, weight=1)

        #This button allows user to interact with entries and edit them
        editButton = Button(self.customerDetailsFrame, text="Edit", state=state, bg="orange")
        editButton.grid(row=1, column=0, columnspan=2, sticky="nsew")

        #configuring commmand for editButton as self.edit()
        editButton.config(command=lambda entryList=entryList, editButton=editButton: self.editCustomer(entryList, editButton))

    #thsi edite function changes state of entries to normal and allows user to edit them and save them
    def editCustomer(self, entryList, editButton):
        #changing state to normal
        for entry in entryList:
            entry.config(state="normal")
        editButton.destroy()

        #opens a filedialog box to select replacement image of client
        changePhotoButton = Button(self.operationFrame, text="change", command=self.changePhoto)
        changePhotoButton.grid(row=0, column=0, sticky="we")

        #cancelButton to exit from edit mode and go to read mode
        cancelButton = Button(self.operationFrame, text="Cancel", command=self.detailsFrameController)
        cancelButton.grid(row=0, column=1, sticky="ew")

        #saves the changes made in edit mode by user
        saveButton = Button(self.operationFrame, text="Save", command=self.save)
        saveButton.grid(row=0, column=2, sticky="we")

        #deletes the customer ,but not its relations with files
        deleteButton = Button(self.operationFrame, text="Delete", bg="red", command=self.delete)
        deleteButton.grid(row=0, column=3, sticky="we")
    
    #this functions saves the changes made by user in edit mode and save it to the database
    def save(self):
        #checking if the fields are filled properly
        if((not self.customerEntryVar.get())):
            requirementsFilled=False
            instructionText = "Please fill Customer's Name Field"
        elif(((not self.aadharEntryVar.get().isdigit()) or (len(self.aadharEntryVar.get())!=12))):
            requirementsFilled=False
            instructionText = "Please Fill Right Format of Aadhar"
        elif((not self.mobileEntryVar.get().isdigit()) or (len(self.mobileEntryVar.get())!=10)):
            requirementsFilled=False
            instructionText = "Please Fill Right Format of Mobile"
        elif((not self.fatherEntryVar.get())):
            requirementsFilled=False
            instructionText = "Please fill Father's Name Field"
        elif((not self.homeAddressEntryVar.get())):
            requirementsFilled=False
            instructionText = "Please fill Home Address Field"
        elif((not self.workAddressEntryVar.get())):
            requirementsFilled=False
            instructionText = "Please fill work address Field"
        else:
            requirementsFilled=True
            instructionText = ""

        if(requirementsFilled):
            #asking if user wants to really save changes
            if(message.askyesno("Save Changes", "Do you want save the changes ?")):
                #creating a customerobject
                customerObject = Customer()

                #updating customer data by takin customer id as reference 
                customerObject.updateData(id=self.data[0][0], name=self.customerEntryVar.get(), father=self.fatherEntryVar.get(), mobile=self.mobileEntryVar.get(), home_address=self.homeAddressEntryVar.get(), work_address=self.workAddressEntryVar.get(), aadhar=self.aadharEntryVar.get())

                #if self.photopath is defined then copying image to the customerPhoto, it will replace the previous image with same name
                if(self.photoPath):
                    shutil.copy(self.photoPath, f"{CUSTOMERPHOTOPATH}/{self.data[0][0]}.jpg")

                #updating self.data 
                self.data = customerObject.whereData(id=self.data[0][0])

                #now calling detailsFrameController to show new customerDetails in readmode
                self.detailsFrameController()
                
                #if self.updateStatus is not empty then updating the tabName
                if(self.updateStatus):
                    self.updateStatus(tabName=self.customerEntryVar.get())
        else:
            message.showerror("Error", instructionText)
    
    def changePhoto(self):
            self.photoPath = askopenfilename(title="Select Customer's Photo", initialdir="/",filetypes=(("PNG", "*.png"),("JPG", "jpg")), multiple=False)
            #if self.photoPath is not empty then only it will proceed
            if(self.photoPath):
                #creating a PIL image object
                img=Image.open(self.photoPath)
                #resizing the image
                img=img.resize((82,120))

                #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
                self.customerPhoto = ImageTk.PhotoImage(img)

                self.customerPhotoLabel.config(image=self.customerPhoto)
            else:
                self.photoPath= None
                
    def delete(self):
        pass
    

#following code won't run until it is run from this file only
if __name__ =="__main__":
    root = Tk()
    root.geometry("950x600")
    root.title("Profile")
    profileObject = Profile(root, 785337610582)
    root.mainloop()