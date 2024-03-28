from tkinter import Tk, Frame, Label, Listbox, Scrollbar, END, Checkbutton, IntVar, StringVar, Entry, Button
from tkcalendar import DateEntry
from PIL import Image, ImageTk

#AddFile class needs a parameter either a tk window or frame
class AddFile:
    def __init__(self, addFileWindow):
        mainFrameColor="black"
        #create mainframe containing everything
        mainFrame = Frame(addFileWindow, bg=mainFrameColor)
        mainFrame.pack(fill="both", expand=True)

        #columnconfigure() resizes the grid vertically, while rowconfigure() resizes the grid horizontally. The width of a grid column is equal to the width of its widest cell.
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=1)
        
        subFrame1Color = "grey"
        subFrame2Color = "black"
        subFrame3Color = "grey"
        #created subframes for showing different graphs and data
        
        #The sticky parameter in the .grid() method of Tkinter is used to define how a widget should expand to fill the space allocated to it within a grid cell.
        subFrame1 = Frame(mainFrame, bg=subFrame1Color, relief="groove", border=3)
        subFrame1.grid(row=0, column=0, sticky="ewns")

        subFrame2 = Frame(mainFrame, relief="groove", border=3)
        subFrame2.grid(row=0, column=1, sticky="ewns", rowspan=2)

        subFrame3 = Frame(mainFrame, bg=subFrame3Color, relief="groove", border=3)
        subFrame3.grid(row=1, column=0, sticky="ewns")  

        #now creating 3 sections : 
        #section 1 for selecting any one loan requests also adding heading/label

        selectRequestLabel = Label(subFrame1, text="Select Loan Request ")
        selectRequestLabel.pack(fill="x")
        section1 = Frame(subFrame1)
        section1.pack(fill="both", expand=True) 

        #section 2 for loan confirmation along with some formalities
        section2 = Frame(subFrame2)
        section2.grid(row=0, column=0, sticky="n", pady=50)

        #section 3 for showing selected loan request details along with some customer details

        section3 = Frame(subFrame3)
        section3.pack(fill="both", expand=True) 

        #now filling in these sections
        #section 1 work start-------

        #creating a section1 as more responsive  using rowconfigure and columnconfigure

        section1.rowconfigure(0, weight=1)
        section1.columnconfigure(0, weight=1)

        customerRequestBox = Listbox(section1)
        customerRequestBox.grid(row=0, column=0, sticky="nsew")


        # creating scrollbar for y direction
        scrollY = Scrollbar(customerRequestBox, command=customerRequestBox.yview)
        scrollY.pack(side="right", fill="y")
        customerRequestBox.config(yscrollcommand=scrollY.set)

        #creating scrollbar for x dirextion
        scrollX = Scrollbar(customerRequestBox, command=customerRequestBox.xview, orient="horizontal")
        scrollX.pack(side="bottom", fill="x")
        customerRequestBox.config(xscrollcommand=scrollX.set)


        # scroll = Scrollbar(section1)
        # scroll.pack()
        for i in range(100):
            customerRequestBox.insert(END, f"customer Id : {i} | name {"Yash"} | amount : 34000 | date : 2/2/2 | mobile : 9999999999 | aadhar : 123456789012")

        #section 1 work ends----
        
        #section 2 work starts ----
            
        #creating a section1 as more responsive  using rowconfigure and columnconfigure

        subFrame2.rowconfigure(0, weight=1)
        subFrame2.columnconfigure(0, weight=1)

        #now creating labels

        approveLoanLabel = Label(section2, text="Approve Loan : ")
        approveLoanLabel.grid(row=0, column=0, pady=20)

        dateApprovedLabel = Label(section2, text="Date Approved : ")
        dateApprovedLabel.grid(row=1, column=0, pady=20)

        amountApprovedLabel = Label(section2, text="Amount Approved : ")
        amountApprovedLabel.grid(row=2, column=0, pady=20)

        currencyLabel1= Label(section2, text=" ₹")
        currencyLabel1.grid(row=2, column=2)

        interestLabel = Label(section2, text="Interest : ")
        interestLabel.grid(row=3, column=0, pady=20)

        percentLabel= Label(section2, text=" %")
        percentLabel.grid(row=3, column=2)

        loanPeriodLabel = Label(section2, text="Loan Period : ")
        loanPeriodLabel.grid(row=4, column=0, pady=20)

        timeUnitLabel= Label(section2, text=" Months")
        timeUnitLabel.grid(row=4, column=2)

        emiAmountLabel = Label(section2, text="EMI amount : ")
        emiAmountLabel.grid(row=5, column=0, pady=20)

        currencyLabel2= Label(section2, text=" ₹")
        currencyLabel2.grid(row=5, column=2)

        totalEmiLabel = Label(section2, text="Total EMI's : ")
        totalEmiLabel.grid(row=6, column=0, pady=20)

        #now creating entries, dateentry, combobox

        #this function enables disabels the entries state on the basis of current value of loanCheckVar
        def enableEntries():
            if(loanCheckVar.get()):
                for entry in entryList:
                    entry.config(state="normal")
                    dateApprovedEntry.config(state="readonly")
            else:
                for entry in entryList:
                    entry.config(state="disable")
                    dateApprovedEntry.config(state="disable")


        #here a check button is created to enable access to remaining entries and to make sure that loan is approved

        loanCheckVar = IntVar()
        approveLoanCheck = Checkbutton(section2, variable=loanCheckVar, command=enableEntries)
        approveLoanCheck.grid(row=0, column=1, stick="w")

        #created dateApprovedEntry to select the date on which loan was aprroved
        dateApprovedEntry = DateEntry(section2, width=17, date_pattern="dd/MM/yyyy", justify="center", state="disable", selectmode="day")
        dateApprovedEntry.grid(row=1, column=1)

        #this entry holds the amount of loan which was approved
        amountApprovedEntry = Entry(section2, state="disable")
        amountApprovedEntry.grid(row=2, column=1)

        #this entry holds the value of interes taken for particular client
        interestEntry = Entry(section2, state="disable")
        interestEntry.grid(row=3, column=1)

        #this entry holds the time period in months or loan period
        loanPeriodEntry = Entry(section2, state="disable")
        loanPeriodEntry.grid(row=4, column=1)
        
        #this entry holds the amount of one emi
        emiAmountEntry = Entry(section2, state="disable")
        emiAmountEntry.grid(row=5, column=1)

        #this entry holds the total number of emi's
        totalEmiEntry = Entry(section2, state="disable")
        totalEmiEntry.grid(row=6, column=1)

        #entryList which holds all entries
        entryList = [loanPeriodEntry, emiAmountEntry, totalEmiEntry, interestEntry, amountApprovedEntry]

        #creating save button
        saveDataButton = Button(section2, text="Save", bg="orange")
        saveDataButton.grid(row=7, columnspan=3, sticky="nsew")

        #section 2 work endss ----
            
        #section3 work starts ----
        
        #making responsive section3
        section3.rowconfigure(0, weight=1)
        section3.columnconfigure(0, weight=1)
        section3.columnconfigure(1, weight=2)

        #creating two frames sec3PhotoFrame and sec3Details inside section3
        sec3PhotoFrame = Frame(section3, relief="groove", border=3)
        sec3PhotoFrame.grid(row=0, column=0, sticky="nsew")

        sec3Details = Frame(section3, relief="groove", border=3)
        sec3Details.grid(row=0, column=1, sticky="nsew")

        #creating responsive sec3PhotoFrame
        sec3PhotoFrame.rowconfigure(0, weight=1)
        sec3PhotoFrame.columnconfigure(0, weight=1)

        #creating a PIL image object
        initialPhotoPath = r"D:\projects\finoshok\finoshok\assets\defaultImages\user.jpg"
        img=Image.open(initialPhotoPath)
        
        #resizing the image
        img=img.resize((82,80))

        #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
        self.customerPhoto = ImageTk.PhotoImage(img)

        #now integrating the image into label widget and positioning it via grid 
        self.customerPhotoLabel = Label(sec3PhotoFrame, image=self.customerPhoto)
        self.customerPhotoLabel.grid(row=0, column=0)

        #creating responsive sec3Details frame
        sec3Details.rowconfigure(0, weight=1)
        sec3Details.columnconfigure(0, weight=1)
        
        #creating a inner subFramee detailsInnerFrame inside sec3details
        detailsInnerFrame = Frame(sec3Details)
        detailsInnerFrame.grid(row=0, column=0)

        #creating labels static
        customerNameLabel = Label(detailsInnerFrame, text="Customer Name : ")
        customerNameLabel.grid(row=0, column=0)

        civilScoreLabel = Label(detailsInnerFrame, text="Civil Score : ")
        civilScoreLabel.grid(row=1, column=0)

        mobileLabel = Label(detailsInnerFrame, text="Mobile : ")
        mobileLabel.grid(row=2, column=0)

        workAddressLabel = Label(detailsInnerFrame, text="Work Address : ")
        workAddressLabel.grid(row=3, column=0)

        #creating labels dynamic
        customerEntryLabel = Label(detailsInnerFrame, text="Yashraj")
        customerEntryLabel.grid(row=0, column=1)

        civilScoreEntryLabel = Label(detailsInnerFrame, text="9 ")
        civilScoreEntryLabel.grid(row=1, column=1)

        mobileEntryLabel = Label(detailsInnerFrame, text="7357446466")
        mobileEntryLabel.grid(row=2, column=1)
        
        wAddresssEntryLabel = Label(detailsInnerFrame, text="kankroli")
        wAddresssEntryLabel.grid(row=3, column=1)
        #section3 workd ends----

if __name__=="__main__":
    root = Tk()
    root.geometry("599x499")
    root.title("add new file")
    object = AddFile(root)
    root.mainloop()
