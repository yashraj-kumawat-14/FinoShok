# imorting database class to make connection with database and execute quereis and fetch data accordingly
from database.database import Database

class Model:
    #should be changed while dealing with another table
    fillable=["col1", "col2", "col3", "col4", "col5"]
    tableName= "tableName"

    def rowCount(self):
        #creating a database object
        object = Database()

        #getting all data and using len to determine the num of rows
        numOfRows = len(object.fetchData(f"select * from `{self.tableName}`"))

        #returning the row numbers
        return numOfRows
    
    def readAllData(self):
        #creating a database object
        object = Database()

        data = object.fetchData(f"select * from `{self.tableName}`")

        #returning the data
        return data
    
    def readData(self, numRow):
        #creating a database object
        object = Database()

        data = object.fetchData(f"select * from `{self.tableName}`")[0:numRow] #getting n number of rows from the list

        #returning the data
        return data
    
    #it takes arbitary keyword arguments parameters in the dictionary and filters them and insert into the table
    def insertData(self, **kwargs):
        #it checks if self.fillable is empty or not . if it is empty then it will not procced the suite
        if(self.fillable):
            #assingning the kwargs to data variable
            data = kwargs

            #tempKeys holds the keys present data dictionary. these keys are temporary and might change due to filtration in next lines of code
            tempKeys = list(data.keys())

            # iterating through tempKeys
            for key in tempKeys:
                #if there is a key which isn't in self.fillable then it will remove it from the data
                if(key not in self.fillable):
                    data.pop(key)

            #creating a empty list
            columns=list()

            #again creating tempKeys to get latest keys present in the data after filtration
            tempKeys = list(data.keys())

            #iterating through tempkeys to manipulate string and do some necessary concatenation before executing or inserting the data
            for key in tempKeys:
                columns.append("`"+str(key)+"`")
            
            #join function is a string method that concatenates the elements of an iterable such as list into a single string , using a specified separator.
            columns=" ,".join(columns)

            values=list()
            tempValues = list(data.values())

            for value in tempValues:
                values.append("'"+str(value)+"'")
            values=" ,".join(values)


            #creating a database object
            object = Database()

            #returning true means succeessful insertion and false for unsuccessfull  insertion
            return (object.dataModify(f"INSERT INTO `{self.tableName}` ({columns}) values ({values})"))
        
    def deleteRow(self, id):
        #creating a database object
        object = Database()

        #returning true means succeessful deletion and false for unsuccessfull  deletion of row
        return (object.dataModify(f"delete from `{self.tableName}` where id={id}"))

    def updateData(self, id, **kwargs):
         #it checks if self.fillable is empty or not . if it is empty then it will not procced the suite
        if(self.fillable):
            #assingning the kwargs to data variable
            data = kwargs

            #tempKeys holds the keys present data dictionary. these keys are temporary and might change due to filtration in next lines of code
            tempKeys = list(data.keys())

            # iterating through tempKeys
            for key in tempKeys:
                #if there is a key which isn't in self.fillable then it will remove it from the data
                if(key not in self.fillable):
                    data.pop(key)

            #creating a empty list
            columns=list()

            #again creating tempKeys to get latest keys present in the data after filtration
            tempKeys = list(data.keys())

            #iterating through tempkeys to manipulate string and do some necessary concatenation before executing or inserting the data
            for key in tempKeys:
                columns.append("`"+key+"`")

            values=list()
            tempValues = list(data.values())

            for value in tempValues:
                values.append("'"+str(value)+"'")

            #FORMATED STRING
            formattedString = ""
            for i in range(len(data)):
                formattedString+= columns[i]+"="+values[i]
                if(i!=len(data)-1):
                    formattedString+=","
            
            #creating a database object
            object = Database()
            
            #returning true means succeessful insertion and false for unsuccessfull  insertion
            return (object.dataModify(f"update `{self.tableName}` SET {formattedString} where `id` = {id}"))
    
    #fetching data based on prevalues of columns
    def whereData(self, **kwargs):
        data = kwargs
        #creating a empty list
        columns=list()

        #again creating tempKeys to get latest keys present in the data after filtration
        tempKeys = list(data.keys())

        #iterating through tempkeys to manipulate string and do some necessary concatenation before executing or inserting the data
        for key in tempKeys:
            columns.append("`"+key+"`")

        values=list()
        tempValues = list(data.values())

        for value in tempValues:
            values.append("'"+str(value)+"'")

        #FORMATED STRING
        formattedString = ""
        for i in range(len(data)):
            formattedString+= columns[i]+"="+values[i]+"and"

        formattedString=formattedString.rstrip("and") 

        #creating a database object
        object = Database()

        #returning true means succeessful fething and false for unsuccessfull  fetching
        return (object.fetchData(f"select * from `{self.tableName}` where {formattedString}"))
  

