# Create Fake Data for IK Hospital using Classes
from faker import Faker
import random
import os
import datetime
import time
import mysql.connector
import psycopg2
from contextlib import contextmanager
import generate.api_medicines as api_medicines


class Hospital:

    # ID for General Doctors
    id_general_doctors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                          13, 14, 15, 16, 17, 18]

    general_areas = ["Allergist", "Cardiologist", "Dermatologist",
                     "Oncologist", "Ophthalmologist", "General"]

    general_doctors = ["Robert Junior", "Sullivan Colt", "Jon Doe", "Jane Stephen",
                       "Marcia Ribeiro", "Zoey Colleman", "Francis Gistalt", "Arshad Renno",
                       "Daniel Guttenbeck", "Roberto Gonzaga", "David Tior", "Daniel Martinez",
                       "Pablo Moreira", "Igor Albuquerque", "Peter Astut", "Melinna Alves", "Catarina Cussolim", "Alberto Mezzani"]

    symptomns_each_area = {
        "General": ["Cough", "Fever", "Sore throat", "Chest pains", "Headaches", "Heartburn"],
        "Allergist": ["Rhinitis", "Sinusitis"],
        "Oncologist": ["Cancer"],
        "Cardiologist": ["Heart Attack", "High Blood Pressure"],
        "Dermatologist": ["Pimple", "Wart", "Dandruff"],
        "Pediatrician": ["Fever", "Diarrhea", "Heartburn", "Cough"],
    }

    # ID for Female Doctors
    id_doctors_female = [19, 20, 21, 22, 23, 24]
    female_areas = ["Gynaecologist", "Obstetrician"]
    female_doctors = ["Mark Constantine", "Dakota Dunlap",
                      "Wendy Ray", "Tammy White", "Laura Johnson", "Nathan Patel"]
    # ID for Male Doctors
    id_doctors_male = [25, 26, 27]
    male_areas = ["Urologist"]
    male_doctors = ["Lucas Piantolli", "Brad Felgucci Jr",
                    "Nuno Goncalves"]

    # Areas and Doctor for Child
    id_doctors_child = [28, 29, 30]
    child_areas = ["Pediatrician"]
    child_doctors = ["Barion Dunno", "Dick Harper", "Jane Bartilda"]

    # ID Shift
    id_shift = [1, 2, 3]
    #################################################################
    ids_smoke = [1, 2, 3]
    #############
    email_providers = ["@google.com", "@outlook.com",
                       "@company.com", "@hotmail.com"]

    def __init__(self, qty_patients: int, user, password, host, database) -> None:
        self.qty_patients = qty_patients
        # Locale
        self.locale = ['de-DE',  'it_IT', 'fr_FR',
                       'en_US', "en_GB", "es_MX", 'pt_BR', 'pt_PT']
        # Hold ALL My patients
        self.fakes_patients = []
        # Hold ALL My Areas - Specialty - Doctors
        self.all_areas = []
        # Hold Credentials for the Database
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # Generate ALL my Patients
        for _ in range(self.qty_patients):
            f = Faker(self.locale)

            # get Random domain email
            email = random.choice(self.email_providers)

            # Generate a MALE PATIENT
            fake_male_name = f.name_male()
            fake_email_male = fake_male_name[3:8] + \
                str(random.randint(0, 1800)) + email
            male = [fake_male_name, "M",
                    fake_email_male.replace(" ", "").strip(".").lower()]

            # Generate a FEMALE PATIENT
            fake_name_female = f.name_female()
            fake_email_female = fake_name_female[3:8].lower(
            ) + str(random.randint(0, 1800)) + email
            femnale = [fake_name_female, "F",
                       fake_email_female.replace(" ", "").lower()]

            # Generate a PROFILE PATIENT
            profile = f.profile()
            random_profile = [profile["name"], profile["sex"], profile["mail"]]

            # SELECT RANDOMLY Between them
            list_patient = [male,
                            femnale, random_profile]

            # Extract the Information
            fake_profile = random.choice(list_patient)
            fake_name = fake_profile[0]
            fake_sex = fake_profile[1]
            fake_email = fake_profile[2]
            fake_age = random.randint(0, 115)
            fake_adress = f.address()
            fake_country = f.country()
            fake_number = f.phone_number()

            self.fakes_patients.append(
                [_ + 1, fake_name, fake_sex, fake_age, fake_adress, fake_country, fake_number, fake_email])

        # Generate ALL my Doctors
        #######################################

        # At least 3 doctors per shift
        qty_id_shifts = len(self.id_shift)

        # General Doctors
        at_least_one_area_per_shift_general = [
            [d] * qty_id_shifts for d in self.general_areas]
        areas_general = [
            i for l in at_least_one_area_per_shift_general for i in l]
        zip_general = zip(self.id_general_doctors, areas_general,
                          self.general_doctors, self.id_shift * len(self.id_general_doctors))
        list_general = [[i, a, d, s]for i, a, d, s in zip_general]

        # Male Area
        at_least_one_area_per_shift_male = [
            [d] * qty_id_shifts for d in self.male_areas]
        areas_male = [i for l in at_least_one_area_per_shift_male for i in l]
        zip_male = zip(self.id_doctors_male, areas_male, self.male_doctors,
                       self.id_shift * len(self.id_doctors_male))
        list_male = [[i, a, d, s]for i, a, d, s in zip_male]

        # Female Area
        at_least_one_area_per_shift_female = [
            [d] * qty_id_shifts for d in self.female_areas]
        areas_female = [
            i for l in at_least_one_area_per_shift_female for i in l]
        zip_female = zip(self.id_doctors_female, areas_female, self.female_doctors,
                         self.id_shift * len(self.id_doctors_female))
        list_female = [[i, a, d, s]for i, a, d, s in zip_female]

        # Child Area
        at_least_one_area_per_shift_child = [
            [d] * qty_id_shifts for d in self.child_areas]
        areas_child = [
            i for l in at_least_one_area_per_shift_child for i in l]
        zip_child = zip(self.id_doctors_child, areas_child, self.child_doctors,
                        self.id_shift * len(self.id_doctors_child))
        list_child = [[i, a, d, s]for i, a, d, s in zip_child]

        # Bring together ALL AREAS and DOCTORS
        [self.all_areas.append(g) for g in list_general]
        [self.all_areas.append(f)for f in list_female]
        [self.all_areas.append(m)for m in list_male]
        [self.all_areas.append(c)for c in list_child]

    @contextmanager
    def OpenConn(self):
        conn = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database)
        try:
            yield conn
        finally:
            conn.close()

    def tbl_events(self, table_events):
        self.table_events = table_events

        min_to_run = datetime.timedelta(minutes=60)
        hora_inicio = datetime.datetime.today()
        hora_termino = datetime.datetime.today() + min_to_run

        while True:

            p = random.choice(self.fakes_patients)

            # Send patient each n Seconds
            time.sleep(2)

            id_patient = p[0]
            patient = p[1]
            sex = p[2]
            age = p[3]
            # Rules to my events
            if sex == "M":
                random_general = random.choice(self.id_general_doctors)
                random_male = random.choice(self.id_doctors_male)
                id_doctor = random.choice(
                    [random_general, random_male])
            elif sex == "F" and age >= 16:
                random_general = random.choice(self.id_general_doctors)
                random_female = random.choice(self.id_doctors_female)
                id_doctor = random.choice(
                    [random_general, random_female])
            elif age <= 12:
                random_general = random.choice(self.id_general_doctors)
                random_child = random.choice(self.id_doctors_child)
                id_doctor = random.choice(
                    [random_general, random_child])

            if age >= 16:
                id_smoke = random.choice(self.ids_smoke)
            else:
                id_smoke = None

            # Get SYMPTOMS accordingly for each DOCTOR/AREA set
            area_w_symptoms = list(self.symptomns_each_area.keys())
            # Check if we have SYMPTOMS set for each especific area
            check_area = [l[0:2]
                          for l in self.all_areas if l[1] in area_w_symptoms]

            # Check if the RANDOM ID DOCTOR is on the list
            check_id = [l for l in check_area if id_doctor in l]

            try:
                get_area = check_id[0][1]

                if get_area == "General":
                    symptoms = random.choice(
                        self.symptomns_each_area.get("General"))
                elif get_area == "Allergist":
                    symptoms = random.choice(
                        self.symptomns_each_area.get("Allergist"))
                elif get_area == "Oncologist":
                    symptoms = random.choice(
                        self.symptomns_each_area.get("Oncologist"))
                elif get_area == "Cardiologist":
                    symptoms = random.choice(
                        self.symptomns_each_area.get("Cardiologist"))
                elif get_area == "Dermatologist":
                    symptoms = random.choice(
                        self.symptomns_each_area.get("Dermatologist"))
                elif get_area == "Pediatrician":
                    symptoms = random.choice(
                        self.symptomns_each_area.get("Pediatrician"))
            except:
                symptoms = None

            # Date of Service
            start_date = datetime.date(2020, 1, 1)
            end_date = datetime.date.today()

            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            date_of_service = start_date + \
                datetime.timedelta(days=random_number_of_days)

            # Prepare Data to INSERT
            tuple_data = (id_patient, patient, sex,
                          age, id_doctor, id_smoke, date_of_service, symptoms)
            cmd_to_print = f"INSERT INTO {self.database}.{ self.table_events} (id_patient ,patient, sex, age, id_doctor, id_smoke, date_of_service,symptoms ) VALUES ( {id_patient}, '{patient}', '{sex}',{age}, {id_doctor},{id_smoke},{date_of_service},'{symptoms}')"
            cmd_insert_values = f"INSERT INTO {self.database}.{ self.table_events} (id_patient, patient, sex, age, id_doctor, id_smoke, date_of_service,symptoms ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
            print(cmd_to_print)

            # Add Patient to the Database
            with self.OpenConn() as conn:
                cursor = conn.cursor()
                cursor.execute(cmd_insert_values, tuple_data)
                cursor.close()
                conn.commit()

    def tbl_doctors(self, table_doctors):
        self.table_doctors = table_doctors

        # Make our table IDEMPOTENCE by truncating it

        command_to_truncate = f"TRUNCATE TABLE {self.database}.{self.table_doctors}"
        with self.OpenConn() as conn:
            cursor = conn.cursor()
            cursor.execute(command_to_truncate)
            cursor.close()
            conn.commit()

        # Prepare Data to INSERT
        for doctor in self.all_areas:

            id_doctor = doctor[0]
            area = doctor[1]
            name = doctor[2]
            shift = doctor[3]

            tuple_data = (id_doctor, area, name, shift)
            # Just to validate the command
            cmd_to_print = f"INSERT INTO {self.database}.{self.table_doctors} (id_doctor ,area, name,id_shift ) VALUES ( {id_doctor}, '{area}', '{name}',{shift})"
            cmd_insert_values = f"INSERT INTO {self.database}.{self.table_doctors} (id_doctor ,area, name,id_shift ) VALUES ( %s, %s, %s, %s)"

            with self.OpenConn() as conn:
                cursor = conn.cursor()
                cursor.execute(cmd_insert_values, tuple_data)
                cursor.close()
                conn.commit()
        print("Created doctors table")

    def tbl_patient(self, table_patient):
        self.table_patient = table_patient

        # Make our table IDEMPOTENCE by truncating it

        command_to_truncate = f"TRUNCATE TABLE {self.database}.{self.table_patient}"

        # Open Connection to the Database
        with self.OpenConn() as conn:
            cursor = conn.cursor()
            cursor.execute(command_to_truncate)
            cursor.close()

            # Commit to Database
            conn.commit()

        for patient in self.fakes_patients:

            id_patient = patient[0]
            name = patient[1]
            sex = patient[2]
            age = patient[3]
            address = patient[4]
            country = patient[5]
            number = patient[6]
            email = patient[7]

            # Prepare Data to INSERT
            tuple_data = (id_patient, name, sex,
                          age, address, country, number, email)
            cmd_to_print = f"INSERT INTO {self.database}.{ self.table_patient} (id_patient ,name, sex, age, address, country, number ,email) VALUES ( {id_patient}, '{name}', '{sex}',{age}, {address},{country},{number},'{email}')"
            cmd_insert_values = f"INSERT INTO {self.database}.{ self.table_patient} (id_patient, name, sex, age, address, country, number,email ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"

            # Open Connection with the Database
            with self.OpenConn() as conn:
                cursor = conn.cursor()
                cursor.execute(cmd_insert_values, tuple_data)
                cursor.close()
                conn.commit()

        print("Created Patient table")

    def tbl_shift(self, table_shift):
        self.table_shift = table_shift

        # Make our table IDEMPOTENCE by truncating it

        command_to_truncate = f"TRUNCATE TABLE {self.database}.{self.table_shift}"
        with self.OpenConn() as conn:
            cursor = conn.cursor()
            cursor.execute(command_to_truncate)
            cursor.close()
            conn.commit()

            shift = ['Morning', 'Evening', 'Dawn']
            shifts = zip(self.id_shift, shift)

        for id_each_shift, shift_name in shifts:

            # Prepare Data to INSERT
            tuple_data = (id_each_shift, shift_name)
            cmd_to_print = f"INSERT INTO {self.database}.{ self.table_shift} (id_shift, shift_name) VALUES ( {id_each_shift}, '{shift_name}')"
            cmd_insert_values = f"INSERT INTO {self.database}.{ self.table_shift} (id_shift, shift_name ) VALUES ( %s, %s )"

            # print(cmd_to_print)
            # Open Connection with the Database
            with self.OpenConn() as conn:
                cursor = conn.cursor()
                cursor.execute(cmd_insert_values, tuple_data)
                cursor.close()
                conn.commit()

        print("Created Shift table")


