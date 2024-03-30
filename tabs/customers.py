#Customers module to show list of customers present in the database using customer model
from tkinter import Tk, Frame, Listbox, Scrollbar, Label, Entry, Button, END
from PIL import Image, ImageTk
#importign sys.path so that we can add model folder to search path
from sys import path
path.append(r"D:\projects\finoshok\finoshok\model")
#now we can import Customer class successfully from customer model
from Customer import Customer

#this is customer class which creates a object for searching customers and getting their information
class Customers:
    def __init__(self, customerWindow) :
        #customerwindow can be a frame or a tk object

        #mainFrame contains all the things
        mainFrame = Frame(customerWindow)
        mainFrame.pack(fill="both", expand=True)

        #configuring mainframe as grid to make responsive design
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=1)

        #two subframes inside mainframe
        subFrame1 = Frame(mainFrame)
        subFrame1.grid(row=0, column=0, sticky="nsew")

        subFrame2 = Frame(mainFrame)
        subFrame2.grid(row=0, column=1, sticky="nsew")
        #creating two frames one is searchFrame and second is customerListBox inside mainFrame

        #searchFrame will consist of search label , search entry amd search filter for searching the customers 
        searchFrame = Frame(subFrame1)
        searchFrame.pack(side="top", fill="x")

        #customerListFrame will display customers details from surface according the search query and filters
        customerListFrame = Frame(subFrame1)
        customerListFrame.pack(fill="both", expand=True)

        #work of searchFrame starts here
        searchFrame.columnconfigure(3, weight=1)

        searchLabel = Label(searchFrame, text="Search here : ")
        searchLabel.grid(row=0, column=0)

        searchEntry = Entry(searchFrame)
        searchEntry.grid(row=0, column=1)

        searchButton = Button(searchFrame, text="Search", bg="orange")
        searchButton.grid(row=0, column=2)

        filterButton = Button(searchFrame, text="Filter")
        filterButton.grid(row=0, column=3, sticky="e")

        #work of searchFrame ends here

        #work of customerListFrame starts here
        
        #creating a listbox
        customerListBox = Listbox(customerListFrame)
        customerListBox.pack(fill="both", expand=True)

        # creating scrollbar for y direction
        scrollY = Scrollbar(customerListBox, command=customerListBox.yview)
        scrollY.pack(side="right", fill="y")
        customerListBox.config(yscrollcommand=scrollY.set)

        #creating scrollbar for x dirextion
        scrollX = Scrollbar(customerListBox, command=customerListBox.xview, orient="horizontal")
        scrollX.pack(side="bottom", fill="x")
        customerListBox.config(xscrollcommand=scrollX.set)

        #getting data from database
        data = Customer().readAllData()

        #inserting data initially into listbox
        for customer in data:
            customerListBox.insert(END, f"customer Id : {customer[0]} | Name {customer[1]} | Mobile :{customer[3]} | Aadhar : {customer[6]}")

        #work of customerListFrame ends here
            
        #work in subframe2 starts here
        subFrame2.rowconfigure(0, weight=1)
        subFrame2.columnconfigure(0, weight=1)

        customerDetailsFrame = Frame(subFrame2)
        customerDetailsFrame.grid(row=0, column=0)
            
        #creating two frames sec3PhotoFrame and sec3Details inside subframe2
        PhotoFrame = Frame(customerDetailsFrame, relief="groove", border=3)
        PhotoFrame.grid(row=0, column=0, sticky="nsew")

        Details = Frame(customerDetailsFrame, relief="groove", border=3)
        Details.grid(row=0, column=1, sticky="nsew")

        #creating responsive sec3PhotoFrame
        PhotoFrame.rowconfigure(0, weight=1)
        PhotoFrame.columnconfigure(0, weight=1)

        #creating a PIL image object
        initialPhotoPath = r"D:\projects\finoshok\finoshok\assets\defaultImages\user.jpg"
        img=Image.open(initialPhotoPath)
        
        #resizing the image
        img=img.resize((82,80))

        #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
        self.customerPhoto = ImageTk.PhotoImage(img)

        #now integrating the image into label widget and positioning it via grid 
        self.customerPhotoLabel = Label(PhotoFrame, image=self.customerPhoto)
        self.customerPhotoLabel.grid(row=0, column=0)

        #creating responsive sec3Details frame
        Details.rowconfigure(0, weight=1)
        Details.columnconfigure(0, weight=1)
        
        #creating a inner subFramee detailsInnerFrame inside sec3details
        detailsInnerFrame = Frame(Details)
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
        
if __name__ == "__main__":
    root = Tk()
    root.geometry("500x500")
    root.title("Customers")
    a = Customers(root)
    root.mainloop()