#importing necessary modules and components and clases
from tkinter import Tk, Frame, Label, Listbox, Scrollbar, END, Checkbutton, IntVar, StringVar, Entry, Button, Text, ttk,  DoubleVar
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from sys import path
path.append(r"D:\projects\finoshok\finoshok\model")
path.append(r"D:\projects\finoshok\finoshok\config")
from pathConfig import CUSTOMERPHOTOPATH
#now we can import Customer and Requests class successfully from customer model and Rewusts model respectively
from Customer import Customer
from File import File
from Ledger import Ledger
from Requests import Requests


#AddFile class needs a parameter either a tk window or frame
class AddFile:
    def __init__(self, addFileWindow):
        #create mainframe containing everything
        mainFrame = Frame(addFileWindow)
        mainFrame.pack(fill="both", expand=True)

        #columnconfigure() resizes the grid vertically, while rowconfigure() resizes the grid horizontally. The width of a grid column is equal to the width of its widest cell.

        mainFrame.rowconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=1)
        
        #created subframes
        
        #The sticky parameter in the .grid() method of Tkinter is used to define how a widget should expand to fill the space allocated to it within a grid cell.

        subFrame1 = Frame(mainFrame, relief="groove", border=3)
        subFrame1.grid(row=0, column=0, sticky="ewns")
        subFrame1.pack_propagate(False)

        subFrame2 = Frame(mainFrame, relief="groove", border=3)
        subFrame2.grid(row=0, column=1, sticky="ewns", rowspan=2)
        subFrame2.pack_propagate(False)
        #creating a subframe2 as more responsive  using rowconfigure and columnconfigure

        subFrame2.rowconfigure(0, weight=1)
        subFrame2.columnconfigure(0, weight=1)

        subFrame3 = Frame(mainFrame, relief="groove", border=3)
        subFrame3.grid(row=1, column=0, sticky="ewns")  
        subFrame3.pack_propagate(False)

        #now creating 3 sections : 

        #section 1 for selecting any one loan requests also adding heading/label
        self.searchFrame = Frame(subFrame1)
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
        scrollY = Scrollbar(subFrame1)
        scrollY.pack(side="right", fill="y")

        self.section1 = Frame(subFrame1)
        self.section1.pack(fill="both", expand=True) 

        #section 2 for loan confirmation along with some formalities
        self.section2 = Frame(subFrame2)
        self.section2.pack(fill="both", expand=True)

        #section 3 for showing selected loan request details along with some customer details

        self.section3 = Frame(subFrame3)
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

        scrollY.config(command=self.customerRequestBox.yview)
        self.customerRequestBox.config(yscrollcommand=scrollY.set)

        #creating scrollbar for x dirextion
        scrollX = Scrollbar(subFrame1, command=self.customerRequestBox.xview, orient="horizontal")
        scrollX.pack(side="bottom", fill="x")
        self.customerRequestBox.config(xscrollcommand=scrollX.set)
        
        self.dataList = []
        self.tempDataList = []

        #section 1 work ends----
        
        #section 2 work starts ----
        self.section2.rowconfigure(0, weight=1)
        self.section2.columnconfigure(0, weight=1)

        self.pagesList = [ApprovalPage(self.section2, parentUpdateStatus=self.updateStatus), GuarrantersPage(self.section2, parentUpdateStatus=self.updateStatus), VehiclesPage(self.section2, parentUpdateStatus=self.updateStatus), DocVerifyPage(self.section2, parentUpdateStatus=self.updateStatus), finalPage(self.section2, parentUpdateStatus=self.updateStatus)]

        self.changePage(0)
        operationFrame = Frame(subFrame2)
        operationFrame.pack(side="bottom", fill="x")

        operationFrame.rowconfigure(0, weight=1)
        operationFrame.columnconfigure(0, weight=1)
        operationFrame.columnconfigure(1, weight=1)
        operationFrame.columnconfigure(2, weight=1)

        self.cancelButton = Button(operationFrame, text="Cancel", command=self.cancelMethod)
        self.cancelButton.grid(row=0, column=0, sticky="ew")

        self.backButton = Button(operationFrame, text="Back", command=self.backPage)
        self.backButton.grid(row=0, column=1, sticky="ew")

        self.nextButton = Button(operationFrame, text="Next", bg="orange", command=self.nextPage)
        self.nextButton.grid(row=0, column=2, sticky="we")

        #section 2 work endss ----
            
        #self.section3 work starts ----

        self.section3.rowconfigure(0, weight=1)
        self.section3.columnconfigure(0, weight=1)

        self.customerDetailsFrame = Frame(self.section3, border=1, relief="raised")
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

        purposeLabel = Label(self.customerDetailsFrame, text="Purpose of Loan : ")
        purposeLabel.grid(row=1, column=0)

        #creating labels dynamic
        self.customerEntryVar = StringVar()
        self.customerEntryVar.set("name")
        customerEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.customerEntryVar)
        customerEntry.grid(row=0, column=1)

        self.aadharEntryVar = StringVar()
        self.aadharEntryVar.set("aadhar")
        aadharEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.aadharEntryVar)
        aadharEntry.grid(row=1, column=1)

        self.mobileEntryVar = StringVar()
        self.mobileEntryVar.set("mobile")
        mobileEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.mobileEntryVar)
        mobileEntry.grid(row=2, column=1)

        self.fatherEntryVar = StringVar()
        self.fatherEntryVar.set("father")
        fatherEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.fatherEntryVar)
        fatherEntry.grid(row=3, column=1)

        self.homeAddressEntryVar = StringVar()
        self.homeAddressEntryVar.set("homeAddress")
        homeAddressEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.homeAddressEntryVar)
        homeAddressEntry.grid(row=4, column=1)

        self.workAddressEntryVar = StringVar()
        self.workAddressEntryVar.set("workAddress")
        workAddressEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.workAddressEntryVar)
        workAddressEntry.grid(row=5, column=1)

        self.purposeEntry = Text(self.customerDetailsFrame, width=40, height=10)
        self.purposeEntry.grid(row=1, column=1)
        #self.section3 workd ends----

        #initially invoking search funtion
        self.refresh()
        self.customerRequestBox.selection_set(0)
        self.customerRequestBox.focus(0)
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
    
    #refresh button replenis new data in self.data and renews items in listbox of requests
    def refresh(self):
        #reading the all data of requests from database
        requestsData = Requests().readAllData()

        customerObject = Customer()
        self.dataList = []

        #updating self.datalist and self.customerRequestBox
        for request in requestsData:
            tempCustomerData = customerObject.whereData(id=request[1])

            self.dataList.append({"customerId":tempCustomerData[0][0], "aadhar":tempCustomerData[0][6], "name":tempCustomerData[0][1], "father":tempCustomerData[0][2], "mobile":tempCustomerData[0][3], "homeAddress":tempCustomerData[0][4], "workAddress": tempCustomerData[0][5], "status":request[5], "purpose":request[3], "amountRequested": request[2], "dateRequested":request[4]})

        self.searchEntry.delete(0, "end")
        self.search(None)
        self.customerRequestBox.selection_set(0)
        self.customerRequestBox.focus(0)
        self.dynamicDetails(None)

        
        #now restarting the dynamic details 
        self.customerRequestBox.selection_set(0)
        self.dynamicDetails(None)
    
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
            if(self.pagesList[0].typeOfLoanEntry.get()=="Loan on vehicle"):
                self.pagesList[2].enable()
            else:
                self.pagesList[2].disable()
        
        if(self.pagesList[4].loanPassed):
            print("loanPassed")
            if(self.pagesList[0].ok==True):
                if(self.pagesList[0].guarranterCheckVar.get()==1 and self.pagesList[0].typeOfLoanEntry.get()=="Loan on vehicle"):
                    if(self.pagesList[1].ok and self.pagesList[2].ok):
                        pass
                    else:
                        print("fil necessary things")
                elif(self.pagesList[0].guarranterCheckVar.get()==1 and self.pagesList[0].typeOfLoanEntry.get()=="Personal Loan"):
                    if(self.pagesList[1].ok):
                        pass
                    else:
                        print("fil necessary things")
                elif(self.pagesList[0].typeOfLoanEntry.get() == "Loan on vehicle" and not self.pagesList[0].guarranterCheckVar.get()):
                    if(self.pagesList[2].ok):
                        pass
                    else:
                        print("fil necessary things")
                else:
                    pass
            else:
                print("hello")

    
    def backPage(self):
        self.changePage(self.currentPageIndex-1)

    def nextPage(self):
        self.changePage(self.currentPageIndex+1)
        
    def cancelMethod(self):
        children = self.section2.winfo_children()
        for page in children:
            page.destroy()
        del self.pagesList
        self.pagesList = [ApprovalPage(self.section2, parentUpdateStatus=self.updateStatus), GuarrantersPage(self.section2, parentUpdateStatus=self.updateStatus), VehiclesPage(self.section2, parentUpdateStatus=self.updateStatus), DocVerifyPage(self.section2, parentUpdateStatus=self.updateStatus), finalPage(self.section2, parentUpdateStatus=self.updateStatus)]
        self.pagesList[1].disable()
        self.pagesList[2].disable()
        
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
                print("fill necessar details")
        
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

        self.mobileVar = StringVar()
        self.mobileEntry = Entry(innersubFrame, width=14, textvariable=self.mobileVar)
        self.mobileEntry.grid(row=2, column=1)

        self.fNameVar = StringVar()
        self.fNameEntry = Entry(innersubFrame, width=14, textvariable=self.fNameVar)
        self.fNameEntry.grid(row=3, column=1)

        self.hAddressVar = StringVar()
        self.hAddressEntry = Entry(innersubFrame, width=14, textvariable=self.hAddressVar)
        self.hAddressEntry.grid(row=4, column=1)

        self.wAddressVar = StringVar()
        self.wAddressEntry = Entry(innersubFrame, width=14, textvariable=self.wAddressVar)
        self.wAddressEntry.grid(row=5, column=1)

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
            requirementsFilled=True
        
        if(requirementsFilled):
            self.gNameEntry.config(state='disable')
            self.aadharEntry.config(state="disable")
            self.fNameEntry.config(state="disable")
            self.wAddressEntry.config(state="disable")
            self.hAddressEntry.config(state="disable")
            self.mobileEntry.config(state="disable")
            self.okButton.config(state="disable")
            self.photoSelectButton.config(state="disable")
            self.guarranterDetails = (self.gNameVar.get(), self.aadharVar.get(), self.fNameVar.get(), self.mobileVar.get(), self.hAddressVar.get(), self.wAddressVar.get(), self.photoPath)
            self.ok=True
            self.updateStatus()

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

        self.modelLabel = Label(self.vehicleDetailsFrame, text="Model : ")
        self.modelLabel.grid(row=0, column=0)

        self.manufaturerLabel = Label(self.vehicleDetailsFrame, text="Manufacturer : ")
        self.manufaturerLabel.grid(row=1, column=0)

        self.fuelUsedLabel = Label(self.vehicleDetailsFrame, text="Fuel Used : ")
        self.fuelUsedLabel.grid(row=2, column=0)

        self.engineCCLabel = Label(self.vehicleDetailsFrame, text="Engine (CC) : ")
        self.engineCCLabel.grid(row=3, column=0)

        self.horsePowerLabel = Label(self.vehicleDetailsFrame, text="Horse Power(BHP) : ")
        self.horsePowerLabel.grid(row=4, column=0)

        self.numCyilendersLabel = Label(self.vehicleDetailsFrame, text="No. of Cyilenders : ")
        self.numCyilendersLabel.grid(row=5, column=0)

        self.fuelCapacityLabel = Label(self.vehicleDetailsFrame, text="Fuel Capacity (Litre) : ")
        self.fuelCapacityLabel.grid(row=6, column=0)

        self.seatingCapacityLabel = Label(self.vehicleDetailsFrame, text="Seating Capacity : ")
        self.seatingCapacityLabel.grid(row=7, column=0)

        self.vehicleWeightLabel = Label(self.vehicleDetailsFrame, text="Vehicle Weight (Kg) : ")
        self.vehicleWeightLabel.grid(row=8, column=0)

        self.numberPlateLabel = Label(self.vehicleDetailsFrame, text="Number plate : ")
        self.numberPlateLabel.grid(row=9, column=0)

        self.modelVar = StringVar()
        self.modelEntry = Entry(self.vehicleDetailsFrame, textvariable=self.modelVar, width=14, justify="center")
        self.modelEntry.grid(row=0, column=1, pady=10)

        self.manufaturerVar = StringVar()
        self.manufacturerEntry = ttk.Combobox(self.vehicleDetailsFrame, state="readonly", values=["Hero", "Honda", "Suzuki"], textvariable=self.manufaturerVar, width=12, justify="center")
        self.manufacturerEntry.grid(row=1, column=1, pady=10)

        self.fuelUsedVar = StringVar()
        self.fuelUsedEntry = ttk.Combobox(self.vehicleDetailsFrame, state="readonly", values=["Petrol", "Diesel"], textvariable=self.fuelUsedVar, width=12, justify="center")
        self.fuelUsedEntry.grid(row=2, column=1, pady=10)

        self.engineCCVar = DoubleVar()
        self.engineCCEntry = Entry(self.vehicleDetailsFrame, textvariable=self.engineCCVar, width=14, justify="center")
        self.engineCCEntry.grid(row=3, column=1, pady=10)

        self.horsePowerVar = DoubleVar()
        self.horsePowerEntry = Entry(self.vehicleDetailsFrame, textvariable=self.horsePowerVar, width=14, justify="center")
        self.horsePowerEntry.grid(row=4, column=1, pady=10)

        self.numCyilendersVar = IntVar()
        self.numCyilendersEntry = Entry(self.vehicleDetailsFrame, textvariable=self.numCyilendersVar, width=14, justify="center")
        self.numCyilendersEntry.grid(row=5, column=1, pady=10)

        self.fuelCapacityVar = DoubleVar()
        self.fuelCapacityEntry = Entry(self.vehicleDetailsFrame, textvariable=self.fuelCapacityVar, width=14, justify="center")
        self.fuelCapacityEntry.grid(row=6, column=1, pady=10)

        self.seatingCapacityVar = IntVar()
        self.seatingCapacityEntry = Entry(self.vehicleDetailsFrame, textvariable=self.seatingCapacityVar, width=14, justify="center")
        self.seatingCapacityEntry.grid(row=7, column=1, pady=10)

        self.vehicleWeightVar = DoubleVar()
        self.vehicleWeightEntry = Entry(self.vehicleDetailsFrame, textvariable=self.vehicleWeightVar, width=14, justify="center")
        self.vehicleWeightEntry.grid(row=8, column=1, pady=10)

        self.numberPlateVar = StringVar()
        self.numberPlateEntry = Entry(self.vehicleDetailsFrame, textvariable=self.numberPlateVar, width=14, justify="center")
        self.numberPlateEntry.grid(row=9, column=1, pady=10)

        self.operationButton = Button(self.operationFrame, text="Add Vehicle", command=self.checkData)
        self.operationButton.pack(fill="x")
    
    def checkData(self):
        print("vehicle adding process starts")
        if(not self.modelVar.get()):
            requirementsFilled=False
            instructionText = "Model field is necessary"
        elif(not self.manufaturerVar.get()):
            requirementsFilled=False
            instructionText = "Manufacturer field is necessary"
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

            self.vehicle = [self.modelVar.get(), self.manufaturerVar.get(), self.fuelUsedEntry.get(), self.engineCCVar.get(), self.horsePowerVar.get(), self.numCyilendersVar.get(), self.fuelCapacityVar.get(), self.seatingCapacityVar.get(), self.vehicleWeightVar.get()]
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
        self.fuelCapacityEntry.config(state="disable")
        self.seatingCapacityEntry.config(state="disable")
        self.vehicleWeightEntry.config(state="disable")
        self.operationButton.config(state="disable")
        self.numberPlateEntry.config(state="disable")

    def enable(self):
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

