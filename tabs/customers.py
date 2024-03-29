#Customers module to show list of customers present in the database using customer model
from tkinter import Tk, Frame, Listbox, Scrollbar, Label, Entry, Button, END

#this is customer class which creates a object for searching customers and getting their information
class Customer:
    def __init__(self, customerWindow) :
        #customerwindow can be a frame or a tk object
        #mainFrame contains all the things
        mainFrame = Frame(customerWindow)
        mainFrame.pack(fill="both", expand=True)

        #creating two frames one is searchFrame and second is customerListBox inside mainFrame

        #searchFrame will consist of search label , search entry amd search filter for searching the customers 
        searchFrame = Frame(mainFrame)
        searchFrame.pack(side="top", fill="x")

        #customerListFrame will display customers details from surface according the search query and filters
        customerListFrame = Frame(mainFrame)
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
        for i in range(100):
            customerListBox.insert(END, f"customer Id : {i} | name {"Yash"} | amount : 34000 | date : 2/2/2 | mobile : 9999999999 | aadhar : 123456789012")

        #work of customerListFrame ends here
        
if __name__ == "__main__":
    root = Tk()
    root.geometry("500x500")
    root.title("Customers")
    Customer(root)
    root.mainloop()