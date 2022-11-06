CREATE DATABASE ikhospital;
CREATE SCHEMA pharmacy

CREATE TABLE pharmacy.medicine 
( 
    ID  SERIAL PRIMARY KEY NOT NULL,
    brand_name TEXT ,
    generic_name TEXT ,
    manufacturer_name TEXT,
    product_ndc TEXT ,
    product_type TEXT ,
    route TEXT,
    substance_name TEXT 


 )

SELECT * FROM medicine
-- DROP TABLE medicine
TRUNCATE TABLE medicine RESTART IDENTITY 

--table_catalog == 'ikhospital'
-- table_schema == 'public'
-- table_name == 'medicine'
SELECT * FROM information_schema.tables 
WHERE table_schema = 'public'



SELECT 
table_catalog
,table_schema 
,table_name
 FROM information_schema.tables 
WHERE table_catalog = 'ikhospital' AND table_schema = 'pharmacy'