class Pharmacy():

    def __init__(self, user: str, password: str, host: str, database: str) -> None:

        # Hold Credentials for the Database
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    @contextmanager
    def open_conn_postgres(self):

        conn_string = f"host={self.host} user={self.user} password={self.password} dbname={self.database}"
        conn = psycopg2.connect(conn_string)
        try:
            yield conn
        finally:
            conn.close()

    def tbl_medicines(self,  table_schema: str, table_medicine: str):
        self.table_schema = table_schema
        self.table_medicine = table_medicine

        # Prepare to insert the MEDICINE into Postgres database
        with self.open_conn_postgres() as conn:
            with conn.cursor() as cursor:
                counter = 0
                for _ in api_medicines.medicines:
                    medicine = api_medicines.medicines[counter][0]
                    brand_name = medicine.get("brand_name")
                    generic_name = medicine.get("generic_name")
                    manufacturer_name = medicine.get("manufacturer_name")
                    product_ndc = medicine.get("product_ndc")
                    product_type = medicine.get("product_type")
                    route = medicine.get("route")
                    substance_name = medicine.get("substance_name")
                    record_to_insert = (brand_name, generic_name, manufacturer_name,
                                        product_ndc, product_type, route, substance_name)
                    counter += 1
                    postgres_insert_query = f""" INSERT INTO {self.table_schema}.{self.table_medicine} ("brand_name", "generic_name", "manufacturer_name", "product_ndc", "product_type", "route", "substance_name") VALUES (%s,%s,%s,%s,%s,%s,%s)"""

                    cursor.execute(postgres_insert_query, record_to_insert)
                    conn.commit()

                print("Created table Medicine")


if '__main__' == __name__:
    print(os.getcwd())
