#importing necessary modules and variables
import mysql.connector 
import sys #importing sys module so that we can add config folder to search path

#adding config folder to search path
sys.path.append(r"D:\projects\finoshok\finoshok\config")

#importing necessary things present in databaseConfig.py file present in config folder
from databaseConfig import HOSTNAME, USER, PASSWORD, DATABASE

class Database:
    def fetchData(self, query):
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
        #making connection with database
        conn = mysql.connector.connect(host='localhost', user="root", password="1234", database="finoshok11")

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
        
    