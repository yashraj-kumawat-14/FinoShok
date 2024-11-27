#importing necessary modules and variables
import mysql.connector 
from sys import path
import os
#adding this path search so that interpreter can search modules and import it from this directory 
path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../config")
from pathConfig import ALLPATHS
path.extend(ALLPATHS)
from pathConfig import CUSTOMERPHOTOPATH, GUARRANTERPHOTOPATH, DEFAULTIMAGEPATH

#importing necessary things present in databaseConfig.py file present in config folder
from databaseConfig import HOSTNAME, USER, PASSWORD, DATABASE

class Database:
    def fetchData(self, query):
        print(query)
        #making connection with database
        conn = mysql.connector.connect(host=HOSTNAME, user=USER, password=PASSWORD, database=DATABASE)

        #creating cursor to perform queries and get results
        cursor = conn.cursor()

        try:
            #executing query
            cursor.execute(query)
            #fetching data
            data = cursor.fetchall()
            #closing connections with server and database
            cursor.close()
            conn.close()
            return data  
        except mysql.connector.Error as error:
            print("error in the query", error)
            #undoing the changes made by wrong query
            conn.rollback()
            #returning false as symbol of error in query
            return False
    
    def dataModify(self, query):
        print(query)
        #making connection with database
        conn = mysql.connector.connect(host=HOSTNAME, user=USER, password=PASSWORD, database=DATABASE)

        #creating cursor to perform queries and get results
        cursor = conn.cursor()

        #executing query
        try:
            #executing query
            cursor.execute(query)
            #commiting the changes
            conn.commit()
            # losing connections with server and database
            cursor.close()
            conn.close()
            return True   
        except mysql.connector.Error as error:
            print("error in the query", error)
            #undoing teh changes made during wrong query execution
            conn.rollback()
            #returning false means query execution failed
            return False
        
    