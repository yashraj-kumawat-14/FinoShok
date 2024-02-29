#importing necessary modules and variables
import mysql.connector
from config.databaseConfig import HOSTNAME, USER, PASSWORD, DATABASE

class Database:
    def __init__(self, query):
        #making connection with database
        conn = mysql.connector.connect(host=HOSTNAME, user=USER, password=PASSWORD, database=DATABASE)

        #creating cursor to perform queries and get results
        cursor = conn.cursor()

        #executing query
        result = cursor.execute(query)

        cursor.close()
        conn.close()

        #checking if result is not empty
        if(result):
            return result
        else:
            #if result is empty then return False
            return False
        