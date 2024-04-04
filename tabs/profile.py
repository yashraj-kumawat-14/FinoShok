#profile module shows the whole details and informations related to particular customer and its prvious, ongoing files

#importing necessary modules nad theier components
from tkinter import *
from PIL import Image, ImageTk
from sys import path
#adding this path search so that interpreter can search modules and import it from this directory 
path.append(r"D:\projects\finoshok\finoshok\model")
from Customer import Customer


#Profile class takes one tk Window or a Frame and aadharNumber of the particular customer to show it s profile

class Profile:
    def __init__(self, profileWindow, aadharNumber, updateStatus = None):
        #now assinging the value of aadharNumber to self.aadharNumber so that we can use it throughout the class without making it global
        self.aadharNumber = aadharNumber

        #initially assing the function updateStatus if given to self.updateStatus so to use it across the class
        self.updateStatus = updateStatus
        
        #mainFrame holds everything , content of the profile
        mainFrame = Frame(profileWindow, bg="black")
        mainFrame.pack(fill="both", expand=True)

        #configuring rows and columns so to make responsive grid system
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)
        mainFrame.rowconfigure(2, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        
        #creting two subframes in mainframe
        subFrame1 = Frame(mainFrame, bg="brown")
        subFrame1.grid(row=0, column=0, sticky="nsew")

        subFrame2 = Frame(mainFrame, bg='orange')
        subFrame2.grid(row=1, column=0, sticky="nsew", rowspan=2)

        #configuring grids in subframe1
        subFrame1.rowconfigure(0, weight=1)

        for i in range(6):
            subFrame1.columnconfigure(i, weight=1)

        #creating navigation and details frame in subframe1
        navsubFrame1 = Frame(subFrame1, bg="yellow")
        navsubFrame1.grid(row=0, column=0, sticky="nsew")

        self.detailsFrame = Frame(subFrame1, bg='green')
        self.detailsFrame.grid(row=0, column=1, sticky="nsew", columnspan=5)

        #configuring grids in subframe2
        subFrame2.rowconfigure(0, weight=1)

        for i in range(6):
            subFrame2.columnconfigure(i, weight=1)

        #creating navigation and excel frame in subframe2
        navsubFrame2 = Frame(subFrame2, bg="blue")
        navsubFrame2.grid(row=0, column=0, sticky="nsew")

        excelFrame = Frame(subFrame2, bg='violet')
        excelFrame.grid(row=0, column=1, sticky="nsew", columnspan=5)

        #creating radio buttons in both nav1 and nav2
        self.navsubFrameVar1 = StringVar()
        self.navsubFrameVar1.set("1")
        
        navsubFrame1.rowconfigure(0, weight=1)
        navsubFrame1.columnconfigure(0, weight=1)

        innerNavSubFrame1 = Frame(navsubFrame1)
        innerNavSubFrame1.grid(row=0, column=0)

        customerRadio = Radiobutton(innerNavSubFrame1, text="Customer Profile", variable=self.navsubFrameVar1, value="1", command=lambda:self.detailsFrameController())
        customerRadio.grid(row=0, column=0, sticky="w")
        
        guarranterRadio = Radiobutton(innerNavSubFrame1, text="Guarranters", variable=self.navsubFrameVar1, value="2", command=self.detailsFrameController)
        guarranterRadio.grid(row=1, column=0, sticky="w")

        self.navsubFrameVar2 = StringVar()
        self.navsubFrameVar2.set("1")
        
        for i in range(9):
            navsubFrame2.rowconfigure(i, weight=1)
        
        navsubFrame2.columnconfigure(0, weight=1)

        innerNavSubFrame2 = Frame(navsubFrame2)
        innerNavSubFrame2.grid(row=0, column=0, sticky="nwes")

        innerNavSubFrame2.rowconfigure(0, weight=1)
        innerNavSubFrame2.rowconfigure(1, weight=1)
        innerNavSubFrame2.columnconfigure(0, weight=1)

        vehiclesRadio = Radiobutton(innerNavSubFrame2, text="Vehicles", variable=self.navsubFrameVar2, value="1")
        vehiclesRadio.grid(row=0, column=0, sticky="sw")
        
        filesRadio = Radiobutton(innerNavSubFrame2, text="Files", variable=self.navsubFrameVar2, value="2")
        filesRadio.grid(row=1, column=0, sticky="nw")

        #creating a listbox in nav2 frame
        dynamicListBox = Listbox(navsubFrame2)
        dynamicListBox.grid(row=1, column=0, sticky="nswe", rowspan=8)

        #getting data relavent to customer with aadharnumber stored in self.aadharNuber
        customerObject = Customer()
        self.data = customerObject.whereData(aadhar=str(self.aadharNumber))

        #now invoking detailsConstroller method initiallly
        self.detailsFrameController()

    #this method is used to change content present in detailsFrame acording to the value of radio buttonsi nav1
    def detailsFrameController(self):

        #first things is to delete all the widgets present in self.detailsFrame
        children  = self.detailsFrame.winfo_children()

        for child in children:
            child.destroy()

        #creating new widgets according to value of self.navsubFrameVar1

        #if user selected a radio button whose value is 1 then; 
        if(self.navsubFrameVar1.get()=="1"):
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
                PhotoPath = f"D:\\projects\\finoshok\\finoshok\\assets\\customerPhotos\\{self.data[0][0]}.jpg"
                img=Image.open(PhotoPath)
            
                #resizing the image
                img=img.resize((82,120))

                #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
                self.customerPhoto = ImageTk.PhotoImage(img)
                self.customerPhotoLabel.config(image=self.customerPhoto)
            except:
                PhotoPath = f"D:\\projects\\finoshok\\finoshok\\assets\\defaultImages\\user.jpg"
                img=Image.open(PhotoPath)
            
                #resizing the image
                img=img.resize((82,120))

                #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
                self.customerPhoto = ImageTk.PhotoImage(img)
                self.customerPhotoLabel.config(image=self.customerPhoto)

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
            aadharEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.aadharEntryVar)
            aadharEntry.grid(row=1, column=1)

            self.mobileEntryVar = StringVar()
            self.mobileEntryVar.set(customerData["mobile"])
            mobileEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.mobileEntryVar)
            mobileEntry.grid(row=2, column=1)

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
            entryList = [workAddressEntry, fatherEntry, customerEntry, homeAddressEntry, mobileEntry, aadharEntry]
            
            #This button allows user to interact with entries and edit them
            editButton = Button(self.customerDetailsFrame, text="Edit", state=state)
            editButton.grid(row=1, column=0, columnspan=2, sticky="nsew")

            #configuring commmand for editButton as self.edit()
            editButton.config(command=lambda entryList=entryList, editButton=editButton: self.edit(entryList, editButton))

    #thsi edite function changes state of entries to normal and allows user to edit them and save them
    def edit(self, entryList, editButton):
        #changing state to normal
        for entry in entryList:
            entry.config(state="normal")
        editButton.destroy()

        #cancelButton to exit from edit mode and go to read mode
        cancelButton = Button(self.customerDetailsFrame, text="Cancel", command=self.detailsFrameController)
        cancelButton.grid(row=1, column=0, sticky="ew")

        saveButton = Button(self.customerDetailsFrame, text="Save", command=self.save)
        saveButton.grid(row=1, column=1, sticky="we")
    
    #this functions saves the changes made by user in edit mode and save it to the database
    def save(self):
        #creating a customerobject
        customerObject = Customer()

        #updating customer data by takin customer id as reference 
        customerObject.updateData(id=self.data[0][0], name=self.customerEntryVar.get(), father=self.fatherEntryVar.get(), mobile=self.mobileEntryVar.get(), home_address=self.homeAddressEntryVar.get(), work_address=self.workAddressEntryVar.get(), aadhar=self.aadharEntryVar.get())

        #updating self.data 
        self.data = customerObject.whereData(id=self.data[0][0])

        #now calling detailsFrameController to show new customerDetails in readmode
        self.detailsFrameController()
        
        #if self.updateStatus is not empty then updating the tabName
        if(self.updateStatus):
            self.updateStatus(tabName=self.customerEntryVar.get())
    

#following code won't run until it is run from this file only
if __name__ =="__main__":
    root = Tk()
    root.geometry("500x500")
    root.title("Profile")
    profileObject = Profile(root, 785337610582)
    root.mainloop()