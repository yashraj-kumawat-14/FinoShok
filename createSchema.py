#import mysql.connector to do connection with mysql server
import mysql.connector as connector
from config.databaseConfig import DATABASE, USER, PASSWORD, HOSTNAME

#establish connection
conn = connector.connect(host=HOSTNAME, user=USER, password=PASSWORD)

#make a cursor object to execute queries
cursor = conn.cursor()

#create database if not exists
cursor.execute(f'drop database if exists {DATABASE}')
cursor.execute(F"create database if not exists {DATABASE}")

#selecting the database
cursor.execute(F"use {DATABASE}")

#create admins table
cursor.execute("""CREATE TABLE IF NOT EXISTS `admins` (
  `id` int NOT NULL,
  `username` text,
  `password` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci""")

#create customers table
cursor.execute("""CREATE TABLE IF NOT EXISTS `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text,
  `father` text,
  `mobile` bigint DEFAULT NULL,
  `home_address` text,
  `work_address` text,
  `aadhar` bigint DEFAULT NULL,
  `photo` text,
  `status` int DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `aadhar` (`aadhar`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci""")

#create documents table
cursor.execute("""CREATE TABLE IF NOT EXISTS `documents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int DEFAULT NULL,
  `doc_name` varchar(60) DEFAULT NULL,
  `doc_path` text,
  `status` int DEFAULT NULL,
  `submitted_date` date DEFAULT NULL,
  `returned_date` date DEFAULT NULL,
  `required` int DEFAULT NULL,
  `verified` int DEFAULT NULL,
  `file_id` int NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `documents_chk_1` CHECK ((`doc_name` in (_utf8mb4'aadhar',_utf8mb4'janaadhar',_utf8mb4'pancard',_utf8mb4'cheque',_utf8mb4'photo',_utf8mb4'stamp',_utf8mb4'mobileNum',_utf8mb4'stamp',_utf8mb4'rc')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci""")

#create files table
cursor.execute("""CREATE TABLE IF NOT EXISTS `files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customerId` int DEFAULT NULL,
  `loanAmount` int DEFAULT NULL,
  `interest` int DEFAULT NULL,
  `timePeriod` int DEFAULT NULL,
  `status` int DEFAULT NULL,
  `emiAmount` int DEFAULT NULL,
  `numEmi` int DEFAULT NULL,
  `note` text,
  `dateApproved` date DEFAULT NULL,
  `guarranterId` int DEFAULT NULL,
  `loanType` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci""")

#create guarranters table of customer
cursor.execute("""CREATE TABLE IF NOT EXISTS `guarranters` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `name` text,
  `father` text,
  `mobile` bigint DEFAULT NULL,
  `home_address` text,
  `work_address` text,
  `aadhar` bigint NOT NULL,
  `status` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci""")

#create ledgers table
cursor.execute("""CREATE TABLE IF NOT EXISTS `ledgers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fileId` int NOT NULL,
  `emiNumber` int DEFAULT NULL,
  `status` int DEFAULT '0',
  `emiDate` date DEFAULT NULL,
  `emiAmount` int DEFAULT NULL,
  `paidDate` date DEFAULT NULL,
  `penalty` int DEFAULT '0',
  `paidAmount` int DEFAULT '0',
  `Note` varchar(1000) DEFAULT 'Nothing',
  `paidBy` varchar(1000) DEFAULT 'Nothing',
  `paidVia` varchar(1000) DEFAULT 'Nothing',
  `remainingAmount` int GENERATED ALWAYS AS (((`emiAmount` - `penalty`) - `paidAmount`)) VIRTUAL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci""")

#create requests table
cursor.execute("""CREATE TABLE IF NOT EXISTS `requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int DEFAULT NULL,
  `requested_amount` int DEFAULT NULL,
  `purpose` text,
  `date` date DEFAULT NULL,
  `status` int DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_date_customer_id` (`date`,`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci""")

#create vehicles table
cursor.execute("""CREATE TABLE IF NOT EXISTS `vehicles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customerId` int DEFAULT NULL,
  `name` text,
  `plateNum` text,
  `model` varchar(100) DEFAULT NULL,
  `manufacturer` text,
  `note` text,
  `fuel` varchar(50) DEFAULT NULL,
  `engineCC` int DEFAULT NULL,
  `horsePowerBHP` int DEFAULT NULL,
  `cyilenders` int DEFAULT NULL,
  `fuelCapacity` float DEFAULT NULL,
  `seatingCapacity` float DEFAULT NULL,
  `vehicleWeightKG` float DEFAULT NULL,
  `status` int DEFAULT NULL,
  `currentCondition` varchar(50) DEFAULT NULL,
  `fileId` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci""")

#commiting changes
conn.commit()

# closing connections and cursor
cursor.close()
conn.close()