#importing only necessary classes and things from library
import sys
sys.path.append(r"D:\projects\finoshok\finoshok\model")
sys.path.append(r"D:\projects\finoshok\finoshok\config")
from pathConfig import CUSTOMERPHOTOPATH
from Customer import Customer
from tkinter import Tk, Frame, Label, Entry, Button, Checkbutton, IntVar, END
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import shutil

#AddCustomer class needs a parameter either a tk window or frame
class AddCustomer:
    def __init__(self, addCustomerWindow, parentUpdateStatus=None):
        #parnetupdatestatus
        self.parentUpdateStatus = parentUpdateStatus

        #initial state of customerphoto  and self.photopath is set to None
        self.customerPhoto = None
        self.photoPath = None

        mainFrameColor="black"
        subFrameColor = "black"

        #heading label of the tab
        addCustomerLabel = Label(addCustomerWindow, text="Add Customer", font="COPPER 15", fg="yellow", bg="black")
        addCustomerLabel.pack(side="top", fill="x", ipady=20)

        #alreadyExistsLabel initially set to empty
        instructionLabel = Label(addCustomerWindow, text="", font="COPPER 13", fg="red", bg="black")
        instructionLabel.pack(side="top", fill="x",ipady=10)

        #created mainFrame which will hold everything of AddCustomer page
        mainFrame = Frame(addCustomerWindow, bg=mainFrameColor)
        mainFrame.pack(fill="both", expand=True)

        #congiguring row 0, 1 and column 0 to make the center in the frame
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)

        #creating subframe
        subFrame = Frame(mainFrame, bg=subFrameColor,width=200, height=200)
        subFrame.grid(row=0, column=0)

        labelFgColor = "yellow"
        labelBgColor = "black"

        #naming labels creation in the subframe
        customerNameLabel = Label(subFrame, text="Customer Name : ", fg=labelFgColor, bg=labelBgColor)
        customerNameLabel.grid(row=0, column=0)

        aadharLabel = Label(subFrame, text="Aadhar Number : ", fg=labelFgColor, bg=labelBgColor)
        aadharLabel.grid(row=1, column=0)

        mobileLabel = Label(subFrame, text="Mobile : ", fg=labelFgColor, bg=labelBgColor)
        mobileLabel.grid(row=2, column=0)

        fatherNameLabel = Label(subFrame, text="Father Name : ", fg=labelFgColor, bg=labelBgColor)
        fatherNameLabel.grid(row=3, column=0)

        homeAddressLabel = Label(subFrame, text="Home Address : ", fg=labelFgColor, bg=labelBgColor)
        homeAddressLabel.grid(row=4, column=0)

        WorkAddressLabel = Label(subFrame, text="Work Address : ", fg=labelFgColor, bg=labelBgColor)
        WorkAddressLabel.grid(row=5, column=0)

        photoLabel = Label(subFrame, text="Photo : ", fg=labelFgColor, bg=labelBgColor)
        photoLabel.grid(row=6, column=0)

        #creating entries corresponding to their names labels
        cNameEntry = Entry(subFrame, width=14)
        cNameEntry.grid(row=0, column=1)

        self.aadharEntry = Entry(subFrame, width=14)
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

        self.mobileEntry = Entry(subFrame, width=14)
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

        fNameEntry = Entry(subFrame, width=14)
        fNameEntry.grid(row=3, column=1)

        hAddressEntry = Entry(subFrame, width=14)
        hAddressEntry.grid(row=4, column=1)

        wAddressEntry = Entry(subFrame, width=14)
        wAddressEntry.grid(row=5, column=1)

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
        entryList = [cNameEntry, self.aadharEntry, self.mobileEntry, fNameEntry, hAddressEntry, wAddressEntry]

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
                self.customerPhotoLabel = Label(subFrame, image=self.customerPhoto)
                self.customerPhotoLabel.grid(row=6, column=1, pady=4)

                #changing the text of photoUploadButton from 'select' to 'Change' and also changing its position in the grid
                photoSelectButton.config(text="Change")
                photoSelectButton.grid(row=7, column=1)
            
        #this button will be used to upload photos
        photoSelectButton = Button(subFrame, text="Select", font="COPPER 8", width=13, command=photoSelect)
        photoSelectButton.grid(row=6, column=1)

        #checkAndSave function for checking if all fields are filled properly and the customers already exists or not. if not exists then save it to database along with the necessary details
        def checkAndSave():
            #checking if the fields are filled properly
            if((not cNameEntry.get())):
                requirementsFilled=False
                instructionText = "Please fill Customer's Name Field"
            elif(((not self.aadharEntry.get().isdigit()) or (len(self.aadharEntry.get())!=12))):
                requirementsFilled=False
                instructionText = "Please Fill Right Format of Aadhar"
            elif((not self.mobileEntry.get().isdigit()) or (len(self.mobileEntry.get())!=10)):
                requirementsFilled=False
                instructionText = "Please Fill Right Format of Mobile"
            elif((not fNameEntry.get())):
                requirementsFilled=False
                instructionText = "Please fill Father's Name Field"
            elif((not hAddressEntry.get())):
                requirementsFilled=False
                instructionText = "Please fill Home Address Field"
            elif((not wAddressEntry.get())):
                requirementsFilled=False
                instructionText = "Please fill work address Field"
            else:
                requirementsFilled=True
                 
            if(requirementsFilled):
                #check if customer already exists on the basis of its aadhar
                customerObject = Customer()
                data = customerObject.whereData(aadhar = self.aadharEntry.get())
                if(not data):
                    alreadyExists = False
                else:
                    alreadyExists = True
                
                if(not alreadyExists):
                    #code for saving the customer
                    #insertSuccessfully true if successfull insertion else false
                    insertSuccessfully= (customerObject.insertData(name=cNameEntry.get(), father=fNameEntry.get(), mobile=self.mobileEntry.get(), aadhar =self.aadharEntry.get(), home_address=hAddressEntry.get(), work_address=wAddressEntry.get()))

                    #if customer data inserted succesfully then only proceed
                    if(insertSuccessfully):
                        #adding customer's photo to assets if photoPath exists
                        if(self.photoPath):
                            #saving image as customerId.jpg
                            customerId = customerObject.whereData(aadhar=self.aadharEntry.get())[0][0]
                            shutil.copy(self.photoPath, f"{CUSTOMERPHOTOPATH}\\{customerId}.jpg")

                        #instructing user that all things are carried out successfully
                        instructionText=f"{cNameEntry.get()} added to database successfully"
                        showinfo("Customer Added", instructionText)
                        self.parentUpdateStatus(name=cNameEntry.get(), aadhar=self.aadharEntry.get())
                        instructionLabel.config(text="")

                        #removing old data from all entries
                        for entry in entryList:
                            entry.delete(0, END)
                        
                        #setting value of self.customerPhto to None
                        self.customerPhoto=None
                        #destroying the the label if it was created else do nonthing and return false value
                        self.customerPhotoLabel.destroy() if(self.photoPath) else False
                        
                        #changing the photbutton text
                        photoSelectButton.config(text="select")
                        photoSelectButton.grid(row=6,column=1)

                    else:
                        #instructing to user that customer can't be addede successully if insertSuccessfully is false
                        instructionText="Customer Cannot Be Added To Database"
                        instructionLabel.config(text=instructionText, fg="red")
        
                else:
                    #code for showing error in the tab that custoemr with this aadhar  already exists
                    instructionText = "Customer with same aadhar already exists !"
                    instructionLabel.config(text=instructionText, fg="red")
            else:
                instructionLabel.config(text=instructionText, fg="red")

        #this checkAndSaveButton
        checkAndSaveButton = Button(mainFrame, text="Check And Save", command=checkAndSave)
        checkAndSaveButton.grid(row=1, column=0)

    def updateStatus(self, **kwargs):
        if(self.parentUpdateStatus):
            self.parentUpdateStatus(name="yhj", aadhar="785337610582")    
if __name__=="__main__":
    root = Tk()
    root.geometry("599x499")
    root.title("add customer class testing window")
    AddCustomer(root)
    root.mainloop()
