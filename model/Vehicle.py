#importing necessary modules
import sys
#adding this path to searcheable
sys.path.append(r"D:\projects\finoshok\finoshok")
from model import Model

class Vehicle(Model):
    #fillable insertion will only occur in the columns present in fillable variable
    #setting the tablename to customers to work with only customers table
    fillable=["customerId", 'name', 'plateNum', 'model', 'manufacturer', 'note', 'fuel', 'engineCC', 'horsePowerBHP', 'cyilenders' ,'fuelCapacity' ,'seatingCapacity', 'vehicleWeightKG', 'status', 'currentCondition']

    tableName="vehicles"