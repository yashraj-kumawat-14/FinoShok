from tkinter import *

#here i create a calculator class which requires one parameter as widget frame or Tk window to work properly

class Calculator:
    def __init__(self, calcWindow):
        #coloring of calculator
        commandBg = "orange"
        commandFg = "black"
        numBg = "grey"
        numFg= "white"

        self.tempCalcWindow = calcWindow

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

        #display widget and the self.displayVar which stores value in display widget
        self.displayVar = StringVar()
        self.displayVar.set("0")
        displayEntry = Entry(displayBox, state="readonly", textvariable=self.displayVar, cursor="arrow", justify="right", font="COPPER 17 bold")
        displayEntry.pack(fill=X, ipady=10)

        #number buttons
        button7 = Button(buttonBox, text="7", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("7"))
        button7.grid(row=0, column=0, pady=1, padx=1)

        button8 = Button(buttonBox, text="8", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("8"))
        button8.grid(row=0, column=1, pady=1, padx=1)

        button9 = Button(buttonBox, text="9", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("9"))
        button9.grid(row=0, column=2, pady=1, padx=1)

        button4 = Button(buttonBox, text="4", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("4"))
        button4.grid(row=1, column=0, pady=1, padx=1)

        button5 = Button(buttonBox, text="5", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("5"))
        button5.grid(row=1, column=1, pady=1, padx=1)

        button6 = Button(buttonBox, text="6", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("6"))
        button6.grid(row=1, column=2, pady=1, padx=1)

        button1 = Button(buttonBox, text="1", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("1"))
        button1.grid(row=2, column=0, pady=1, padx=1)

        button2 = Button(buttonBox, text="2", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("2"))
        button2.grid(row=2, column=1, pady=1, padx=1)

        button3 = Button(buttonBox, text="3", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("3"))
        button3.grid(row=2, column=2, pady=1, padx=1)

        button0 = Button(buttonBox, text="0", width=6, height=2, bg=numBg, fg=numFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("0"))
        button0.grid(row=3, column=1, pady=1, padx=1)

        #operational buttons
        buttonC = Button(buttonBox, text="C", width=5, height=2, bg="red", fg="black", font="COPPER 13 bold",command=lambda : self.operationAndNum("C"))
        buttonC.grid(row=0, column=3, pady=1, padx=1)
        
        buttonMinus = Button(buttonBox, text="-", width=5, height=2, bg=commandBg, fg=commandFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("-"))
        buttonMinus.grid(row=1, column=3, pady=1, padx=1)
        
        buttonMul = Button(buttonBox, text="*", width=5, height=2, bg=commandBg, fg=commandFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("*"))
        buttonMul.grid(row=2, column=3, pady=1, padx=1)
        
        buttondiv = Button(buttonBox, text="/", width=5, height=2, bg=commandBg, fg=commandFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("/", self.displayVar))
        buttondiv.grid(row=3, column=2, pady=1, padx=1)
        
        buttonAns = Button(buttonBox, text="=", width=5, height=2, bg=commandBg, fg=commandFg, font="COPPER 13 bold", command=lambda: self.ans())
        buttonAns.grid(row=3, column=3, pady=1, padx=1)
        
        buttonPlus = Button(buttonBox, text="+", width=6, height=2, bg=commandBg, fg=commandFg, font="COPPER 13 bold", command=lambda : self.operationAndNum("+"))
        buttonPlus.grid(row=3, column=0, pady=1, padx=1)

        #by default the focus will be given to root window as it is created first so i moved the focus to calculator window in first
        
        calcWindow.bind("<Key>", self.keyBoardHandler)
        for child in calcWindow.winfo_children():
            child.bind("<Key>", self.keyBoardHandler)

        #now i bind the container frame with Key event so that when i press numbers on keyboard gui can recognize them
        #container.bind("<Key>", keyBoardHandler)
    
    def keyBoardHandler(self, event):
        if(event.char.isdigit()):
            self.operationAndNum(event.char)
        elif(event.char == "/"):
            self.operationAndNum(event.char)
        elif(event.char == "*"):
            self.operationAndNum(event.char)
        elif(event.char == "+"):
            self.operationAndNum(event.char)
        elif(event.char == "-"):
            self.operationAndNum(event.char)
        elif(event.char == "="):
            self.ans()
        elif(event.keysym == "Return"):
            self.ans()
        else:
            pass

    #this function displays the entry of previous result and the operations or numbers sum as a string on the display
    def operationAndNum(self, operationName):
        self.tempCalcWindow.focus_set()
        if operationName=="C":
            self.result=""
            self.displayVar.set(self.result)
        else:
            self.result+=operationName
            self.displayVar.set(self.result)

    #this ans function evaluates the result in the string format and update result and show it to the display window
    def ans(self):
        ans = eval(self.result)
        self.result= str(ans)
        self.displayVar.set(str(ans))

#the below code will run only if the file is run on its own and not by importing it into another file   
if __name__=="__main__":     
    root = Tk()
    root.geometry("200x250")
    Calculator(root)
    root.mainloop()