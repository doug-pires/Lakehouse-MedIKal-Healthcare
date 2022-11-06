import generate.fake_data_hospital as h
import generate.streaming_distribution as s
import os
from dotenv import load_dotenv

# Load  Environment Variables from the .env file
load_dotenv()
admin_postgres = os.getenv("ADMIN_POSTGRES")
admin_mysql = os.getenv("ADMIN_MYSQL")
password = os.getenv("PASSWORD_DATABASES")
host_mysql = os.getenv("SERVER_MYSQL")
host_postgres = os.getenv("SERVER_POSTGRES")


# Azure Postgres
postgres_azure = h.Pharmacy(host=host_postgres, database="ikhospital",
                            user=admin_postgres, password=password)

postgres_azure.tbl_medicines(
    table_schema='pharmacy', table_medicine='medicine')


# Azure MySQL
mysql_azure = h.Hospital(qty_patients=1000, user=admin_mysql, password=password,
                         host=host_mysql, database="ikhospital")

mysql_azure.tbl_doctors(table_doctors="doctors")
mysql_azure.tbl_shift(table_shift="shift")

mysql_azure.tbl_patient(table_patient="patient")
mysql_azure.tbl_events(table_events="events")


s.run_streaming(qty_patients=1000, min_to_run=5)
