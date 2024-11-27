#importing necessary modules
import sys
#adding this path to searcheable
sys.path.append(r"/home/yhj/Desktop/finoshok")
from model import Model

class Customer(Model):
    #fillable insertion will only occur in the columns present in fillable variable
    #setting the tablename to customers to work with only customers table
    fillable=["name", "father", "mobile", "home_address", "work_address", "aadhar", "photo", "status"]
    tableName="customers"