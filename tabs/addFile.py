#importing necessary modules and components and clases
from tkinter import Tk, Frame, Label, Listbox, Scrollbar, END, Checkbutton, IntVar, StringVar, Entry, Button, Text, ttk,  DoubleVar
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from sys import path
import shutil
path.append(r"D:\projects\finoshok\finoshok\model")
path.append(r"D:\projects\finoshok\finoshok\config")
from pathConfig import CUSTOMERPHOTOPATH, GUARRANTERPHOTOPATH
#now we can import Customer and Request class successfully from customer model and Rewusts model respectively
from Customer import Customer
from File import File
from Ledger import Ledger
import tkinter.messagebox as message
from Request import Request
from Guarranter import Guarranter
from Document import Document
from Vehicle import Vehicle
from Ledger import Ledger
from settings import INTERESTRATE


#AddFile class needs a parameter either a tk window or frame
class AddFile:
    def __init__(self, addFileWindow):
        #create mainframe containing everything
        self.mainFrame = Frame(addFileWindow)
        self.mainFrame.pack(fill="both", expand=True)

        #columnconfigure() resizes the grid vertically, while rowconfigure() resizes the grid horizontally. The width of a grid column is equal to the width of its widest cell.

        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.columnconfigure(1, weight=1)
        
        #created subframes
        
        #The sticky parameter in the .grid() method of Tkinter is used to define how a widget should expand to fill the space allocated to it within a grid cell.

        self.subFrame1 = Frame(self.mainFrame, relief="groove", border=3)
        self.subFrame1.grid(row=0, column=0, sticky="ewns")
        self.subFrame1.pack_propagate(False)

        self.subFrame2 = Frame(self.mainFrame, relief="groove", border=3)
        self.subFrame2.grid(row=0, column=1, sticky="ewns", rowspan=2)
        self.subFrame2.pack_propagate(False)

        self.subFrame3 = Frame(self.mainFrame, relief="groove", border=3)
        self.subFrame3.grid(row=1, column=0, sticky="ewns")  
        self.subFrame3.pack_propagate(False)

        #now creating 3 sections : 

        #section 1 for selecting any one loan Request also adding heading/label
        self.searchFrame = Frame(self.subFrame1)
        self.searchFrame.pack(side="top", fill="x")

        #work of searchFrame starts here
        self.searchFrame.columnconfigure(2, weight=1)

        self.searchLabel = Label(self.searchFrame, text="Search here : ")
        self.searchLabel.grid(row=0, column=0)

        self.searchEntry = Entry(self.searchFrame)
        self.searchEntry.grid(row=0, column=1)
        #binding enty and listbox to their respective fucntions
        self.searchEntry.bind("<KeyRelease>", self.search)        #Keyrelease because event actually fires  before entry wicget insert texts.

        self.refreshButton = Button(self.searchFrame, text=u"\u21BB", bg="orange", font="COPPER 12", height=1, width=3, command=self.refresh)
        self.refreshButton.grid(row=0, column=2, sticky="e")

        # creating scrollbar for y direction
        self.scrollY = Scrollbar(self.subFrame1)
        self.scrollY.pack(side="right", fill="y")

        self.section1 = Frame(self.subFrame1)
        self.section1.pack(fill="both", expand=True) 

        #section 2 for loan confirmation along with some formalities
        self.section2 = Frame(self.subFrame2)
        self.section2.pack(fill="both", expand=True)

        #section 3 for showing selected loan request details along with some customer details

        self.section3 = Frame(self.subFrame3)
        self.section3.pack(fill="both", expand=True) 

        #now filling in these sections
        
        #section 1 work start-------

        #creating a self.section1 as more responsive  using rowconfigure and columnconfigure

        self.section1.rowconfigure(0, weight=1)
        self.section1.columnconfigure(0, weight=1)
        
        self.customerRequestBox = ttk.Treeview(self.section1)
        self.customerRequestBox.grid(row=0, column=0, sticky="nsew")
        self.customerRequestBox.bind("<<TreeviewSelect>>", self.dynamicDetails)

        self.customerRequestBox["columns"] = ("name", "mobile", "aadhar", "amount", "date")
        self.customerRequestBox.column('#0', width=50, anchor="center", stretch=False)
        self.customerRequestBox.column('name', width=100, minwidth=50, anchor="center")
        self.customerRequestBox.column('mobile', width=100, minwidth=50, anchor="center")
        self.customerRequestBox.column('aadhar', width=100, minwidth=50, anchor="center")
        self.customerRequestBox.column('amount', width=100, minwidth=50, anchor="center")
        self.customerRequestBox.column('date', width=100, minwidth=50, anchor="center")
        self.customerRequestBox.heading("name", text="Customer Name", anchor="center")
        self.customerRequestBox.heading("mobile", text="Mobile", anchor="center")
        self.customerRequestBox.heading("aadhar", text="Aadhar", anchor="center")
        self.customerRequestBox.heading("amount", text="Amount", anchor="center")
        self.customerRequestBox.heading("date", text="Date", anchor="center")
        self.customerRequestBox.heading("#0", text="S.no.", anchor="center")

        self.scrollY.config(command=self.customerRequestBox.yview)
        self.customerRequestBox.config(yscrollcommand=self.scrollY.set)

        #creating scrollbar for x dirextion
        self.scrollX = Scrollbar(self.subFrame1, command=self.customerRequestBox.xview, orient="horizontal")
        self.scrollX.pack(side="bottom", fill="x")
        self.customerRequestBox.config(xscrollcommand=self.scrollX.set)
        
        self.dataList = []
        self.tempDataList = []

        #section 1 work ends----
        
        #section 2 work starts ----
        self.section2.rowconfigure(0, weight=1)
        self.section2.columnconfigure(0, weight=1)

        self.pagesList = [ApprovalPage(self.section2, parentUpdateStatus=self.updateStatus), GuarrantersPage(self.section2, parentUpdateStatus=self.updateStatus), VehiclesPage(self.section2, parentUpdateStatus=self.updateStatus), DocVerifyPage(self.section2, parentUpdateStatus=self.updateStatus), finalPage(self.section2, parentUpdateStatus=self.updateStatus)]

        self.changePage(0)
        self.operationFrame = Frame(self.subFrame2)
        self.operationFrame.pack(side="bottom", fill="x")

        self.operationFrame.rowconfigure(0, weight=1)
        self.operationFrame.columnconfigure(0, weight=1)
        self.operationFrame.columnconfigure(1, weight=1)
        self.operationFrame.columnconfigure(2, weight=1)

        self.cancelButton = Button(self.operationFrame, text="Cancel", command=self.cancelMethod)
        self.cancelButton.grid(row=0, column=0, sticky="ew")

        self.backButton = Button(self.operationFrame, text="Back", command=self.backPage)
        self.backButton.grid(row=0, column=1, sticky="ew")

        self.nextButton = Button(self.operationFrame, text="Next", bg="orange", command=self.nextPage)
        self.nextButton.grid(row=0, column=2, sticky="we")

        #section 2 work endss ----
            
        #self.section3 work starts ----

        self.section3.rowconfigure(0, weight=1)
        self.section3.columnconfigure(0, weight=1)

        self.customerDetailsFrame = Frame(self.section3, border=1, relief="raised")
        self.customerDetailsFrame.grid(row=0, column=0)
                
        #creating two frames PhotoFrame and Details inside self.customerDetailsFrame
        self.PhotoFrame = Frame(self.customerDetailsFrame, relief="groove", border=3)
        self.PhotoFrame.grid(row=0, column=0, sticky="nsew")

        self.Details = Frame(self.customerDetailsFrame, relief="groove", border=3)
        self.Details.grid(row=0, column=1, sticky="nsew")

        #creating responsive PhotoFrame
        self.PhotoFrame.rowconfigure(0, weight=1)
        self.PhotoFrame.columnconfigure(0, weight=1)

        #creating a PIL image object
            
        #if error found during imaging loading then use default image
        #now integrating the image into label widget and positioning it via grid 
        self.customerPhotoLabel = Label(self.PhotoFrame)
        self.customerPhotoLabel.grid(row=0, column=0)
        
        #creating responsive sec3Details frame
        self.Details.rowconfigure(0, weight=1)
        self.Details.columnconfigure(0, weight=1)
            
        #creating a inner subFramee detailsInnerFrame inside sec3details
        self.detailsInnerFrame = Frame(self.Details)
        self.detailsInnerFrame.grid(row=0, column=0)

        #creating labels static
        self.customerNameLabel = Label(self.detailsInnerFrame, text="Name : ")
        self.customerNameLabel.grid(row=0, column=0)

        self.aadharLabel = Label(self.detailsInnerFrame, text="Aadhar : ")
        self.aadharLabel.grid(row=1, column=0)

        self.mobileLabel = Label(self.detailsInnerFrame, text="Mobile : ")
        self.mobileLabel.grid(row=2, column=0)

        self.fatherLabel = Label(self.detailsInnerFrame, text="Father : ")
        self.fatherLabel.grid(row=3, column=0)

        self.homeAddressLabel = Label(self.detailsInnerFrame, text="Home Address : ")
        self.homeAddressLabel.grid(row=4, column=0)

        self.workAddressLabel = Label(self.detailsInnerFrame, text="Work Address : ")
        self.workAddressLabel.grid(row=5, column=0)

        self.purposeLabel = Label(self.customerDetailsFrame, text="Purpose of Loan : ")
        self.purposeLabel.grid(row=1, column=0)

        #creating labels dynamic
        self.customerEntryVar = StringVar()
        self.customerEntryVar.set("null")
        self.customerEntry = Entry(self.detailsInnerFrame, state="readonly", textvariable=self.customerEntryVar)
        self.customerEntry.grid(row=0, column=1)

        self.aadharEntryVar = StringVar()
        self.aadharEntryVar.set("null")
        self.aadharEntry = Entry(self.detailsInnerFrame, state="readonly", textvariable=self.aadharEntryVar)
        self.aadharEntry.grid(row=1, column=1)

        self.mobileEntryVar = StringVar()
        self.mobileEntryVar.set("null")
        self.mobileEntry = Entry(self.detailsInnerFrame, state="readonly", textvariable=self.mobileEntryVar)
        self.mobileEntry.grid(row=2, column=1)

        self.fatherEntryVar = StringVar()
        self.fatherEntryVar.set("null")
        self.fatherEntry = Entry(self.detailsInnerFrame, state="readonly", textvariable=self.fatherEntryVar)
        self.fatherEntry.grid(row=3, column=1)

        self.homeAddressEntryVar = StringVar()
        self.homeAddressEntryVar.set("null")
        self.homeAddressEntry = Entry(self.detailsInnerFrame, state="readonly", textvariable=self.homeAddressEntryVar)
        self.homeAddressEntry.grid(row=4, column=1)

        self.workAddressEntryVar = StringVar()
        self.workAddressEntryVar.set("null")
        self.workAddressEntry = Entry(self.detailsInnerFrame, state="readonly", textvariable=self.workAddressEntryVar)
        self.workAddressEntry.grid(row=5, column=1)

        self.purposeEntry = Text(self.customerDetailsFrame, width=40, height=10, state="disabled")
        self.purposeEntry.grid(row=1, column=1)
        #self.section3 workd ends----

        #initially invoking search funtion
        self.refresh()
        self.customerRequestBox.selection_set(0) if(self.dataList!=[]) else 0
        self.customerRequestBox.focus(0) if(self.dataList!=[]) else 0
        self.dynamicDetails(None)
    #it will display data in listbox according to the search query
    
    def search(self, event):
        if(self.searchEntry.get()):
            #search according to aadhar, mobile, name
            searchText = self.searchEntry.get()
            self.tempDataList = []

            for customer in self.dataList:
                if(searchText.lower() in str(customer["aadhar"]).lower() or searchText.lower() in customer["name"].lower() or searchText.lower() in str(customer["mobile"]).lower()):
                    self.tempDataList.append(customer)
            iids = self.customerRequestBox.get_children()
            for iid in iids:
                self.customerRequestBox.delete(iid)
            count=0
            for customer in self.tempDataList:
                self.customerRequestBox.insert(parent="", text=count, index="end", iid=count, values=(customer["name"], customer["mobile"], customer["aadhar"], customer["amountRequested"], customer["dateRequested"]))
                count+=1
        else:
            iids = self.customerRequestBox.get_children()
            for iid in iids:
                self.customerRequestBox.delete(iid)
            count=0
            for customer in self.dataList:
                self.customerRequestBox.insert(parent="", text=count, index="end", iid=count, values=(customer["name"], customer["mobile"], customer["aadhar"], customer["amountRequested"], customer["dateRequested"]))
                count+=1
            self.tempDataList = self.dataList
    
    def dynamicDetails(self, event):
        #checking if there is selected item currnently and the status of that item is 1 i.e active
        if(self.customerRequestBox.focus() and self.dataList[int(self.customerRequestBox.focus())]["status"]==1):
            #trying to show photo of customer
            try:
                self.photoPath = f"D:\\projects\\finoshok\\finoshok\\assets\\customerPhotos\\{self.dataList[int(self.customerRequestBox.focus())]["customerId"]}.jpg"
                img=Image.open(self.photoPath)
                
                #resizing the image
                img=img.resize((82,120))

                #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
                self.customerPhoto = ImageTk.PhotoImage(img)
                self.customerPhotoLabel.config(image=self.customerPhoto)
            except:
                self.photoPath = f"D:\\projects\\finoshok\\finoshok\\assets\\defaultImages\\user.jpg"
                img=Image.open(self.photoPath)
                
                #resizing the image
                img=img.resize((82,120))

                #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
                self.customerPhoto = ImageTk.PhotoImage(img)
                self.customerPhotoLabel.config(image=self.customerPhoto)

            #settign the values of entries in details frame
                
            self.customerEntryVar.set(self.dataList[int(self.customerRequestBox.focus())]["name"])
            self.aadharEntryVar.set(self.dataList[int(self.customerRequestBox.focus())]["aadhar"])
            self.mobileEntryVar.set(self.dataList[int(self.customerRequestBox.focus())]["mobile"])
            self.fatherEntryVar.set(self.dataList[int(self.customerRequestBox.focus())]["father"])
            self.homeAddressEntryVar.set(self.dataList[int(self.customerRequestBox.focus())]["homeAddress"])
            self.workAddressEntryVar.set(self.dataList[int(self.customerRequestBox.focus())]["workAddress"])
            self.purposeEntry.config(state="normal")
            
            #deleting all the data from textbox of purpose entry and then reinserting the new value of purpose
            self.purposeEntry.delete("1.0", END)
            self.purposeEntry.insert(END, self.dataList[int(self.customerRequestBox.focus())]["purpose"])
            self.purposeEntry.config(state="disable")
            
            #performing cancel method
            self.cancelMethod()
        else:
            self.photoPath = f"D:\\projects\\finoshok\\finoshok\\assets\\defaultImages\\user.jpg"
            img=Image.open(self.photoPath)
                
            #resizing the image
            img=img.resize((82,120))

            #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
            self.customerPhoto = ImageTk.PhotoImage(img)
            self.customerPhotoLabel.config(image=self.customerPhoto)
    #refresh button replenis new data in self.data and renews items in listbox of Request
    def refresh(self):
        #reading the all data of Request from database
        RequestData = Request().whereData(status="1")

        customerObject = Customer()
        self.dataList = []

        #updating self.datalist and self.customerRequestBox
        for request in RequestData:
            tempCustomerData = customerObject.whereData(id=request[1])

            self.dataList.append({"customerId":tempCustomerData[0][0], "aadhar":tempCustomerData[0][6], "name":tempCustomerData[0][1], "father":tempCustomerData[0][2], "mobile":tempCustomerData[0][3], "homeAddress":tempCustomerData[0][4], "workAddress": tempCustomerData[0][5], "status":request[5], "purpose":request[3], "amountRequested": request[2], "dateRequested":request[4]})

        self.searchEntry.delete(0, "end")
        self.search(None)
        self.customerRequestBox.selection_set(0) if(self.dataList!=[]) else 0
        self.customerRequestBox.focus(0) if(self.dataList!=[]) else 0
        self.dynamicDetails(None)
        
        #now restarting the dynamic details 
        self.customerRequestBox.selection_set(0) if(self.dataList!=[]) else 0
        self.dynamicDetails(None)
        self.cancelMethod()
    
    #method to change page dynamically
    def changePage(self, index):
        if(not(index>(len(self.pagesList)-1)) and index>-1):
            for page in self.pagesList:
                page.mainFrame.grid_forget()
            self.pagesList[index].mainFrame.grid(row=0, column=0, sticky="nsew")
            self.currentPageIndex = index
        
    
    def updateStatus(self):
        # if(self.pagesList[0].loanCheckVar.get()==1):
        #     self.customerRequestBox.config(state="disable")
        # else:
        #     self.customerRequestBox.config(state="normal")
        
        if(self.pagesList[0].ok==True):
            if(self.pagesList[0].guarranterCheckVar.get()==1):
                self.pagesList[1].enable()
            else:
                self.pagesList[1].disable()

            if(self.pagesList[0].typeOfLoanEntry.get()=="Loan on vehicle" and self.pagesList[2].ok !=True):
                self.pagesList[2].enable()
            else:
                self.pagesList[2].disable()

            if(self.pagesList[3].ok==True):
                self.pagesList[3].disable()
            else:
                self.pagesList[3].enable()
            
            if(self.pagesList[4].loanPassed):
                if(self.pagesList[0].guarranterCheckVar.get()==1 and self.pagesList[0].typeOfLoanEntry.get()=="Loan on vehicle"):
                    if(self.pagesList[1].ok and self.pagesList[2].ok):
                        if(self.pagesList[3].ok):
                            customerObject = Customer()
                            customerId = customerObject.whereData(aadhar=self.aadharEntryVar.get())[0][0]

                            fileObject = File()
                            loanAmount=self.pagesList[4].amountApprovedVar.get()
                            interest=self.pagesList[4].interestVar.get()
                            timePeriod=self.pagesList[4].loanPeriodVar.get()
                            emiAmount=self.pagesList[4].installmentAmtVar.get()
                            numOfEmi = self.pagesList[4].numOfEmiVar.get()
                            dateApproved=str(self.pagesList[0].dateApprovedEntry.get_date().year)+"/"+str(self.pagesList[0].dateApprovedEntry.get_date().month)+"/"+str(self.pagesList[0].dateApprovedEntry.get_date().day)

                            fileInsertSuccessfully = fileObject.insertData(customerId=customerId, loanAmount=loanAmount, interest=interest, timePeriod=timePeriod, status="1", emiAmount=emiAmount, numEmi=numOfEmi,  note=self.purposeEntry.get('1.0', 'end'), loanType="Loan on vehicles", dateApproved=dateApproved)

                            fileId = fileObject.whereData(customerId=customerId, dateApproved=dateApproved)[0][0]

                            guarranterObject = Guarranter()

                            guarranterInsertSuccessfully=guarranterObject.insertData(customer_id=customerId, name=self.pagesList[1].gNameVar.get(), father=self.pagesList[1].fNameVar.get(), mobile=self.pagesList[1].mobileVar.get(), home_address=self.pagesList[1].hAddressVar.get(), work_address=self.pagesList[1].wAddressVar.get(), aadhar=self.pagesList[1].aadharVar.get(), status=1)

            
                            guarranterId=guarranterObject.whereData(aadhar=self.pagesList[1].aadharVar.get())[0][0]
                            fileObject.updateData(id=fileId, guarranterId=guarranterId)


                            if(self.photoPath):
                                shutil.copy(self.photoPath, f"{GUARRANTERPHOTOPATH}\\{guarranterId}.jpg")

                            documentObject = Document()
                            documentObject.insertData(customer_id=customerId, doc_name="aadhar", required=self.pagesList[3].aadharReqVar.get(), verified=self.pagesList[3].aadharVerifyVar.get(), file_id=fileId, status=self.pagesList[3].aadharVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="pancard", required=self.pagesList[3].pancardReqVar.get(), verified=self.pagesList[3].pancardVerifyVar.get(), file_id=fileId, status=self.pagesList[3].pancardVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="cheque", required=self.pagesList[3].chequeReqVar.get(), verified=self.pagesList[3].chequeVerifyVar.get(), file_id=fileId, status=self.pagesList[3].chequeVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="stamp", required=self.pagesList[3].stampReqVar.get(), verified=self.pagesList[3].stampVerifyVar.get(), file_id=fileId, status=self.pagesList[3].stampVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="rc", required=self.pagesList[3].rcReqVar.get(), verified=self.pagesList[3].rcVerifyVar.get(), file_id=fileId, status=self.pagesList[3].rcVerifyVar.get())

                            vehicleObject = Vehicle()
                            vehicleInsertSuccessfully=vehicleObject.insertData(customerId=customerId, name=self.pagesList[2].vNameVar.get(), plateNum=self.pagesList[2].numberPlateVar.get(), model=self.pagesList[2].modelVar.get(), manufacturer=self.pagesList[2].manufacturerVar.get(), note="sud", fuel=self.pagesList[2].fuelUsedVar.get(), engineCC=self.pagesList[2].engineCCVar.get(), horsePowerBHP=self.pagesList[2].horsePowerVar.get(), cyilenders=self.pagesList[2].numCyilendersVar.get() ,fuelCapacity=self.pagesList[2].fuelCapacityVar.get() ,seatingCapacity=self.pagesList[2].seatingCapacityVar.get(), vehicleWeightKG=self.pagesList[2].vehicleWeightVar.get(), status=1, currentCondition="fine", fileId=fileId)

                            ledgerObject = Ledger()
                            itemIids =  self.pagesList[4].table.get_children()
                            for iid in itemIids:
                                values = self.pagesList[4].table.item(iid, "values")
                                ledgerObject.insertData(fileId=fileId, emiNumber=values[0], status=0, emiDate=values[1], emiAmount=values[2], note="sud")
                            
                            if(fileInsertSuccessfully):
                                RequestObject = Request()
                                id=RequestObject.whereData(customer_id=customerId)[0][0]
                                RequestObject.updateData(id=id, status="0")
                                message.showinfo("Loan Passed Successfully", f"Loan Passed successfully for {self.customerEntryVar.get()}")
                                self.refresh()
                            else:
                                if(vehicleInsertSuccessfully):
                                    vehicleId = vehicleObject.whereData(fileId=fileId)[0][0]
                                    vehicleObject.deleteRow(id=vehicleId)
                                ledgerIds = ledgerObject.whereData(fileId=fileId)
                                for idrow in ledgerIds:
                                    ledgerObject.deleteRow(id=idrow[0])
                                documentIds = documentObject.whereData(fileId=fileId)
                                for idrow in documentIds:
                                    documentObject.deleteRow(id=idrow[0])
                                if(guarranterInsertSuccessfully):
                                    guarranterId = fileObject.whereData(fileId=fileId)[0][10]
                                    guarranterObject.deleteRow(guarranterId)
                                
                                message.showerror("Error", f"please contact developer for \nmore details")
                        else:
                            self.changePage(3)
                    else:
                        self.pagesList[4].loanPassed=False
                        if(not self.pagesList[1].ok):
                            self.changePage(1)
                            self.pagesList[1].checkData()
                        else:
                            self.changePage(2)
                            self.pagesList[2].checkData()

                elif(self.pagesList[0].guarranterCheckVar.get()==1 and self.pagesList[0].typeOfLoanEntry.get()=="Personal Loan"):
                    if(self.pagesList[1].ok):
                        if(self.pagesList[3].ok):
                            customerObject = Customer()
                            customerId = customerObject.whereData(aadhar=self.aadharEntryVar.get())[0][0]

                            fileObject = File()
                            loanAmount=self.pagesList[4].amountApprovedVar.get()
                            interest=self.pagesList[4].interestVar.get()
                            timePeriod=self.pagesList[4].loanPeriodVar.get()
                            emiAmount=self.pagesList[4].installmentAmtVar.get()
                            numOfEmi = self.pagesList[4].numOfEmiVar.get()
                            dateApproved=str(self.pagesList[0].dateApprovedEntry.get_date().year)+"/"+str(self.pagesList[0].dateApprovedEntry.get_date().month)+"/"+str(self.pagesList[0].dateApprovedEntry.get_date().day)

                            fileInsertSuccessfully = fileObject.insertData(customerId=customerId, loanAmount=loanAmount, interest=interest, timePeriod=timePeriod, status="1", emiAmount=emiAmount, numEmi=numOfEmi,  note=self.purposeEntry.get('1.0', 'end'), loanType="Loan on vehicles", dateApproved=dateApproved)

                            fileId = fileObject.whereData(customerId=customerId, dateApproved=dateApproved)[0][0]

                            guarranterObject = Guarranter()
                            guarranterInsertSuccessfully=guarranterObject.insertData(customer_id=customerId, name=self.pagesList[1].gNameVar.get(), father=self.pagesList[1].fNameVar.get(), mobile=self.pagesList[1].mobileVar.get(), home_address=self.pagesList[1].hAddressVar.get(), work_address=self.pagesList[1].wAddressVar.get(), aadhar=self.pagesList[1].aadharVar.get(), photo=self.pagesList[1].photoPath, status=1)

                            documentObject = Document()
                            documentObject.insertData(customer_id=customerId, doc_name="aadhar", required=self.pagesList[3].aadharReqVar.get(), verified=self.pagesList[3].aadharVerifyVar.get(), file_id=fileId, status=self.pagesList[3].aadharVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="pancard", required=self.pagesList[3].pancardReqVar.get(), verified=self.pagesList[3].pancardVerifyVar.get(), file_id=fileId, status=self.pagesList[3].pancardVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="cheque", required=self.pagesList[3].chequeReqVar.get(), verified=self.pagesList[3].chequeVerifyVar.get(), file_id=fileId, status=self.pagesList[3].chequeVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="stamp", required=self.pagesList[3].stampReqVar.get(), verified=self.pagesList[3].stampVerifyVar.get(), file_id=fileId, status=self.pagesList[3].stampVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="rc", required=self.pagesList[3].rcReqVar.get(), verified=self.pagesList[3].rcVerifyVar.get(), file_id=fileId, status=self.pagesList[3].rcVerifyVar.get())

                            ledgerObject = Ledger()
                            itemIids =  self.pagesList[4].table.get_children()
                            for iid in itemIids:
                                values = self.pagesList[4].table.item(iid, "values")
                                ledgerObject.insertData(fileId=fileId, emiNumber=values[0], status=0, emiDate=values[1], emiAmount=values[2], note="sud")
                            
                            if(fileInsertSuccessfully):
                                RequestObject = Request()
                                id=RequestObject.whereData(customer_id=customerId)[0][0]
                                RequestObject.updateData(id=id, status="0")
                                message.showinfo("Loan Passed Successfully", f"Loan Passed successfully for {self.customerEntryVar.get()}")
                                self.refresh()
                            else:
                                ledgerIds = ledgerObject.whereData(fileId=fileId)
                                for idrow in ledgerIds:
                                    ledgerObject.deleteRow(id=idrow[0])
                                documentIds = documentObject.whereData(fileId=fileId)
                                for idrow in documentIds:
                                    documentObject.deleteRow(id=idrow[0])
                                if(guarranterInsertSuccessfully):
                                    guarranterId = fileObject.whereData(fileId=fileId)[0][10]
                                    guarranterObject.deleteRow(guarranterId)
                                
                                message.showerror("Error", f"please contact developer for \nmore details")
                        else:
                            self.changePage(3)
                    else:
                        self.pagesList[4].loanPassed=False
                        if(not self.pagesList[1].ok):
                            self.changePage(1)
                            self.pagesList[1].checkData()
                elif(self.pagesList[0].typeOfLoanEntry.get() == "Loan on vehicle" and not self.pagesList[0].guarranterCheckVar.get()):
                    if(self.pagesList[2].ok):
                        if(self.pagesList[3].ok):
                            customerObject = Customer()
                            customerId = customerObject.whereData(aadhar=self.aadharEntryVar.get())[0][0]

                            fileObject = File()
                            loanAmount=self.pagesList[4].amountApprovedVar.get()
                            interest=self.pagesList[4].interestVar.get()
                            timePeriod=self.pagesList[4].loanPeriodVar.get()
                            emiAmount=self.pagesList[4].installmentAmtVar.get()
                            numOfEmi = self.pagesList[4].numOfEmiVar.get()
                            dateApproved=str(self.pagesList[0].dateApprovedEntry.get_date().year)+"/"+str(self.pagesList[0].dateApprovedEntry.get_date().month)+"/"+str(self.pagesList[0].dateApprovedEntry.get_date().day)

                            fileInsertSuccessfully = fileObject.insertData(customerId=customerId, loanAmount=loanAmount, interest=interest, timePeriod=timePeriod, status="1", emiAmount=emiAmount, numEmi=numOfEmi,  note=self.purposeEntry.get('1.0', 'end'), loanType="Loan on vehicles", dateApproved=dateApproved)

                            fileId = fileObject.whereData(customerId=customerId, dateApproved=dateApproved)[0][0]

                            documentObject = Document()
                            documentObject.insertData(customer_id=customerId, doc_name="aadhar", required=self.pagesList[3].aadharReqVar.get(), verified=self.pagesList[3].aadharVerifyVar.get(), file_id=fileId, status=self.pagesList[3].aadharVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="pancard", required=self.pagesList[3].pancardReqVar.get(), verified=self.pagesList[3].pancardVerifyVar.get(), file_id=fileId, status=self.pagesList[3].pancardVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="cheque", required=self.pagesList[3].chequeReqVar.get(), verified=self.pagesList[3].chequeVerifyVar.get(), file_id=fileId, status=self.pagesList[3].chequeVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="stamp", required=self.pagesList[3].stampReqVar.get(), verified=self.pagesList[3].stampVerifyVar.get(), file_id=fileId, status=self.pagesList[3].stampVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="rc", required=self.pagesList[3].rcReqVar.get(), verified=self.pagesList[3].rcVerifyVar.get(), file_id=fileId, status=self.pagesList[3].rcVerifyVar.get())

                            vehicleObject = Vehicle()
                            vehicleInsertSuccessfully=vehicleObject.insertData(customerId=customerId, name=self.pagesList[2].vNameVar.get(), plateNum=self.pagesList[2].numberPlateVar.get(), model=self.pagesList[2].modelVar.get(), manufacturer=self.pagesList[2].manufacturerVar.get(), note="sud", fuel=self.pagesList[2].fuelUsedVar.get(), engineCC=self.pagesList[2].engineCCVar.get(), horsePowerBHP=self.pagesList[2].horsePowerVar.get(), cyilenders=self.pagesList[2].numCyilendersVar.get() ,fuelCapacity=self.pagesList[2].fuelCapacityVar.get() ,seatingCapacity=self.pagesList[2].seatingCapacityVar.get(), vehicleWeightKG=self.pagesList[2].vehicleWeightVar.get(), status=1, currentCondition="fine")

                            ledgerObject = Ledger()
                            itemIids =  self.pagesList[4].table.get_children()
                            for iid in itemIids:
                                values = self.pagesList[4].table.item(iid, "values")
                                ledgerObject.insertData(fileId=fileId, emiNumber=values[0], status=0, emiDate=values[1], emiAmount=values[2], note="sud")
                            
                            if(fileInsertSuccessfully):
                                RequestObject = Request()
                                id=RequestObject.whereData(customer_id=customerId)[0][0]
                                RequestObject.updateData(id=id, status="0")
                                message.showinfo("Loan Passed Successfully", f"Loan Passed successfully for {self.customerEntryVar.get()}")
                                self.refresh()
                            else:
                                if(vehicleInsertSuccessfully):
                                    vehicleId = vehicleObject.whereData(fileId=fileId)[0][0]
                                    vehicleObject.deleteRow(id=vehicleId)
                                ledgerIds = ledgerObject.whereData(fileId=fileId)
                                for idrow in ledgerIds:
                                    ledgerObject.deleteRow(id=idrow[0])
                                documentIds = documentObject.whereData(fileId=fileId)
                                for idrow in documentIds:
                                    documentObject.deleteRow(id=idrow[0])

                                message.showerror("Error", f"please contact developer for \nmore details")
                        else:
                            self.changePage(3)
                    else:
                        self.pagesList[4].loanPassed=False
                        if(not self.pagesList[2].ok):
                            self.changePage(2)
                            self.pagesList[2].checkData()
                
                elif(self.pagesList[0].typeOfLoanEntry.get() == "Personal Loan" and not self.pagesList[0].guarranterCheckVar.get()):
                    if(self.pagesList[3].ok):
                            customerObject = Customer()
                            customerId = customerObject.whereData(aadhar=self.aadharEntryVar.get())[0][0]

                            fileObject = File()
                            loanAmount=self.pagesList[4].amountApprovedVar.get()
                            interest=self.pagesList[4].interestVar.get()
                            timePeriod=self.pagesList[4].loanPeriodVar.get()
                            emiAmount=self.pagesList[4].installmentAmtVar.get()
                            numOfEmi = self.pagesList[4].numOfEmiVar.get()
                            dateApproved=str(self.pagesList[0].dateApprovedEntry.get_date().year)+"/"+str(self.pagesList[0].dateApprovedEntry.get_date().month)+"/"+str(self.pagesList[0].dateApprovedEntry.get_date().day)

                            fileInsertSuccessfully = fileObject.insertData(customerId=customerId, loanAmount=loanAmount, interest=interest, timePeriod=timePeriod, status="1", emiAmount=emiAmount, numEmi=numOfEmi,  note=self.purposeEntry.get('1.0', 'end'), loanType="Loan on vehicles", dateApproved=dateApproved)

                            fileId = fileObject.whereData(customerId=customerId, dateApproved=dateApproved)[0][0]

                            documentObject = Document()
                            documentObject.insertData(customer_id=customerId, doc_name="aadhar", required=self.pagesList[3].aadharReqVar.get(), verified=self.pagesList[3].aadharVerifyVar.get(), file_id=fileId, status=self.pagesList[3].aadharVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="pancard", required=self.pagesList[3].pancardReqVar.get(), verified=self.pagesList[3].pancardVerifyVar.get(), file_id=fileId, status=self.pagesList[3].pancardVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="cheque", required=self.pagesList[3].chequeReqVar.get(), verified=self.pagesList[3].chequeVerifyVar.get(), file_id=fileId, status=self.pagesList[3].chequeVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="stamp", required=self.pagesList[3].stampReqVar.get(), verified=self.pagesList[3].stampVerifyVar.get(), file_id=fileId, status=self.pagesList[3].stampVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="rc", required=self.pagesList[3].rcReqVar.get(), verified=self.pagesList[3].rcVerifyVar.get(), file_id=fileId, status=self.pagesList[3].rcVerifyVar.get())

                            ledgerObject = Ledger()
                            itemIids =  self.pagesList[4].table.get_children()
                            for iid in itemIids:
                                values = self.pagesList[4].table.item(iid, "values")
                                ledgerObject.insertData(fileId=fileId, emiNumber=values[0], status=0, emiDate=values[1], emiAmount=values[2], note="sud")
                            
                            if(fileInsertSuccessfully):
                                RequestObject = Request()
                                id=RequestObject.whereData(customer_id=customerId)[0][0]
                                RequestObject.updateData(id=id, status="0")
                                message.showinfo("Loan Passed Successfully", f"Loan Passed successfully for {self.customerEntryVar.get()}")
                                self.refresh()
                            else:
                                ledgerIds = ledgerObject.whereData(fileId=fileId)
                                for idrow in ledgerIds:
                                    ledgerObject.deleteRow(id=idrow[0])
                                documentIds = documentObject.whereData(fileId=fileId)
                                for idrow in documentIds:
                                    documentObject.deleteRow(id=idrow[0])
                                
                                message.showerror("Error", f"please contact developer for \nmore details")
                    else:
                        self.changePage(3)
                elif(self.pagesList[0].typeOfLoanEntry.get() == "Personal Loan" and self.pagesList[0].guarranterCheckVar.get()):
                    if(self.pagesList[1].ok):
                        if(self.pagesList[3].ok):
                            customerObject = Customer()
                            customerId = customerObject.whereData(aadhar=self.aadharEntryVar.get())[0][0]

                            fileObject = File()
                            loanAmount=self.pagesList[4].amountApprovedVar.get()
                            interest=self.pagesList[4].interestVar.get()
                            timePeriod=self.pagesList[4].loanPeriodVar.get()
                            emiAmount=self.pagesList[4].installmentAmtVar.get()
                            numOfEmi = self.pagesList[4].numOfEmiVar.get()
                            dateApproved=str(self.pagesList[0].dateApprovedEntry.get_date().year)+"/"+str(self.pagesList[0].dateApprovedEntry.get_date().month)+"/"+str(self.pagesList[0].dateApprovedEntry.get_date().day)

                            fileInsertSuccessfully = fileObject.insertData(customerId=customerId, loanAmount=loanAmount, interest=interest, timePeriod=timePeriod, status="1", emiAmount=emiAmount, numEmi=numOfEmi,  note=self.purposeEntry.get('1.0', 'end'), loanType="Loan on vehicles", dateApproved=dateApproved)

                            fileId = fileObject.whereData(customerId=customerId, dateApproved=dateApproved)[0][0]

                            guarranterObject = Guarranter()
                            guarranterInsertSuccessfully=guarranterObject.insertData(customer_id=customerId, name=self.pagesList[1].gNameVar.get(), father=self.pagesList[1].fNameVar.get(), mobile=self.pagesList[1].mobileVar.get(), home_address=self.pagesList[1].hAddressVar.get(), work_address=self.pagesList[1].wAddressVar.get(), aadhar=self.pagesList[1].aadharVar.get(), photo=self.pagesList[1].photoPath, status=1)

                            documentObject = Document()
                            documentObject.insertData(customer_id=customerId, doc_name="aadhar", required=self.pagesList[3].aadharReqVar.get(), verified=self.pagesList[3].aadharVerifyVar.get(), file_id=fileId, status=self.pagesList[3].aadharVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="pancard", required=self.pagesList[3].pancardReqVar.get(), verified=self.pagesList[3].pancardVerifyVar.get(), file_id=fileId, status=self.pagesList[3].pancardVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="cheque", required=self.pagesList[3].chequeReqVar.get(), verified=self.pagesList[3].chequeVerifyVar.get(), file_id=fileId, status=self.pagesList[3].chequeVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="stamp", required=self.pagesList[3].stampReqVar.get(), verified=self.pagesList[3].stampVerifyVar.get(), file_id=fileId, status=self.pagesList[3].stampVerifyVar.get())

                            documentObject.insertData(customer_id=customerId, doc_name="rc", required=self.pagesList[3].rcReqVar.get(), verified=self.pagesList[3].rcVerifyVar.get(), file_id=fileId, status=self.pagesList[3].rcVerifyVar.get())

                            ledgerObject = Ledger()
                            itemIids =  self.pagesList[4].table.get_children()
                            for iid in itemIids:
                                values = self.pagesList[4].table.item(iid, "values")
                                ledgerObject.insertData(fileId=fileId, emiNumber=values[0], status=0, emiDate=values[1], emiAmount=values[2], note="sud")
                            
                            if(fileInsertSuccessfully):
                                RequestObject = Request()
                                id=RequestObject.whereData(customer_id=customerId)[0][0]
                                RequestObject.updateData(id=id, status="0")
                                message.showinfo("Loan Passed Successfully", f"Loan Passed successfully for {self.customerEntryVar.get()}")
                                self.refresh()
                            else:
                                ledgerIds = ledgerObject.whereData(fileId=fileId)
                                for idrow in ledgerIds:
                                    ledgerObject.deleteRow(id=idrow[0])
                                documentIds = documentObject.whereData(fileId=fileId)
                                for idrow in documentIds:
                                    documentObject.deleteRow(id=idrow[0])
                                if(guarranterInsertSuccessfully):
                                    guarranterId = fileObject.whereData(fileId=fileId)[0][10]
                                    guarranterObject.deleteRow(guarranterId)
                                
                                message.showerror("Error", f"please contact developer for \nmore details")
                        else:
                            self.changePage(3)
                    else:
                        self.pagesList[4].loanPassed=False
                        self.changePage(1)
                        self.pagesList[1].checkData()
                
            else:
                self.pagesList[4].enable()
        

    def backPage(self):
        self.changePage(self.currentPageIndex-1)

    def nextPage(self):
        self.changePage(self.currentPageIndex+1)
        
    def cancelMethod(self):
        # children = self.section2.winfo_children()
        # for page in children:
        #     page.destroy()
        # del self.pagesList
        # self.pagesList = [ApprovalPage(self.section2, parentUpdateStatus=self.updateStatus), GuarrantersPage(self.section2, parentUpdateStatus=self.updateStatus), VehiclesPage(self.section2, parentUpdateStatus=self.updateStatus), DocVerifyPage(self.section2, parentUpdateStatus=self.updateStatus), finalPage(self.section2, parentUpdateStatus=self.updateStatus)]
        # self.pagesList[1].disable()
        # self.pagesList[2].disable()
        self.pagesList[0].initialStage()
        self.pagesList[1].initialStage()
        self.pagesList[2].initialStage()
        self.pagesList[3].initialStage()
        self.pagesList[4].initialStage()
        self.pagesList[0].ok=False
        if(not self.dataList):
            self.pagesList[0].disable()

        self.changePage(0)
        self.updateStatus()

