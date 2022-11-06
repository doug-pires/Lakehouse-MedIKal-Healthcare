
CREATE DATABASE ikhospital;
USE ikhospital;

-- Create table Events
CREATE TABLE IF NOT EXISTS events ( 
ID INT AUTO_INCREMENT NOT NULL,
ID_PATIENT INT NOT NULL,
PATIENT VARCHAR (100),
SEX VARCHAR (2),
AGE INT,
ID_DOCTOR INT,
ID_SMOKE INT,
SYMPTOMS VARCHAR ( 20 ),
DATE_OF_SERVICE DATE,
primary key ( ID )
);

-- TRUNCATE TABLE ikhospital.events;
-- SELECT * FROM ikhospital.events;

-- Create Table Doctors
CREATE TABLE IF NOT EXISTS doctors ( 
ID INT AUTO_INCREMENT NOT NULL,
ID_DOCTOR INT NOT NULL,
AREA VARCHAR (100),
NAME VARCHAR (100),
ID_SHIFT INT,
primary key ( ID )
);

-- TRUNCATE TABLE ikhospital.doctors;
-- SELECT * FROM ikhospital.doctors;

-- Create Table Patient
CREATE TABLE  IF NOT EXISTS patient ( 
ID INT AUTO_INCREMENT NOT NULL,
ID_PATIENT INT NOT NULL,
NAME VARCHAR (100),
SEX VARCHAR (100),
AGE INT,
ADDRESS VARCHAR ( 100 ),
COUNTRY VARCHAR ( 100 ),
NUMBER VARCHAR ( 50 ),
EMAIL VARCHAR ( 100 ),
primary key ( ID )

);
-- ALTER TABLE ikhospital.patient
-- MODIFY COLUMN COUNTRY VARCHAR ( 100 );
-- SELECT * FROM ikhospital.patient;




-- Create Table shift
CREATE TABLE IF NOT EXISTS shift ( 
ID INT AUTO_INCREMENT NOT NULL,
ID_SHIFT INT NOT NULL,
SHIFT_NAME VARCHAR (20),
primary key ( ID )

);




USE ikhospital;
TRUNCATE TABLE doctors;
TRUNCATE TABLE events;
TRUNCATE TABLE patient;
TRUNCATE TABLE shift;


-- SELECT Schema and Table
SELECT table_schema, table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = 'ikhospital'

DROP TABLE distribution_medicines;
