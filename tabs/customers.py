#Customers module to show list of customers present in the database using customer model
from tkinter import Tk, Frame, Listbox, Scrollbar, Label, Entry, Button, END, StringVar
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
        searchFrame.columnconfigure(2, weight=1)

        searchLabel = Label(searchFrame, text="Search here : ")
        searchLabel.grid(row=0, column=0)

        self.searchEntry = Entry(searchFrame)
        self.searchEntry.grid(row=0, column=1)

        refreshButton = Button(searchFrame, text=u"\u21BB", bg="orange", font="COPPER 12", height=1, width=3, command=self.refresh)
        refreshButton.grid(row=0, column=2, sticky="e")

        # filterButton = Button(searchFrame, text="Filter")
        # filterButton.grid(row=0, column=3, sticky="e")

        #work of searchFrame ends here

        #work of customerListFrame starts here
        
        #creating a listbox
        self.customerListBox = Listbox(customerListFrame, selectmode="browse")
        self.customerListBox.pack(fill="both", expand=True)

        # creating scrollbar for y direction
        scrollY = Scrollbar(self.customerListBox, command=self.customerListBox.yview)
        scrollY.pack(side="right", fill="y")
        self.customerListBox.config(yscrollcommand=scrollY.set)

        #creating scrollbar for x dirextion
        scrollX = Scrollbar(self.customerListBox, command=self.customerListBox.xview, orient="horizontal")
        scrollX.pack(side="bottom", fill="x")
        self.customerListBox.config(xscrollcommand=scrollX.set)

        #getting data from database
        data = Customer().readAllData()

        #creating an empty list initailly which will store dictionary containing individual customer data
        self.dataList = []

        #creating temporary datalist
        self.tempDataList = []

        #inserting data initially into listbox
        for customer in data:
            self.dataList.append({"name":customer[1], "mobile": customer[3], "aadhar":customer[6], "father":customer[2], "home_address":customer[4], "work_address":customer[5]})

        #binding enty and listbox to their respective fucntions
        self.searchEntry.bind("<KeyRelease>", self.search)        #Keyrelease because event actually fires  before entry wicget insert texts.
        self.customerListBox.bind("<<ListboxSelect>>", self.dynamicDetails)

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
        customerNameLabel = Label(detailsInnerFrame, text="Name : ")
        customerNameLabel.grid(row=0, column=0)

        aadharLabel = Label(detailsInnerFrame, text="Aadhar : ")
        aadharLabel.grid(row=1, column=0)

        mobileLabel = Label(detailsInnerFrame, text="Mobile : ")
        mobileLabel.grid(row=2, column=0)

        #creating labels dynamic
        self.customerEntryVar = StringVar()
        customerEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.customerEntryVar)
        customerEntry.grid(row=0, column=1)

        self.aadharEntryVar = StringVar()
        aadharEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.aadharEntryVar)
        aadharEntry.grid(row=1, column=1)

        self.mobileEntryVar = StringVar()
        mobileEntry = Entry(detailsInnerFrame, state="readonly", textvariable=self.mobileEntryVar)
        mobileEntry.grid(row=2, column=1)
        
        #view customer button
        self.viewCustomerButton = Button(customerDetailsFrame, text="View Customer", bg="pink")
        self.viewCustomerButton.grid(row=1, column=0, columnspan=2, sticky="nsew")

        #initially invoking search funtion
        self.search(None)
        self.customerListBox.selection_set(0)
        self.dynamicDetails(None)
    
    #it will display data in listbox according to the search query
    def search(self, event):
        if(self.searchEntry.get()):
            #search according to aadhar, mobile, name
            searchText = self.searchEntry.get()
            self.tempDataList = []

            for customer in self.dataList:
                if(searchText in str(customer["aadhar"]) or searchText in customer["name"] or searchText in str(customer["mobile"])):
                    self.tempDataList.append(customer)

            self.customerListBox.delete(0, END)
            for customer in self.tempDataList:
                self.customerListBox.insert(END, f"Name {customer["name"]} | Mobile :{customer["mobile"]} | Aadhar : {customer["aadhar"]}")
        else:
            #clearing all the previous data in listbox and tempDataList and reinserting all the data
            self.customerListBox.delete(0, END)

            for customer in self.dataList:
                self.customerListBox.insert(END, f"Name {customer["name"]} | Mobile :{customer["mobile"]} | Aadhar : {customer["aadhar"]}")
                self.tempDataList.append({"name":customer["name"], "mobile": customer["mobile"], "aadhar":customer["aadhar"]})
            
    #this function dynamically changes details in detailframe according to the currentselection in customerlistbox
    def dynamicDetails(self, event):
        if(self.customerListBox.curselection()):
            #dynamic updating details and photo

            #setting new data
            self.customerEntryVar.set(f"{self.tempDataList[self.customerListBox.curselection()[0]]["name"]}")
            self.mobileEntryVar.set(f"{self.tempDataList[self.customerListBox.curselection()[0]]["mobile"]}")
            self.aadharEntryVar.set(f"{self.tempDataList[self.customerListBox.curselection()[0]]["aadhar"]}")

            #creating a PIL image object
            PhotoPath = f"D:\\projects\\finoshok\\finoshok\\assets\\customerPhotos\\{self.tempDataList[self.customerListBox.curselection()[0]]["aadhar"]}.jpg"
            
            #if error found during imaging loading then use default image
            try:
                img=Image.open(PhotoPath)
            
                #resizing the image
                img=img.resize((82,80))

                #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
                self.customerPhoto = ImageTk.PhotoImage(img)
                self.customerPhotoLabel.config(image=self.customerPhoto)
            except:
                PhotoPath = f"D:\\projects\\finoshok\\finoshok\\assets\\defaultImages\\user.jpg"
                img=Image.open(PhotoPath)
            
                #resizing the image
                img=img.resize((82,80))

                #using ImageTk module's PhotoImage class so that to convert pil img object into a form that tkinter can understand
                self.customerPhoto = ImageTk.PhotoImage(img)
                self.customerPhotoLabel.config(image=self.customerPhoto)
        
    def refresh(self):
        #getting data from database
        data = Customer().readAllData()

        #creating an empty list initailly which will store dictionary containing individual customer data
        self.dataList = []

        #creating temporary datalist
        self.tempDataList = []

        #inserting data initially into listbox
        for customer in data:
            self.dataList.append({"name":customer[1], "mobile": customer[3], "aadhar":customer[6]})
        print(self.dataList)
        
        self.search(None)
        self.customerListBox.selection_set(0)
        self.dynamicDetails(None)


if __name__ == "__main__":
    root = Tk()
    root.geometry("500x500")
    root.title("Customers")
    a = Customers(root)
    root.mainloop()