class ApprovalPage:
    def __init__(self, pageWindow, parentUpdateStatus = None):
        
        self.parentUpdateStatus = parentUpdateStatus
        self.mainFrame = Frame(pageWindow)
        self.mainFrame.grid(row=0, column=0, sticky="nsew")

        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)

        innerMainFrame = Frame(self.mainFrame)
        innerMainFrame.grid(row=0, column=0)

        self.ok = False

        #now creating labels

        approveLoanLabel = Label(innerMainFrame, text="Approve Loan : ")
        approveLoanLabel.grid(row=0, column=0, pady=20)

        dateApprovedLabel = Label(innerMainFrame, text="Date Approved : ")
        dateApprovedLabel.grid(row=1, column=0, pady=20)

        typeOfLoanLabel = Label(innerMainFrame, text="Type of Loan : ")
        typeOfLoanLabel.grid(row=2, column=0, pady=20)

        guarranterLabel = Label(innerMainFrame, text="Guarranter : ")
        guarranterLabel.grid(row=3, column=0, pady=20)


        # #now creating entries, dateentry

        #here a check button is created to enable access to remaining entries and to make sure that loan is approved

        self.loanCheckVar = IntVar()
        self.approveLoanCheck = Checkbutton(innerMainFrame, variable=self.loanCheckVar, command=self.enableEntries)
        self.approveLoanCheck.grid(row=0, column=1, stick="w")

        #created dateApprovedEntry to select the date on which loan was aprroved
        self.dateApprovedEntry = DateEntry(innerMainFrame, width=17, date_pattern="yyyy-mm-dd", justify="center", state="disable", selectmode="day")
        self.dateApprovedEntry.grid(row=1, column=1)

        #created typeofloanentry to select the type of loan
        values = ["Loan on vehicle", "Personal Loan"]
        self.typeOfLoanEntry = ttk.Combobox(innerMainFrame, width=17, justify="center", state="disable", values=values)
        self.typeOfLoanEntry.grid(row=2, column=1)

        #created gurranterEntry to check if gurranters are their on this loan
        self.guarranterCheckVar = IntVar()
        self.guarranterCheck = Checkbutton(innerMainFrame, variable=self.guarranterCheckVar, state="disable")
        self.guarranterCheck.grid(row=3, column=1, stick="w")

        self.okButton = Button(innerMainFrame, text="Ok", state="disable", command=self.checkData)
        self.okButton.grid(row=4, column=0, columnspan=2, sticky="we")

    
    def updateStatus(self):
        if(self.parentUpdateStatus):
            self.parentUpdateStatus()
    
    def enableEntries(self):
        if(self.loanCheckVar.get()==1):
            self.dateApprovedEntry.config(state="readonly")
            self.typeOfLoanEntry.config(state="readonly")
            self.guarranterCheck.config(state="normal")
            self.okButton.config(state="normal")
        else:
            self.dateApprovedEntry.config(state="disable")
            self.typeOfLoanEntry.config(state="disable")
            self.guarranterCheck.config(state="disable")
            self.okButton.config(state="disable")
        self.updateStatus()
    
    def checkData(self):
        if(self.loanCheckVar.get()==1):
            if(self.dateApprovedEntry.get() and self.typeOfLoanEntry.get()):
                self.ok = True
                self.approveLoanCheck.config(state="disable")
                self.dateApprovedEntry.config(state="disable")
                self.typeOfLoanEntry.config(state="disable")
                self.guarranterCheck.config(state="disable")
                self.okButton.config(state="disable")
                self.updateStatus()
            else:
                self.ok = False
        else:
            self.approveLoanCheck.config(state="normal")
        
    def disable(self):
        self.approveLoanCheck.config(state="disable")
        self.dateApprovedEntry.config(state="disable")
        self.typeOfLoanEntry.config(state="disable")
        self.guarranterCheck.config(state="disable")
        self.okButton.config(state="disable")
        self.approveLoanCheck.config(state="disable")
    
    def enable(self):
        self.approveLoanCheck.config(state="normal")
        self.dateApprovedEntry.config(state="normal")
        self.typeOfLoanEntry.config(state="normal")
        self.guarranterCheck.config(state="normal")
        self.okButton.config(state="normal")
        self.approveLoanCheck.config(state="normal")
    
    def initialStage(self):
        self.typeOfLoanEntry.set("")
        self.dateApprovedEntry.config(state="normal")
        self.dateApprovedEntry.delete(0, 'end')
        self.guarranterCheckVar.set(0)
        self.loanCheckVar.set(0)
        self.enableEntries()
        self.ok=False
        self.checkData()

