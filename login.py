from sys import path
import os
#adding this path search so that interpreter can search modules and import it from this directory 
path.append(f"{os.path.dirname(os.path.abspath(__file__))}/config")
from pathConfig import ALLPATHS
path.extend(ALLPATHS)
from databaseConfig import DATABASE, PASSWORD, USER
from tkinter import *
import mysql.connector as mysql


#here i made a login using which you can create a window containing a login page

class Login:
    #here is constructor which takes a window object like login_window
    def __init__(self, login_window):
        black = "black"
        yellow = "yellow"
        #initail value of result is set to false
        login_window.result = False
        
        #getting the display's and login_window  widhth and height
        login_window.update() #update ensures that the window has been updated to its actual size before you attempt to calculate the center coordinates.

        screenWidth = login_window.winfo_screenwidth()
        screenHeight = login_window.winfo_screenheight()
        x = (screenWidth-login_window.winfo_width())//2
        y = (screenHeight-login_window.winfo_height())//2
        
        #setting the position of login window to center of display
        login_window.geometry(f"+{x}+{y}")

        loginLabel = Label(login_window, text="Enter login credentials : ", font="COPPER 10", fg=yellow, bg=black)
        loginLabel.pack(side="top", fill=X)

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

        loginButton = Button(centerFrame, text="login", bg=black, fg=yellow, command=lambda:self.loginCheck(login_window, loginLabel))
        loginButton.pack(pady=20)

    #here this function checks if the user and password matches in the users table
    def loginCheck(self, login_window, loginLabel):
        # global result
        conn = mysql.connect(host="localhost", user=USER, password=PASSWORD, database=DATABASE)
        cursorobject = conn.cursor()
        cursorobject.execute("select * from admins where username = '{}' and password = '{}'".format(self.userVar.get(), self.passwordVar.get()))
        login_window.userDetail = cursorobject.fetchone()
        if(login_window.userDetail):
            login_window.result = True
            login_window.destroy()
        else:
            login_window.result=False
            loginLabel.config(text="Wrong username password\n combination", fg="red")


#here i created a demo window to pass to class login 
if __name__=="__main__":
    login_window = Tk()
    login_window.title("Login")
    login_window.geometry("200x200")
    login_window.resizable(False, False)
    Login(login_window)
    login_window.mainloop()
