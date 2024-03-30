from tkinter import *
from PIL import Image, ImageTk

class Client:
    def __init__(self, clientWindow):
        mainFrame = Frame(clientWindow)
        mainFrame.pack(fill="both", expand=True)

        mainFrame.rowconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)
        mainFrame.rowconfigure(2, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=1)
        mainFrame.columnconfigure(2, weight=1)
        mainFrame.columnconfigure(3, weight=1)

        customerDetailsFrame = Frame(mainFrame, bg="red")
        customerDetailsFrame.grid(row=0, column=0, sticky="nsew", columnspan=4)

        customerDetailsFrame.rowconfigure(0, weight=1)
        customerDetailsFrame.columnconfigure(0, weight=1)
        customerDetailsFrame.columnconfigure(1, weight=1)

        filesFrame = Frame(mainFrame, bg="pink")
        filesFrame.grid(row=1, column=0, sticky="nsew", rowspan=2)

        fileExcelFrame = Frame(mainFrame, bg="blue")
        fileExcelFrame.grid(row=1, column=1, sticky="nsew", rowspan=2, columnspan=4)

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
        customerEntryLabel = Label(detailsInnerFrame, text="Yashraj")
        customerEntryLabel.grid(row=0, column=1)

        aadharEntryLabel = Label(detailsInnerFrame, text="989898989012 ")
        aadharEntryLabel.grid(row=1, column=1)

        mobileEntryLabel = Label(detailsInnerFrame, text="7357446466")
        mobileEntryLabel.grid(row=2, column=1)

if __name__ == "__main__":
    root = Tk()
    root.title("Client")
    root.geometry("500x500")
    object = Client(root)
    root.mainloop()