class GuarrantersPage:
    def __init__(self, pageWindow, parentUpdateStatus = None):
        self.parentUpdateStatus = parentUpdateStatus
        self.mainFrame = Frame(pageWindow)
        self.mainFrame.grid(row=0, column=0, sticky="nsew")

        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)

        self.innerMainFrame = Frame(self.mainFrame)
        self.innerMainFrame.grid(row=0, column=0)

        #initial state of customerphoto  and self.photopath is set to None
        self.customerPhoto = None
        self.photoPath = None
        self.guarranterDetails = None
        self.ok = False

        #heading label of the tab
        addCustomerLabel = Label(self.innerMainFrame, text="Add Guarranter", font="COPPER 15")
        addCustomerLabel.pack(side="top", fill="x", ipady=20)

        #alreadyExistsLabel initially set to empty
        self.instructionLabel = Label(self.innerMainFrame, text="", font="COPPER 13")
        self.instructionLabel.pack(side="top", fill="x",ipady=10)

        #created mainFrame which will hold everything of AddCustomer page
        subFrame = Frame(self.innerMainFrame)
        subFrame.pack(fill="both", expand=True)

        #congiguring row 0, 1 and column 0 to make the center in the frame
        subFrame.rowconfigure(0, weight=1)
        subFrame.columnconfigure(0, weight=1)
        subFrame.rowconfigure(1, weight=1)

        #creating subframe
        innersubFrame = Frame(subFrame,width=200, height=200)
        innersubFrame.grid(row=0, column=0)

        labelFgColor = "yellow"
        labelBgColor = "black"

        #naming labels creation in the subframe
        guarranterNameLabel = Label(innersubFrame, text="Guarranter Name : ")
        guarranterNameLabel.grid(row=0, column=0)

        aadharLabel = Label(innersubFrame, text="Aadhar Number : ")
        aadharLabel.grid(row=1, column=0)

        mobileLabel = Label(innersubFrame, text="Mobile : ")
        mobileLabel.grid(row=2, column=0)

        fatherNameLabel = Label(innersubFrame, text="Father Name : ")
        fatherNameLabel.grid(row=3, column=0)

        homeAddressLabel = Label(innersubFrame, text="Home Address : ")
        homeAddressLabel.grid(row=4, column=0)

        WorkAddressLabel = Label(innersubFrame, text="Work Address : ")
        WorkAddressLabel.grid(row=5, column=0)

        photoLabel = Label(innersubFrame, text="Photo : ")
        photoLabel.grid(row=6, column=0)

        #creating entries corresponding to their names labels
        self.gNameVar = StringVar()
        self.gNameEntry = Entry(innersubFrame, width=14, textvariable=self.gNameVar)
        self.gNameEntry.grid(row=0, column=1)

        self.aadharVar = StringVar()
        self.aadharEntry = Entry(innersubFrame, width=14, textvariable=self.aadharVar)
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

        self.mobileVar = StringVar()
        self.mobileEntry = Entry(innersubFrame, width=14, textvariable=self.mobileVar)
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


        self.fNameVar = StringVar()
        self.fNameEntry = Entry(innersubFrame, width=14, textvariable=self.fNameVar)
        self.fNameEntry.grid(row=3, column=1)

        self.hAddressVar = StringVar()
        self.hAddressEntry = Entry(innersubFrame, width=14, textvariable=self.hAddressVar)
        self.hAddressEntry.grid(row=4, column=1)

        self.wAddressVar = StringVar()
        self.wAddressEntry = Entry(innersubFrame, width=14, textvariable=self.wAddressVar)
        self.wAddressEntry.grid(row=5, column=1)
        self.customerPhotoLabel = Label(innersubFrame, image=self.customerPhoto)

        #this function changes widhth of entries according to the no. of characters present in entry
        #it takes two parameter one is event(default para) and one is entryList(necessary) which contains all entries whose width shouild be chnaged
        
        def dynamicWidth(event, entryList):
            #intitially condition is set to True 
            condition=True
            
            #empty which will hold the length of character present in a entry with more than 10 characters
            lengthEntryList = list()
            #traversing through all entries
            for entry in entryList:
                #checking if any one entry has no. of character more than 10
                if(len(entry.get())>10):
                    lengthEntryList.append(len(entry.get()))
                    condition=False

           
            #if condition is true till now that means none of the entry in entryList has length of characters more than 13 so we set the width of all entries to 14
            
            if(condition):
                #traversing through all entries
                for otherEntry in entryList:
                        #configuring widht of entries
                        otherEntry.config(width=14)
            #ELSE widht of all entries will be configured to maxlength on any one entry
            else:
                maxLength = max(lengthEntryList)
                for entry in entryList:
                    entry.config(width=maxLength+10)

        #creating entryList variable containing all entry widgets whom we wnat to enable dynamic width
        entryList = [self.gNameEntry, self.aadharEntry, self.mobileEntry, self.fNameEntry, self.hAddressEntry, self.wAddressEntry]

        #traversing through all entry widgets present in entryList
        for entry in entryList:
            #binding each and everyEntry to Key event and function func is set to dynamicWidth
            #lambda is used to make anonymous function syntax : lambda arguments : expression
            entry.bind("<Key>", func= lambda event, entryList=entryList: dynamicWidth(event, entryList))

        #this function helps to selec images and display on the screen
        def photoSelect():
            #this self.photopath variable stores the path of image of customer
            self.photoPath = askopenfilename(title="Select Customer's Photo", initialdir="/",filetypes=(("PNG", "*.png"),("JPG", "jpg")), multiple=False)
            
            #if photopath is not empty then only it will proceed
            if(self.photoPath):
                #creating a PIL image object
                img=Image.open(self.photoPath)
                #resizing the image
                img=img.resize((82,80))

                #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
                self.customerPhoto = ImageTk.PhotoImage(img)

                #now integrating the image into label widget and positioning it via grid 
                self.customerPhotoLabel = Label(innersubFrame, image=self.customerPhoto)
                self.customerPhotoLabel.grid(row=6, column=1, pady=4)

                #changing the text of photoUploadButton from 'select' to 'Change' and also changing its position in the grid
                self.photoSelectButton.config(text="Change")
                self.photoSelectButton.grid(row=7, column=1)
            
        #this button will be used to upload photos
        self.photoSelectButton = Button(innersubFrame, text="Select", font="COPPER 8", width=13, command=photoSelect)
        self.photoSelectButton.grid(row=6, column=1)

        

        #this checkAndSaveButton
        self.okButton = Button(subFrame, text="Ok", command=self.checkData)
        self.okButton.grid(row=1, column=0, pady=10, sticky="nswe")

       
    def updateStatus(self):
        if(self.parentUpdateStatus):
            self.parentUpdateStatus()

    #checkAndSave function for checking if all fields are filled properly and the customers already exists or not. if not exists then save it to database along with the necessary details
    def checkData(self):
        #checking if the fields are filled properly
        if((not self.gNameEntry.get())):
            requirementsFilled=False
            instructionText = "Please fill Guarranter's Name Field"
        elif(((not self.aadharEntry.get().isdigit()) or (len(self.aadharEntry.get())!=12))):
            requirementsFilled=False
            instructionText = "Please Fill Right Format of Aadhar"
        elif((not self.mobileEntry.get().isdigit()) or (len(self.mobileEntry.get())!=10)):
            requirementsFilled=False
            instructionText = "Please Fill Right Format of Mobile"
        elif((not self.fNameEntry.get())):
            requirementsFilled=False
            instructionText = "Please fill Father's Name Field"
        elif((not self.hAddressEntry.get())):
            requirementsFilled=False
            instructionText = "Please fill Home Address Field"
        elif((not self.wAddressEntry.get())):
            requirementsFilled=False
            instructionText = "Please fill work address Field"
        else:
            instructionText = ""
            requirementsFilled=True
        
        if(requirementsFilled):
            self.guarranterDetails = (self.gNameVar.get(), self.aadharVar.get(), self.fNameVar.get(), self.mobileVar.get(), self.hAddressVar.get(), self.wAddressVar.get(), self.photoPath)
            self.ok=True
            self.instructionLabel.config(text=instructionText)
            self.updateStatus()
            self.disable()

        else:
            self.instructionLabel.config(text=instructionText, fg="red")
    
    def disable(self):
        self.gNameEntry.config(state='disable')
        self.aadharEntry.config(state="disable")
        self.fNameEntry.config(state="disable")
        self.wAddressEntry.config(state="disable")
        self.hAddressEntry.config(state="disable")
        self.mobileEntry.config(state="disable")
        self.okButton.config(state="disable")
        self.photoSelectButton.config(state="disable")

    def enable(self):
        self.gNameEntry.config(state='normal')
        self.aadharEntry.config(state="normal")
        self.fNameEntry.config(state="normal")
        self.wAddressEntry.config(state="normal")
        self.hAddressEntry.config(state="normal")
        self.mobileEntry.config(state="normal")
        self.okButton.config(state="normal")
        self.photoSelectButton.config(state="normal")
    
    def initialStage(self):
        self.enable()
        self.ok=False
        self.gNameEntry.delete(0, END)
        self.aadharEntry.delete(0, END)
        self.fNameEntry.delete(0, END)
        self.wAddressEntry.delete(0, END)
        self.hAddressEntry.delete(0, END)
        self.mobileEntry.delete(0, END)
        self.customerPhotoLabel.destroy()
        self.instructionLabel.pack_forget()
        self.instructionLabel.pack(side="top", fill="x",ipady=10)
        self.photoSelectButton.grid(row=6, column=1)
        self.disable()
        

