#profile module shows the whole details and informations related to particular customer and its prvious, ongoing files

#importing necessary modules nad theier components
from tkinter import *
from PIL import Image, ImageTk
from sys import path
#adding this path search so that interpreter can search modules and import it from this directory 
path.append(r"D:\projects\finoshok\finoshok\model")
from Customer import Customer
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as message
import shutil
from pathConfig import CUSTOMERPHOTOPATH


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
        # mainFrame.rowconfigure(2, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=1)
        mainFrame.columnconfigure(2, weight=1)
        
        #creting two subframes in mainframe
        subFrame1 = Frame(mainFrame, borderwidth=3, relief="groove")
        subFrame1.grid(row=0, column=0, sticky="nsew")
        # subFrame1.grid_propagate(False)

        subFrame2 = Frame(mainFrame, borderwidth=3, relief="groove")
        subFrame2.grid(row=1, column=0, sticky="nsew", rowspan=2)

        subFrame3 = Frame(mainFrame, borderwidth=3, relief="groove")
        subFrame3.grid(row=0, column=1, sticky="nsew", rowspan=2, columnspan=2)

        #subframe1 work starts here
        profileDetailsLabel = Label(subFrame1, text="Profile Details", font="COPPER 20", bg="orange")
        profileDetailsLabel.pack(fill="x")

        self.detailsFrame = Frame(subFrame1, bg="black")
        self.detailsFrame.pack(fill="both", expand=True)

        #getting data relavent to customer with aadharnumber stored in self.aadharNuber
        customerObject = Customer()
        self.data = customerObject.whereData(aadhar=str(self.aadharNumber))

        #subframe1 work ends here

        #now invoking detailsConstroller method initiallly
        self.detailsFrameController()

        #subframe2 work starts here
        navsubFrame2 = Frame(subFrame2, borderwidth=2, relief="raised")
        navsubFrame2.pack(fill="x")

        #configuring grid area
        navsubFrame2.columnconfigure(0, weight=1)
        navsubFrame2.columnconfigure(1, weight=1)

        #navigation radio buttons
        self.navsubFrameVar2 = IntVar()
        self.navsubFrameVar2.set(1)
        
        #creating radiobuttons
        filesRadioButton = Radiobutton(navsubFrame2, text="Files", value=1, variable=self.navsubFrameVar2)
        filesRadioButton.grid(row=0, column=0)

        vehiclesRadioButton = Radiobutton(navsubFrame2, text="Vehicles",value=2, variable=self.navsubFrameVar2)
        vehiclesRadioButton.grid(row=0, column=1)

        #creating listbox
        self.dataListBox = Listbox(subFrame2)
        self.dataListBox.pack(fill="both", expand=True)
    #
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
            self.photoPath = f"D:\\projects\\finoshok\\finoshok\\assets\\customerPhotos\\{self.data[0][0]}.jpg"
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
        editButton.config(command=lambda entryList=entryList, editButton=editButton: self.edit(entryList, editButton))

    #thsi edite function changes state of entries to normal and allows user to edit them and save them
    def edit(self, entryList, editButton):
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
                    shutil.copy(self.photoPath, f"{CUSTOMERPHOTOPATH}\\{self.data[0][0]}.jpg")

                #updating self.data 
                self.data = customerObject.whereData(id=self.data[0][0])

                #now calling detailsFrameController to show new customerDetails in readmode
                self.detailsFrameController()
                
                #if self.updateStatus is not empty then updating the tabName
                if(self.updateStatus):
                    self.updateStatus(tabName=self.customerEntryVar.get())
        else:
            print(instructionText)
    
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
    root.geometry("500x500")
    root.title("Profile")
    profileObject = Profile(root, 785337610582)
    root.mainloop()