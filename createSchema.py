#import mysql.connector to do connection with mysql server
import mysql.connector as connector
from config.databaseConfig import DATABASE, USER, PASSWORD, HOSTNAME

#establish connection
conn = connector.connect(host=HOSTNAME, user=USER, password=PASSWORD)

#make a cursor object to execute queries
cursor = conn.cursor()

#create database if not exists
cursor.execute(F"create database if not exists {DATABASE}")

#selecting the database
cursor.execute(F"use {DATABASE}")

#create customers table
cursor.execute("create table if not exists customers(id int primary key, name text, father text, mobile bigint, home_address text, work_address text, aadhar bigint, photo text, status int)")

#create files table
cursor.execute("create table if not exists files(id int primary key, customer_id int, loan_amount bigint, interest_rate int, time_period_months int, file_status int, emi_amount bigint, num_of_emi int, note text)")

#create ledger table
cursor.execute("create table if not exists ledger(id int primary key, file_id int, emi_th_num int, emi_amount bigint, status int, emi_date datetime, emi_paid_date datetime, penalty int, paid_amount bigint, note text)")

#create admins table
cursor.execute("create table if not exists admins(id int primary key, username text, password varchar(14))")

#create partners table of customer
cursor.execute("create table if not exists partners(id int primary key, customer_id int,name text, father text, mobile bigint, home_address text, work_address text, aadhar bigint, photo text, status int)")

#create vehicles table
cursor.execute("create table if not exists vehicles(id int primary key, customer_id int, name text, plate_num text, model int, manufacturer text)")

#create documents table
cursor.execute("create table if not exists documents(id int primary key, customer_id int, doc_name text, doc_path text, status int, submitted_date datetime, returned_date datetime)")

#commiting changes
conn.commit()

# closing connections and cursor
cursor.close()
conn.close()