class DocVerifyPage:
    def __init__(self, pageWindow, parentUpdateStatus=None):
        self.parentUpdateStatus = parentUpdateStatus
        self.mainFrame = Frame(pageWindow)
        self.mainFrame.grid(row=0, column=0, sticky="nsew")

        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)

        self.innerMainFrame = Frame(self.mainFrame, borderwidth=2, relief="raised")
        self.innerMainFrame.grid(row=0, column=0)

        self.ok = False

        self.headingLabel = Label(self.innerMainFrame, text="Documents verification page", font="COPPER 15")
        self.headingLabel.pack(fill="x")

        self.instructionLabel = Label(self.innerMainFrame, text="")
        self.instructionLabel.pack(fill="x")

        self.documentsFrame = Frame(self.innerMainFrame)
        self.documentsFrame.pack(fill="both", expand=True)

        self.documentsLabel = Label(self.documentsFrame, text="Documents", font="COPPER 12 bold")
        self.documentsLabel.grid(row=0, column=0)

        self.docRequireLabel = Label(self.documentsFrame, text="Required", font="COPPER 12 bold")
        self.docRequireLabel.grid(row=0, column=1)

        self.docVerifiedLabel = Label(self.documentsFrame, text="Verified", font="COPPER 12 bold")
        self.docVerifiedLabel.grid(row=0, column=2)

        self.aadharDocLabel = Label(self.documentsFrame, text="Aadhar")
        self.aadharDocLabel.grid(row=1, column=0)

        self.pancardDocLabel = Label(self.documentsFrame, text="Pancard")
        self.pancardDocLabel.grid(row=2, column=0)
        
        self.chequeDocLabel = Label(self.documentsFrame, text="Cheque")
        self.chequeDocLabel.grid(row=3, column=0)

        self.stampDocLabel = Label(self.documentsFrame, text="Stamp")
        self.stampDocLabel.grid(row=4, column=0)

        self.mobileDocLabel = Label(self.documentsFrame, text="Mobile no.")
        self.mobileDocLabel.grid(row=5, column=0)

        self.rcDocLabel = Label(self.documentsFrame, text="RC")
        self.rcDocLabel.grid(row=6, column=0)

        self.aadharReqVar = IntVar()
        self.aadharReqCheck = Checkbutton(self.documentsFrame, variable=self.aadharReqVar)
        self.aadharReqCheck.grid(row=1, column=1)

        self.aadharVerifyVar = IntVar()
        self.aadharVerifyCheck = Checkbutton(self.documentsFrame, variable=self.aadharVerifyVar)
        self.aadharVerifyCheck.grid(row=1, column=2)

        self.pancardReqVar = IntVar()
        self.pancardReqCheck = Checkbutton(self.documentsFrame, variable=self.pancardReqVar)
        self.pancardReqCheck.grid(row=2, column=1)

        self.pancardVerifyVar = IntVar()
        self.pancardVerifyCheck = Checkbutton(self.documentsFrame, variable=self.pancardVerifyVar)
        self.pancardVerifyCheck.grid(row=2, column=2)

        self.chequeReqVar = IntVar()
        self.chequeReqCheck = Checkbutton(self.documentsFrame, variable=self.chequeReqVar)
        self.chequeReqCheck.grid(row=3, column=1)

        self.chequeVerifyVar = IntVar()
        self.chequeVerifyCheck = Checkbutton(self.documentsFrame, variable=self.chequeVerifyVar)
        self.chequeVerifyCheck.grid(row=3, column=2)

        self.stampReqVar = IntVar()
        self.stampReqCheck = Checkbutton(self.documentsFrame, variable=self.stampReqVar)
        self.stampReqCheck.grid(row=4, column=1)

        self.stampVerifyVar = IntVar()
        self.stampVerifyCheck = Checkbutton(self.documentsFrame, variable=self.stampVerifyVar)
        self.stampVerifyCheck.grid(row=4, column=2)

        self.mobileReqVar = IntVar()
        self.mobileReqCheck = Checkbutton(self.documentsFrame, variable=self.mobileReqVar)
        self.mobileReqCheck.grid(row=5, column=1)

        self.mobileVerifyVar = IntVar()
        self.mobileVerifyCheck = Checkbutton(self.documentsFrame, variable=self.mobileVerifyVar)
        self.mobileVerifyCheck.grid(row=5, column=2)

        self.rcReqVar = IntVar()
        self.rcReqCheck = Checkbutton(self.documentsFrame, variable=self.rcReqVar)
        self.rcReqCheck.grid(row=6, column=1)

        self.rcVerifyVar = IntVar()
        self.rcVerifyCheck = Checkbutton(self.documentsFrame, variable=self.rcVerifyVar)
        self.rcVerifyCheck.grid(row=6, column=2)

        self.okButton = Button(self.documentsFrame, text="Ok", command=self.checkData)
        self.okButton.grid(row=7, column=1, sticky="we")
            
    def updateStatus(self):
        if(self.parentUpdateStatus):
            self.parentUpdateStatus()
    
    def checkData(self):
        self.aadharReqCheck.config(state="disable")
        self.aadharVerifyCheck.config(state="disable")
        self.rcVerifyCheck.config(state="disable")
        self.rcReqCheck.config(state="disable")
        self.pancardReqCheck.config(state="disable")
        self.pancardVerifyCheck.config(state="disable")
        self.stampReqCheck.config(state="disable")
        self.stampVerifyCheck.config(state="disable")
        self.mobileReqCheck.config(state="disable")
        self.mobileVerifyCheck.config(state="disable")
        self.chequeReqCheck.config(state="disable")
        self.chequeVerifyCheck.config(state="disable")
        self.okButton.config(state="disable")
        self.ok = True
        self.updateStatus()
    
    def disable(self):
        self.aadharReqCheck.config(state="disable")
        self.aadharVerifyCheck.config(state="disable")
        self.rcVerifyCheck.config(state="disable")
        self.rcReqCheck.config(state="disable")
        self.pancardReqCheck.config(state="disable")
        self.pancardVerifyCheck.config(state="disable")
        self.stampReqCheck.config(state="disable")
        self.stampVerifyCheck.config(state="disable")
        self.mobileReqCheck.config(state="disable")
        self.mobileVerifyCheck.config(state="disable")
        self.chequeReqCheck.config(state="disable")
        self.chequeVerifyCheck.config(state="disable")
        self.okButton.config(state="disable")
    
    def enable(self):
        self.aadharReqCheck.config(state="normal")
        self.aadharVerifyCheck.config(state="normal")
        self.rcVerifyCheck.config(state="normal")
        self.rcReqCheck.config(state="normal")
        self.pancardReqCheck.config(state="normal")
        self.pancardVerifyCheck.config(state="normal")
        self.stampReqCheck.config(state="normal")
        self.stampVerifyCheck.config(state="normal")
        self.mobileReqCheck.config(state="normal")
        self.mobileVerifyCheck.config(state="normal")
        self.chequeReqCheck.config(state="normal")
        self.chequeVerifyCheck.config(state="normal")
        self.okButton.config(state="normal")
    
    def initialStage(self):
        self.enable()
        self.aadharReqVar.set(0)
        self.aadharVerifyVar.set(0)
        self.pancardReqVar.set(0)
        self.pancardVerifyVar.set(0)
        self.chequeReqVar.set(0)
        self.chequeVerifyVar.set(0)
        self.stampReqVar.set(0)
        self.stampVerifyVar.set(0)
        self.ok=False
        self.mobileReqVar.set(0)
        self.mobileVerifyVar.set(0)
        self.rcReqVar.set(0)
        self.rcVerifyVar.set(0)
        self.disable()