class finalPage:
    def __init__(self, pageWindow, parentUpdateStatus=None):
        self.loanPassed = False
        self.parentUpdateStatus = parentUpdateStatus
        self.mainFrame = Frame(pageWindow)
        self.mainFrame.grid(row=0, column=0, sticky="nsew")

        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)

        self.innerMainFrame = Frame(self.mainFrame, borderwidth=2, relief="raised")
        self.innerMainFrame.grid(row=0, column=0)

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

        self.interestPercentLabel = Label(self.finalDataFrame, text="% per month")
        self.interestPercentLabel.grid(row=1, column=2)

        self.loanPeriodLabel = Label(self.finalDataFrame, text="Loan Period : ")
        self.loanPeriodLabel.grid(row=2, column=0)

        self.loanTimeLabel = Label(self.finalDataFrame, text="In months")
        self.loanTimeLabel.grid(row=2, column=2)

        self.installmentAmtLabel = Label(self.finalDataFrame, text="Installment Amount : ")
        self.installmentAmtLabel.grid(row=3, column=0)

        self.rupeesLabel2 = Label(self.finalDataFrame, text="₹")
        self.rupeesLabel2.grid(row=3, column=2)

        self.saveButton = Button(self.finalDataFrame, text="Loan Pass", bg="light green", command=self.save)
        self.saveButton.grid(row=4, column=1, sticky="we", pady=20)

        self.amountApprovedVar = DoubleVar()
        self.amountApprovedEntry = Entry(self.finalDataFrame, textvariable=self.amountApprovedVar)
        self.amountApprovedEntry.grid(row=0, column=1)

        self.interestVar = DoubleVar()
        self.interestEntry = Entry(self.finalDataFrame, textvariable=self.interestVar)
        self.interestEntry.grid(row=1, column=1)

        self.loanPeriodVar = DoubleVar()
        self.loanPeriodEntry = Entry(self.finalDataFrame, textvariable=self.loanPeriodVar)
        self.loanPeriodEntry.grid(row=2, column=1)

        self.installmentAmtVar = DoubleVar()
        self.installmentAmtEntry = Entry(self.finalDataFrame, textvariable=self.installmentAmtVar)
        self.installmentAmtEntry.grid(row=3, column=1)

    def save(self):
        self.loanPassed = True
        self.updateStatus()
        
    def updateStatus(self):
        if(self.parentUpdateStatus):
            self.parentUpdateStatus()

if __name__=="__main__":
    root = Tk()
    root.geometry("599x499")
    root.title("add new file")
    object = AddFile(root)
    root.mainloop()
