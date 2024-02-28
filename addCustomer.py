from tkinter import Tk, Frame, Label, Entry, Radiobutton, StringVar, Button, Checkbutton, IntVar

class AddCustomer:
    def __init__(self, addCustomerWindow):
        mainFrameColor="black"
        subFrameColor = "black"
        mainFrame = Frame(addCustomerWindow, bg=mainFrameColor)
        mainFrame.pack(fill="both", expand=True)
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)

        subFrame = Frame(mainFrame, bg=subFrameColor,width=200, height=200)
        subFrame.grid(row=0, column=0)

        labelFgColor = "yellow"
        labelBgColor = "black"

        customerNameLabel = Label(subFrame, text="Customer Name : ", fg=labelFgColor, bg=labelBgColor)
        customerNameLabel.grid(row=0, column=0)

        mobileLabel = Label(subFrame, text="Mobile : ", fg=labelFgColor, bg=labelBgColor)
        mobileLabel.grid(row=1, column=0)

        fatherNameLabel = Label(subFrame, text="Father Name : ", fg=labelFgColor, bg=labelBgColor)
        fatherNameLabel.grid(row=2, column=0)

        homeAddressLabel = Label(subFrame, text="Home Address : ", fg=labelFgColor, bg=labelBgColor)
        homeAddressLabel.grid(row=3, column=0)

        WorkAddressLabel = Label(subFrame, text="Work Address : ", fg=labelFgColor, bg=labelBgColor)
        WorkAddressLabel.grid(row=4, column=0)

        photoLabel = Label(subFrame, text="Photo : ", fg=labelFgColor, bg=labelBgColor)
        photoLabel.grid(row=5, column=0)

        docVerifyLabel = Label(subFrame, text="Documents Verified : ", fg=labelFgColor, bg=labelBgColor)
        docVerifyLabel.grid(row=6, column=0)


        cNameEntry = Entry(subFrame, width=14)
        cNameEntry.grid(row=0, column=1)

        mobileEntry = Entry(subFrame, width=14)
        mobileEntry.grid(row=1, column=1)

        fNameEntry = Entry(subFrame, width=14)
        fNameEntry.grid(row=2, column=1)

        hAddressEntry = Entry(subFrame, width=14)
        hAddressEntry.grid(row=3, column=1)

        wAddressEntry = Entry(subFrame, width=14)
        wAddressEntry.grid(row=4, column=1)

        photoUploadButton = Button(subFrame, text="Upload", font="COPPER 8", width=13)
        photoUploadButton.grid(row=5, column=1)

        verifyVar = IntVar()

        yesCheck = Checkbutton(subFrame, text="Yes", variable=verifyVar, fg="black", bg="white")
        yesCheck.grid(row=6, column=1)

        checkAndSaveButton = Button(mainFrame, text="Check And Save")
        checkAndSaveButton.grid(row=1, column=0)

if __name__=="__main__":
    root = Tk()
    root.geometry("599x499")
    root.title("add customer class testing window")
    AddCustomer(root)
    root.mainloop()