class VehiclesPage:
    def __init__(self, pageWindow, parentUpdateStatus=None):
        self.parentUpdateStatus = parentUpdateStatus
        self.mainFrame = Frame(pageWindow)
        self.mainFrame.grid(row=0, column=0, sticky="nsew")

        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)

        self.innerMainFrame = Frame(self.mainFrame, borderwidth=2, relief="raised")
        self.innerMainFrame.grid(row=0, column=0)

        self.ok = False

        self.instructionLabel = Label(self.innerMainFrame, text="")
        self.instructionLabel.pack(fill="x")

        self.vehicleDetailsFrame = Frame(self.innerMainFrame)
        self.vehicleDetailsFrame.pack(fill="both", expand=1)

        self.operationFrame = Frame(self.innerMainFrame)
        self.operationFrame.pack(side="bottom", fill="x")

        self.vehicle = None

        self.vNameLable = Label(self.vehicleDetailsFrame, text="Vehicle Name : ")
        self.vNameLable.grid(row=0, column=0)

        self.modelLabel = Label(self.vehicleDetailsFrame, text="Model : ")
        self.modelLabel.grid(row=1, column=0)

        self.manufaturerLabel = Label(self.vehicleDetailsFrame, text="Manufacturer : ")
        self.manufaturerLabel.grid(row=2, column=0)

        self.fuelUsedLabel = Label(self.vehicleDetailsFrame, text="Fuel Used : ")
        self.fuelUsedLabel.grid(row=3, column=0)

        self.engineCCLabel = Label(self.vehicleDetailsFrame, text="Engine (CC) : ")
        self.engineCCLabel.grid(row=4, column=0)

        self.horsePowerLabel = Label(self.vehicleDetailsFrame, text="Horse Power(BHP) : ")
        self.horsePowerLabel.grid(row=5, column=0)

        self.numCyilendersLabel = Label(self.vehicleDetailsFrame, text="No. of Cyilenders : ")
        self.numCyilendersLabel.grid(row=6, column=0)

        self.fuelCapacityLabel = Label(self.vehicleDetailsFrame, text="Fuel Capacity (Litre) : ")
        self.fuelCapacityLabel.grid(row=7, column=0)

        self.seatingCapacityLabel = Label(self.vehicleDetailsFrame, text="Seating Capacity : ")
        self.seatingCapacityLabel.grid(row=8, column=0)

        self.vehicleWeightLabel = Label(self.vehicleDetailsFrame, text="Vehicle Weight (Kg) : ")
        self.vehicleWeightLabel.grid(row=9, column=0)

        self.numberPlateLabel = Label(self.vehicleDetailsFrame, text="Number plate : ")
        self.numberPlateLabel.grid(row=10, column=0)

        self.vNameVar = StringVar()
        self.vNameEntry = Entry(self.vehicleDetailsFrame, textvariable=self.vNameVar, width=14, justify="center")
        self.vNameEntry.grid(row=0, column=1, pady=10)

        self.modelVar = StringVar()
        self.modelEntry = Entry(self.vehicleDetailsFrame, textvariable=self.modelVar, width=14, justify="center")
        self.modelEntry.grid(row=1, column=1, pady=10)

        self.manufacturerVar = StringVar()
        self.manufacturerEntry = ttk.Combobox(self.vehicleDetailsFrame, state="readonly", values=["Hero", "Honda", "Suzuki"], textvariable=self.manufacturerVar, width=12, justify="center")
        self.manufacturerEntry.grid(row=2, column=1, pady=10)

        self.fuelUsedVar = StringVar()
        self.fuelUsedEntry = ttk.Combobox(self.vehicleDetailsFrame, state="readonly", values=["Petrol", "Diesel"], textvariable=self.fuelUsedVar, width=12, justify="center")
        self.fuelUsedEntry.grid(row=3, column=1, pady=10)

        self.engineCCVar = StringVar()
        self.engineCCEntry = Entry(self.vehicleDetailsFrame, textvariable=self.engineCCVar, width=14, justify="center")
        self.engineCCEntry.grid(row=4, column=1, pady=10)

        self.horsePowerVar = StringVar()
        self.horsePowerEntry = Entry(self.vehicleDetailsFrame, textvariable=self.horsePowerVar, width=14, justify="center")
        self.horsePowerEntry.grid(row=5, column=1, pady=10)

        self.numCyilendersVar = StringVar()
        self.numCyilendersEntry = Entry(self.vehicleDetailsFrame, textvariable=self.numCyilendersVar, width=14, justify="center")
        self.numCyilendersEntry.grid(row=6, column=1, pady=10)

        self.fuelCapacityVar = StringVar()
        self.fuelCapacityEntry = Entry(self.vehicleDetailsFrame, textvariable=self.fuelCapacityVar, width=14, justify="center")
        self.fuelCapacityEntry.grid(row=7, column=1, pady=10)

        self.seatingCapacityVar = StringVar()
        self.seatingCapacityEntry = Entry(self.vehicleDetailsFrame, textvariable=self.seatingCapacityVar, width=14, justify="center")
        self.seatingCapacityEntry.grid(row=8, column=1, pady=10)

        self.vehicleWeightVar = StringVar()
        self.vehicleWeightEntry = Entry(self.vehicleDetailsFrame, textvariable=self.vehicleWeightVar, width=14, justify="center")
        self.vehicleWeightEntry.grid(row=9, column=1, pady=10)

        self.numberPlateVar = StringVar()
        self.numberPlateEntry = Entry(self.vehicleDetailsFrame, textvariable=self.numberPlateVar, width=14, justify="center")
        self.numberPlateEntry.grid(row=10, column=1, pady=10)

        self.operationButton = Button(self.operationFrame, text="Add Vehicle", command=self.checkData)
        self.operationButton.pack(fill="x")
    
    def checkData(self):
        print("vehicle adding process starts")
        if(not self.modelVar.get()):
            requirementsFilled=False
            instructionText = "Model field is necessary"
        elif(not self.manufacturerVar.get()):
            requirementsFilled=False
            instructionText = "Manufacturer field is necessary"
        elif(not self.numberPlateVar.get()):
            requirementsFilled=False
            instructionText = "Number Plate field is necessary"
        else:
            instructionText = "Vehicle added successfully"
            requirementsFilled=True

        if(requirementsFilled):
            print("vehicle added")

            self.modelEntry.config(state="disable")
            self.manufacturerEntry.config(state="disable")
            self.fuelUsedEntry.config(state="disable")
            self.engineCCEntry.config(state="disable")
            self.horsePowerEntry.config(state="disable")
            self.numCyilendersEntry.config(state="disable")
            self.fuelCapacityEntry.config(state="disable")
            self.seatingCapacityEntry.config(state="disable")
            self.vehicleWeightEntry.config(state="disable")
            self.numberPlateEntry.config(state="disable")
            self.operationButton.config(state="disable")

            self.vehicle = [self.modelVar.get(), self.manufacturerVar.get(), self.fuelUsedEntry.get(), self.engineCCVar.get(), self.horsePowerVar.get(), self.numCyilendersVar.get(), self.fuelCapacityVar.get(), self.seatingCapacityVar.get(), self.vehicleWeightVar.get()]
            self.ok = True

            self.updateStatus()

            print(self.vehicle)

            self.instructionLabel.config(text=instructionText, fg="green")        
        else:
            print("vehicle not added")
            self.instructionLabel.config(text=instructionText, fg="red")

    def updateStatus(self):
        if(self.parentUpdateStatus):
            self.parentUpdateStatus()
    
    def disable(self):
        self.modelEntry.config(state="disable")
        self.manufacturerEntry.config(state="disable")
        self.fuelUsedEntry.config(state="disable")
        self.engineCCEntry.config(state="disable")
        self.horsePowerEntry.config(state="disable")
        self.numCyilendersEntry.config(state="disable")
        self.vNameEntry.config(state="disable")
        self.fuelCapacityEntry.config(state="disable")
        self.seatingCapacityEntry.config(state="disable")
        self.vehicleWeightEntry.config(state="disable")
        self.operationButton.config(state="disable")
        self.numberPlateEntry.config(state="disable")

    def enable(self):
        self.vNameEntry.config(state="normal")
        self.modelEntry.config(state="normal")
        self.manufacturerEntry.config(state="normal")
        self.fuelUsedEntry.config(state="normal")
        self.engineCCEntry.config(state="normal")
        self.horsePowerEntry.config(state="normal")
        self.numCyilendersEntry.config(state="normal")
        self.fuelCapacityEntry.config(state="normal")
        self.seatingCapacityEntry.config(state="normal")
        self.vehicleWeightEntry.config(state="normal")
        self.operationButton.config(state="normal")
        self.numberPlateEntry.config(state="normal")

    def initialStage(self):
        self.enable()
        self.ok=False
        self.modelEntry.delete(0, END)
        self.vNameEntry.delete(0, END)
        self.manufacturerEntry.delete(0, END)
        self.fuelUsedEntry.delete(0, END)
        self.engineCCEntry.delete(0, END)
        self.horsePowerEntry.delete(0, END)
        self.numCyilendersEntry.delete(0, END)
        self.fuelCapacityEntry.delete(0, END)
        self.seatingCapacityEntry.delete(0, END)
        self.instructionLabel.config(text="")
        self.vehicleWeightEntry.delete(0, END)
        self.numberPlateEntry.delete(0, END)
        self.disable()

