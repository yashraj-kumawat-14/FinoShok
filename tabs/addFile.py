from tkinter import Tk, Frame, Label, Listbox, Scrollbar, END
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

        subFrame2 = Frame(mainFrame, bg=subFrame2Color, relief="groove", border=3)
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
        section2.pack(fill="both", expand=True)

        #section 3 for showing selected loan request details along with some customer details

        section3 = Frame(subFrame3)
        section3.pack(fill="both", expand=True) 

        #now filling in these sections
        #section 1 work start-------

        #creating a section3 as more responsive  using rowconfigure and columnconfigure

        section1.rowconfigure(0, weight=1)
        section1.columnconfigure(0, weight=1)
        customerRequestBox = Listbox(section1)
        customerRequestBox.grid(row=0, column=0, sticky="nsew")


        # creating scrollbar for y direction
        scrollY = Scrollbar(customerRequestBox, command=customerRequestBox.yview)
        scrollY.pack(side="right", fill="y")
        customerRequestBox.config(yscrollcommand=scrollY.set)


        # scroll = Scrollbar(section1)
        # scroll.pack()
        for i in range(100):
            customerRequestBox.insert(END, f"customer Id : {i} | name {i} | date : 2/2/2 | amount : 34000 |")

        #section 1 work ends----
        
        #section 2 work starts ----
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
        customerEntryLabel = Label(detailsInnerFrame, text="Yashraj ")
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
