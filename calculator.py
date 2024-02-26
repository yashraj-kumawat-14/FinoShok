from tkinter import *

#here i create a calculator class which requires one parameter as widget frame or Tk window to work properly

class Calculator:
    def __init__(self, calcWindow):
        #coloring of calculator
        commandBg = "orange"
        commandFg = "black"
        numBg = "grey"
        numFg= "white"

        #initial self.result = "0"
        self.result=""

        #creating containers  and other necessary frames
        container = Frame(calcWindow, bg="grey", width=200, height=250)
        container.pack(fill=BOTH, expand=1)
        container.pack_propagate(0) #By setting pack_propagate(0), the frame maintains its specified size (width and height), and it does not automatically adjust to fit its child widgets.

        displayBox = Frame(container, bg="white")
        displayBox.pack(fill=X)

        buttonBox = Frame(container, bg="black")
        buttonBox.pack(fill=BOTH, expand=1)

        #congiguring so that any thing inside just gets centered
        buttonBox.rowconfigure(0, weight=1)
        buttonBox.rowconfigure(1, weight=1)
        buttonBox.rowconfigure(2, weight=1)

        buttonBox.columnconfigure(0, weight=1)
        buttonBox.columnconfigure(1, weight=1)
        buttonBox.columnconfigure(2, weight=1)

        #display widget and the displayVar which stores value in display widget
        displayVar = StringVar()
        displayVar.set("0")
        displayEntry = Entry(displayBox, state="readonly", textvariable=displayVar, cursor="arrow", justify="right", font="COPPER 17 bold")
        displayEntry.pack(fill=X, ipady=10)

        #number buttons
        button7 = Button(buttonBox, text="7", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("7", self.result, displayVar))
        button7.grid(row=0, column=0, pady=1, padx=1)

        button8 = Button(buttonBox, text="8", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("8", self.result, displayVar))
        button8.grid(row=0, column=1, pady=1, padx=1)

        button9 = Button(buttonBox, text="9", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("9", self.result, displayVar))
        button9.grid(row=0, column=2, pady=1, padx=1)

        button4 = Button(buttonBox, text="4", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("4", self.result, displayVar))
        button4.grid(row=1, column=0, pady=1, padx=1)

        button5 = Button(buttonBox, text="5", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("5", self.result, displayVar))
        button5.grid(row=1, column=1, pady=1, padx=1)

        button6 = Button(buttonBox, text="6", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("6", self.result, displayVar))
        button6.grid(row=1, column=2, pady=1, padx=1)

        button1 = Button(buttonBox, text="1", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("1", self.result, displayVar))
        button1.grid(row=2, column=0, pady=1, padx=1)

        button2 = Button(buttonBox, text="2", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("2", self.result, displayVar))
        button2.grid(row=2, column=1, pady=1, padx=1)

        button3 = Button(buttonBox, text="3", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("3", self.result, displayVar))
        button3.grid(row=2, column=2, pady=1, padx=1)

        button0 = Button(buttonBox, text="0", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("0", self.result, displayVar))
        button0.grid(row=3, column=1, pady=1, padx=1)

        #operational buttons
        buttonC = Button(buttonBox, text="C", width=5, height=2, bg="red", fg="black", font="COPPER 13 bold",command=lambda : self.operationAndNum("C", self.result, displayVar))
        buttonC.grid(row=0, column=3, pady=1, padx=1)
        
        buttonMinus = Button(buttonBox, text="-", width=5, height=2, bg=commandBg, fg=commandFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("-", self.result, displayVar))
        buttonMinus.grid(row=1, column=3, pady=1, padx=1)
        
        buttonMul = Button(buttonBox, text="*", width=5, height=2, bg=commandBg, fg=commandFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("*", self.result, displayVar))
        buttonMul.grid(row=2, column=3, pady=1, padx=1)
        
        buttondiv = Button(buttonBox, text="/", width=5, height=2, bg=commandBg, fg=commandFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("/", self.result, displayVar))
        buttondiv.grid(row=3, column=2, pady=1, padx=1)
        
        buttonAns = Button(buttonBox, text="=", width=5, height=2, bg=commandBg, fg=commandFg, font="COPPER 13 bold", command=lambda: self.ans(displayVar))
        buttonAns.grid(row=3, column=3, pady=1, padx=1)
        
        buttonPlus = Button(buttonBox, text="+", width=6, height=2, bg=commandBg, fg=commandFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("+", self.result, displayVar))
        buttonPlus.grid(row=3, column=0, pady=1, padx=1)
    
    def operationAndNum(self, operationName, jj, displayVar):
        if operationName=="C":
            self.result=""
            displayVar.set(self.result)
        else:
            self.result+=operationName
            displayVar.set(self.result)


    def ans(self, displayVar):
        ans = eval(self.result)
        self.result= str(ans)
        displayVar.set(str(ans))

#the below code will run only if the file is run on its own and not by importing it into another file   
if __name__=="__main__":     
    root = Tk()
    root.geometry("200x250")
    Calculator(root)
    root.mainloop()