class finalPage:
    def __init__(self, pageWindow, parentUpdateStatus=None):
        self.loanPassed = False
        self.parentUpdateStatus = parentUpdateStatus
        self.mainFrame = Frame(pageWindow)
        self.mainFrame.grid(row=0, column=0, sticky="nsew")

        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)
        self.mainFrame.rowconfigure(3, weight=1)
        self.mainFrame.rowconfigure(4, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)

        self.firstInnerMainFrame = Frame(self.mainFrame, borderwidth=2, relief="raised" , width=450, height=150)
        self.firstInnerMainFrame.grid(row=0, column=0, sticky="nsew")

        self.firstInnerMainFrame.rowconfigure(0, weight=1)
        self.firstInnerMainFrame.columnconfigure(0, weight=1)

        self.firstInnerMainFrame.grid_propagate(False)

        self.innerMainFrame = Frame(self.firstInnerMainFrame, borderwidth=2)
        self.innerMainFrame.grid(row=0,column=0)
        

        self.secondInnerMainFrame = Frame(self.mainFrame, borderwidth=2, relief="raised")
        self.secondInnerMainFrame.grid(row=1, column=0, sticky="nsew", rowspan=4)

        self.instructionLabel = Label(self.innerMainFrame, text="")
        self.instructionLabel.pack(fill="x")

        self.finalDataFrame =Frame(self.innerMainFrame)
        self.finalDataFrame.pack(fill="both", expand=True)
        
        self.amountApprovedLabel = Label(self.finalDataFrame, text="Amount Approved : ")
        self.amountApprovedLabel.grid(row=0, column=0)

        self.rupeesLabel1 = Label(self.finalDataFrame, text="₹")
        self.rupeesLabel1.grid(row=0, column=2)

        self.interestLabel = Label(self.finalDataFrame, text="Interest : ")
        self.interestLabel.grid(row=1, column=0)

        self.interestPercentLabel = Label(self.finalDataFrame, text="% per annum")
        self.interestPercentLabel.grid(row=1, column=2)

        self.numOfEmi = Label(self.finalDataFrame, text="Num EMI : ")
        self.numOfEmi.grid(row=2, column=0)
        self.loanPeriodLabel = Label(self.finalDataFrame, text="Loan Period : ")
        self.loanPeriodLabel.grid(row=3, column=0)

        self.loanTimeLabel = Label(self.finalDataFrame, text="In months")
        self.loanTimeLabel.grid(row=3, column=2)

        self.installmentAmtLabel = Label(self.finalDataFrame, text="EMI Amount : ")
        self.installmentAmtLabel.grid(row=4, column=0)

        self.rupeesLabel2 = Label(self.finalDataFrame, text="₹ per 30 days")
        self.rupeesLabel2.grid(row=4, column=2)

        self.startDateLabel = Label(self.finalDataFrame, text="Start Date : ")
        self.startDateLabel.grid(row=5, column=0)


        self.saveButton = Button(self.finalDataFrame, text="Loan Pass", bg="light green", command=self.save)
        self.saveButton.grid(row=6, column=0, sticky="we", pady=20, columnspan=3)

        self.amountApprovedVar = StringVar()

        #initialValue 
        self.amountApprovedEntry = Entry(self.finalDataFrame, textvariable=self.amountApprovedVar, justify="center")
        self.amountApprovedEntry.grid(row=0, column=1)


        #updating root after creating this many widgets and configurations
        pageWindow.update()

        #event handler for amountApprovedEntry to restrict user from entering letters, character
        def amountApprovedEntryEventHandler(event):
            tempString = ""
            for char in self.amountApprovedEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char
            
            self.amountApprovedEntry.delete(0, "end")
            self.amountApprovedEntry.insert("end", tempString)
            self.dynamicTableDetails()

        self.amountApprovedEntry.bind("<KeyRelease>", amountApprovedEntryEventHandler)


        self.interestVar = StringVar()
        self.interestEntry = Entry(self.finalDataFrame, textvariable=self.interestVar, justify="center")
        self.interestEntry.grid(row=1, column=1)

        #created varialble to store total no.of emis
        self.numOfEmiVar = StringVar()
        self.numOfEmiEntry = Entry(self.finalDataFrame, textvariable=self.numOfEmiVar, justify="center")
        self.numOfEmiEntry.grid(row=2, column=1) 

        # Eventhandlere for numOfEmiEntry
        def numOfEmiEntryHandler(event):
            tempString = ""
            for char in self.numOfEmiEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char
            
            self.numOfEmiEntry.delete(0, "end")
            self.numOfEmiEntry.insert("end", tempString)
            self.dynamicTableDetails()

        self.numOfEmiEntry.bind("<KeyRelease>", numOfEmiEntryHandler)

        #event handler for amountApprovedEntry to restrict user from entering letters, character
        def interestEntryEventHandler(event):
            tempString = ""
            for char in self.interestEntry.get():
                if(not (char.isdigit() or char==".")):
                    pass
                elif((char.isdigit() or char==".")):
                    tempString+=char
            
            self.interestEntry.delete(0, "end")
            self.interestEntry.insert("end", tempString)
            self.dynamicTableDetails()

        self.interestEntry.bind("<KeyRelease>", interestEntryEventHandler)

        self.loanPeriodVar = StringVar()
        self.loanPeriodEntry = Entry(self.finalDataFrame, textvariable=self.loanPeriodVar, justify="center")
        self.loanPeriodEntry.grid(row=3, column=1)

        #event handler for amountApprovedEntry to restrict user from entering letters, character
        def loanPeriodEntryEventHandler(event):
            tempString = ""
            for char in self.loanPeriodEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char
        
            self.loanPeriodEntry.delete(0, "end")
            self.loanPeriodEntry.insert("end", tempString)
            self.dynamicTableDetails()

        self.loanPeriodEntry.bind("<KeyRelease>", loanPeriodEntryEventHandler)


        self.installmentAmtVar = StringVar()
        self.installmentAmtEntry = Entry(self.finalDataFrame, textvariable=self.installmentAmtVar, justify="center")
        self.installmentAmtEntry.grid(row=4, column=1)

        #event handler for amountApprovedEntry to restrict user from entering letters, character
        def installmentAmtEntryEventHandler(event):
            tempString = ""
            for char in self.installmentAmtEntry.get():
                if(not char.isdigit()):
                    pass
                elif(char.isdigit()):
                    tempString+=char
        
            self.installmentAmtEntry.delete(0, "end")
            self.installmentAmtEntry.insert("end", tempString)
            self.dynamicTableDetails()

        self.installmentAmtEntry.bind("<KeyRelease>", installmentAmtEntryEventHandler)

        self.startDateEntry = DateEntry(self.finalDataFrame, width=17, date_pattern="yyyy-mm-dd", justify="center", state="disable", selectmode="day")
        self.startDateEntry.grid(row=5, column=1)

        #work of secondInnerMainFrame starts here

        #creating a table of emis and dates of that emi
        self.table=ttk.Treeview(self.secondInnerMainFrame)

        #scrollbar for table
        self.tableScrollY = Scrollbar(self.secondInnerMainFrame)
        self.tableScrollY.pack(side="right", fill="y")

        #now packig table
        self.table.pack(fill="both", expand=True)


        #configuring scrollbar and table
        self.table.config(yscrollcommand=self.tableScrollY.set)
        self.tableScrollY.config(command=self.table.yview)

        #creating columns for the table
        self.table["columns"]=("serialNum", "emiDate", "emiAmount")

        #setting up columns
        self.table.column("#0", width=0, minwidth=0, stretch=False)
        self.table.column("serialNum", width=35, minwidth=35, anchor="center", stretch=False)
        self.table.column("emiDate", width=50, minwidth=50, anchor="center")
        self.table.column("emiAmount", width=50, minwidth=50, anchor="center")

        #creating headings for columns to show to user 
        self.table.heading("serialNum", text="S.No.", anchor="center")
        self.table.heading("emiDate", text="EMI Date", anchor="center")
        self.table.heading("emiAmount", text="EMI Amount", anchor="center")

    def save(self):
        self.loanPassed = True
        self.updateStatus()
        
    def updateStatus(self):
        if(self.parentUpdateStatus):
            self.parentUpdateStatus()
    
    def enable(self):
        self.saveButton.config(state="normal")
        self.numOfEmiEntry.config(state="normal")
        self.amountApprovedEntry.config(state="normal")
        self.interestEntry.config(state="normal")
        self.loanPeriodEntry.config(state="normal")
        self.startDateEntry.config(state="readonly")
        self.installmentAmtEntry.config(state="readonly")

    def disable(self):
        self.saveButton.config(state="disable")
        self.amountApprovedEntry.config(state="disable")
        self.interestEntry.config(state="disable")
        self.loanPeriodEntry.config(state="disable")
        self.numOfEmiEntry.config(state="disable")
        self.startDateEntry.config(state="disable")
        self.installmentAmtEntry.config(state="disable")

    def initialStage(self):
        self.enable()
        self.amountApprovedVar.set("")
        self.interestVar.set(INTERESTRATE)
        self.loanPeriodVar.set("")
        self.installmentAmtVar.set("")
        self.installmentAmtEntry.config(state="readonly")
        self.numOfEmiVar.set("")
        self.rupeesLabel2.config(text="₹ per 30 days")
        self.loanPassed=False
        self.startDateEntry.config(state="disable")
        self.table.delete(*self.table.get_children())
        self.disable()

    #this function will dynamically calculate the table data of emis and dates accordingly
    def dynamicTableDetails(self):
        if(self.amountApprovedVar.get() and self.loanPeriodVar.get() and self.numOfEmiVar.get() and self.interestVar.get() and self.numOfEmiVar.get()!="0" and self.startDateEntry.get_date()):

            installment = int((int(self.amountApprovedVar.get())*(int(self.loanPeriodVar.get())/12)*float(self.interestVar.get())/100 + int(self.amountApprovedVar.get()))/int(self.numOfEmiVar.get()))
            self.installmentAmtVar.set(installment)

            timeGap = int(30*int(self.loanPeriodVar.get())/int(self.numOfEmiVar.get()))
            self.rupeesLabel2.config(text=f"₹ per {int(timeGap)} days")

            numOfEmi = int(self.numOfEmiVar.get())
            
            #deleting prexisting data from table
            self.table.delete(*self.table.get_children())

            #inserting new data into the table
            day=self.startDateEntry.get_date().day
            month = self.startDateEntry.get_date().month
            year = self.startDateEntry.get_date().year

            def addDays(year, month, day, n):
                months31 = [1,3,5,7,8,10,12]
                months30 = [4,6,9,11]
                while n >0:
                    if month in months31:
                        if day +n<=31:
                            day+=n
                            n=0
                        else:
                            n-=(31-day)
                            day=1
                            if month == 12:
                                month=1
                                year+=1
                            else:
                                month+=1
                    elif month in months30:
                        if day + n <=30:
                            day+=n
                            n=0
                        else:
                            n-= (30-day)
                            day=1
                            month+=1
                    elif month==2:
                        if (year %4==0 and year%100!=0) or (year % 400 ==0):
                            if day +n<=29:
                                day+=n
                                n=0
                            else:
                                n-= (29-day)
                                day=1
                                month+=1
                        else:
                            if day +n<=28:
                                day+=n
                                n=0
                            else:
                                n-=(28-day)
                                day=1
                                month+=1
                return year, month, day

            for i in range(numOfEmi):
                self.table.insert(parent="", text="", iid=i, index="end", values=(i+1, f"{year}-{month}-{day}", installment))        
                date=addDays(year, month, day, int(timeGap))
                year=date[0]
                month=date[1]
                day=date[2]

        else:
            self.installmentAmtVar.set("")

            #deleting prexisting data from table
            self.table.delete(*self.table.get_children())

if __name__=="__main__":
    root = Tk()
    root.geometry("599x499")
    root.title("add new file")
    object = AddFile(root)
    root.mainloop()
