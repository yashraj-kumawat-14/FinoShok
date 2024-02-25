#importing necessary modules
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as message
import mysql.connector as mysql

#colors used in gui
mainFrameColor = "grey"
statusBarColor = "red"
toolFrameColor = "green"
black = "black"
yellow = "yellow"

#here i made a login using which you can create a window containing a login page

class login:
    #here is constructor which takes a window object like login_window
    def __init__(self, login_window):
        # global result
        login_window.result = False
        mainFrame = Frame(login_window, bg=black)
        mainFrame.pack(fill=BOTH, expand=True)

        mainFrame.rowconfigure(0, weight=1)
        mainFrame.columnconfigure(0, weight=1)

        centerFrame = Frame(mainFrame, bg=black)
        centerFrame.grid(row=0, column=0)

        innerFrame = Frame(centerFrame, bg=black)
        innerFrame.pack()

        userLabel = Label(innerFrame, text="Username : ", bg=black, fg=yellow)
        userLabel.grid(row=0, column=0)
        password = Label(innerFrame, text="Password : ", bg=black, fg=yellow)
        password.grid(row=1, column=0)

        self.userVar = StringVar()
        self.passwordVar = StringVar()
        
        userEntry = Entry(innerFrame, textvariable=self.userVar)
        userEntry.grid(row=0, column=1)
        passwordEntry = Entry(innerFrame, textvariable=self.passwordVar, state='normal')
        passwordEntry.grid(row=1, column=1)

        loginButton = Button(centerFrame, text="login", bg=black, fg=yellow, command=self.loginCheck)
        loginButton.pack(pady=20)

    #here this function checks if the user and password matches in the users table
    def loginCheck(self):
        # global result
        conn = mysql.connect(host="localhost", user="root", password="1234", database="users")
        cursorobject = conn.cursor()
        cursorobject.execute("select * from users where user = '{}' and password = '{}'".format(self.userVar.get(), self.passwordVar.get()))
        login_window.userDetail = cursorobject.fetchone()
        if(login_window.userDetail):
            login_window.result = True
            login_window.destroy()
        else:
            login_window.result=False            

#here i created a demo window to pass to class login 

login_window = Tk()
login_window.title("Login")
login_window.geometry("200x200")
login_window.resizable(False, False)
login(login_window)
login_window.mainloop()

# checking if the credentials are correct
if(login_window.result):
    
    #initiating the gui
    root = Tk()
    root.geometry("400x400")
    root.title("finoshok")

    #making a menubar
    mainMenubar = Menu(root)
    mainMenubar.add_command(label="hello")
    #making submenubarss
    submenu = Menu(mainMenubar, tearoff=0)
    submenu.add_command(label="raj")
    submenu.add_checkbutton(label="rajj")

    #adding submenu in mainmenybar
    mainMenubar.add_cascade(menu=submenu, label="gile")

    #configuring the menu in root as mainmenubar
    root.config(menu=mainMenubar)

    #creating toolFrame in root

    toolFrame = Frame(root, bg=toolFrameColor)
    toolFrame.pack(side="left", fill="y")

    #CREATING main frame in root

    mainFrame = Frame(root, bg=mainFrameColor)
    mainFrame.pack(fill="both", expand=True)

    #creating a notebook of tabs in mainframe

    my_notebook = ttk.Notebook(mainFrame)
    my_notebook.pack(fill="both", expand=True)

    #creating tabs in notebook

    tab1 = Frame(my_notebook, bg=mainFrameColor)
    tab2 = Frame(my_notebook, bg=toolFrameColor)
    tab1.pack(fill="both", expand=True)
    tab2.pack(fill="both", expand=True)

    my_notebook.add(tab1, text="yashraj")
    my_notebook.add(tab2, text="kumawat")

    #navigation buttons for tabs
    def hide():
        my_notebook.hide(1)
    def show():
        my_notebook.add(tab2, text="kumawat")
    def select():
        my_notebook.select(1)


    hideButton = Button(tab1, text="hide tab 2", command=hide)
    hideButton.pack()

    showButton = Button(tab1, text="show tab 2", command=show)
    showButton.pack()

    selectButton = Button(tab1, text="select tab 2", command=select)
    selectButton.pack()

    #creating a status bar
    statusBar = Frame(root, bg=statusBarColor)
    statusBar.pack(side="bottom", fill="x")


    root.mainloop()