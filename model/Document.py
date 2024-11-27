#importing necessary modules
import sys
#adding this path to searcheable
sys.path.append(r"/home/yhj/Desktop/finoshok")
from model import Model

class Document(Model):
    #fillable insertion will only occur in the columns present in fillable variable
    #setting the tablename to customers to work with only customers table
    fillable=["customer_id", "doc_name", "doc_path", "status", "submitted_date", "returned_date", "required", "verified", "file_id"]
    tableName="documents"