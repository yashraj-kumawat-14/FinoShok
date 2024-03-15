#importing only necessary classes and things from library
from tkinter import Tk, Frame, Label, Entry, Button, Checkbutton, IntVar

#AddCustomer class needs a parameter either a tk window or frame
class AddCustomer:
    def __init__(self, addCustomerWindow):
        mainFrameColor="black"
        subFrameColor = "black"

        #heading label of the tab
        addCustomerLabel = Label(addCustomerWindow, text="Add Customer", font="COPPER 15", fg="yellow", bg="black")
        addCustomerLabel.pack(side="top", fill="x", ipady=20)

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

        aadharEntry = Entry(subFrame, width=14)
        aadharEntry.grid(row=1, column=1)

        mobileEntry = Entry(subFrame, width=14)
        mobileEntry.grid(row=2, column=1)

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

            #traversing through all entries
            for entry in entryList:
                #checking if any one entry has no. of character more than 13
                if(len(entry.get())>13):
                    #if more than 13 then all entries width will be configured or set to their length +1
                    for otherEntry in entryList:
                        otherEntry.config(width=len(entry.get())+1)
                    #now condition is set to false
                    condition = False

            #if condition is true till now that means none of the entry in entryList has length of characters more than 13 so we set the width of all entries to 14
            
            if(condition):
                #traversing through all entries
                for otherEntry in entryList:
                        #configuring widht of entries
                        otherEntry.config(width=14)

        #creating entryList variable containing all entry widgets whom we wnat to enable dynamic width
        entryList = [cNameEntry, aadharEntry, mobileEntry, fNameEntry, hAddressEntry, wAddressEntry]

        #traversing through all entry widgets present in entryList
        for entry in entryList:
            #binding each and everyEntry to Key event and function func is set to dynamicWidth
            #lambda is used to make anonymous function syntax : lambda arguments : expression
            entry.bind("<Key>", func= lambda event, entryList=entryList: dynamicWidth(event, entryList))

        def photoUpload():
            pass
        #this button will be used to upload photos
        photoUploadButton = Button(subFrame, text="Upload", font="COPPER 8", width=13, command=photoUpload)
        photoUploadButton.grid(row=6, column=1)

        #this checkAndSaveButton
        checkAndSaveButton = Button(mainFrame, text="Check And Save")
        checkAndSaveButton.grid(row=1, column=0)

if __name__=="__main__":
    root = Tk()
    root.geometry("599x499")
    root.title("add customer class testing window")
    AddCustomer(root)
    root.mainloop()
