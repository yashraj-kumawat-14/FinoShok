#importing necessary modules
import sys
#adding this path to searcheable
sys.path.append(r"D:\projects\finoshok\finoshok")
from model import Model

class Request(Model):
    #fillable insertion will only occur in the columns present in fillable variable
    #setting the tablename to customers to work with only customers table
    fillable=["customer_id", "purpose", "requested_amount", "date", "status"]
    tableName="requests"