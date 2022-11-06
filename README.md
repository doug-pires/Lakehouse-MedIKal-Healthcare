# Lakehouse MedIKal Care 

The main goal of this portfolio is to demo how to create a **Lakehouse** using Azure services. This new architecture and data storage paradigm combines the characteristics of both data warehouses and data lakes to create a **UNIFIED** basis for **all types of use cases** to be built on top of it.
**Delta protocol** is the key ingredient that will offer features that span all fours system, DW, DL, Streaming, and Machine Learning. We need to build our lakehouses upon four pillars, reliability, performance, governance, and quality; [Delta](https://delta.io/) is the perfect match for this use case.

---
# Meet the Company
![MedIKal_Care-removebg-preview](https://user-images.githubusercontent.com/62630272/198887790-cfe556eb-0d99-4981-98dd-cde69a50debc.png)

MedIKal Care Healthcare is a private hospital that attends to a variety of patients from different countries, including Portugal, Germany, Brazil, Italy,French, USA, Mexico, and the United Kingdom. They have a large structure concerning, doctors, specialties at different shifts and distribution of medicines in their pharmacies.
# Demands from the Company
The CEO aligned with the Head of IT would like to democratize access to the data for different personas once they have the correct privileges they can consume it.

### Their demands were :
- Build a Lakehouse because down the road, they want to have BI applications, AI, and ML use cases. By doing this we can elaborate an **SSOT** ( Single Source of Truth ) to be used on the future.
> All the data, they have nowadays is stored on two different servers/databases hosted on **Azure**.
- MySQL database
- Postgres database
> Both databases have a common name, called *ikhospital* and they said, all tables within this one, could be used to get insights.
- A third data provider is about to be implemented, a streaming device in each pharmacy, which sends stream data regarding the distribution of medicines for their patients. They asked to integrate the streaming data on the data lake.
- Usage of Power BI to create reports/dashboards. Besides the Lakehouse, they would like to have a Global View of the hospital on the Power BI dashboard.
- They use Azure as a cloud provider and they wanna keep it as it is.

---
# Blueprint of the Architecture
![Architecture MedIKal](https://user-images.githubusercontent.com/62630272/199869379-da7d82d9-840b-44e5-8560-ceb2560a2a4a.png)

--- 
# Data Providers
 The data was generated by me using Python. A glimpse about it:
 - Libraries used, mentioned on the *requeriments.txt* file.
 - I used Classes to create the `Class Hospital` and `Class Pharmacy`, inside the classes, I added the fake tables.
   - Classes were good to keep interchangeable between database on Azure and Local ( Running on Docker Containers ).
   - I used one API from [FDA](https://www.fda.gov/) mentioned below.

> The Food and Drug Administration is responsible for protecting public health by ensuring the safety, efficacy,
and security of human and veterinary drugs, biological products, and medical devices; and by ensuring the safety of our nation's food supply, cosmetics, and products that emit radiation.
- The Databases, Tables, and fields were generated using SQL commands, it was not generated by the Python Code.
  - Included on this repo. 
- All the **Business Logic** I built, e.g:
  - In general only Female older than 14 can be attended by a Gynecologist.
  - Only Male guys can be attended by a Urologist.
  - Childs could be attended by a General Doctor or a Pediatrician.
    - ![image](https://user-images.githubusercontent.com/62630272/199871085-bdf454f8-c9fe-4e6b-9dd9-8aafac83bd95.png)
  - The Symptoms for each area may vary, Oncologist is responsible for Cancer not for Rhinitis.
    - ![image](https://user-images.githubusercontent.com/62630272/199871006-7a92a7c4-f662-4f44-80e7-906da55ceac6.png)

  - Everything is available on the CSV files that I imported as an example.
 - The Tables are:
   - **Medicine**, contains the medicines coming from the [FDA](https://www.fda.gov/) API.
   - **Events**, register the events on the hospital.
   - **Doctors** is a table containing all the doctors who work at MedIKal Care.
   - **Shift**, the shift that the employees work.
   - **Patient**, caontains all registered patients.
  - Streaming Device:
    - Sending data regarding the distribution of medicines to the patients.
    > Example how the tables were generated:
    ![1 Generating data](https://user-images.githubusercontent.com/62630272/200128578-992df34f-888d-4d2d-9002-7d0c1e7f9231.gif)
 
 ### All code mentioned above is on the repository.
 
 ---
# Depicting the Architecture on Azure from Left to the Right.
## Data Ingestion
### Eventhub Namespace / Topic Eventhub
 - I used to ingest and use as an Input to Azure Stream Analytics.
 - Azure Eventhub namespace has the abilty to send the raw data to Storage Account, one feature called **CAPTURE**, so we send the data generated by the streaming device to the **bronze** layer as well.
### Copy Data Activity
 - Once the IT manager said to us, they used a common name to the database called *ikhospital* then I create the code to get all the tables from the databases and push to the ADLS Gen2.
  - I used three parameters, *datasource_mysql*, *datasource_postgres* and *database* and these parameters I used to create the **Structure on Bronze container**. More about the structure on the next session, Storage Account.
  - ![image](https://user-images.githubusercontent.com/62630272/200131620-a35fb615-bb6d-46d5-96a3-1f93af365a94.png)

## Storage Account Gen2
 - The Storage Account is the Object Storage which we use to create our **Lakehouse**
 - I created three **containers**, bronze, silver and gold.
  - - ![image](https://user-images.githubusercontent.com/62630272/200132993-f93adcb4-9aa5-41db-96f5-ed716271777d.png)
 - Bronze container, we are going to land our data coming from the datasources, following the structure like that:
   - *container/datasource/databaseORschema/tables* becoming that *bronze/mysql/ikhospital/tables*
    - ![image](https://user-images.githubusercontent.com/62630272/200131332-23929a82-ea87-4182-a043-3a4783610360.png)
 - Silver and Gold containers, I made an different approach, following the structure like that: 
  - *container/databaseORschema/tables* becoming that *silverORgold/ikhospital/tables*
    - ![image](https://user-images.githubusercontent.com/62630272/200131370-52e381ec-650b-4bf9-9ba5-b49561c614db.png)
 > Keep in mind, we could create other options to structure the path inside the containers, adding partitions by YEAR,MONTH and DAY but for the sake of simplicity I utilized the general way. 

## Process Batch
- For all the processing batches I used **Spark Pool** with small size (4 vCores / 32 GB) and 3 nodes to make the minimum transformations. Then sink to the respective containers. The Synapse Notebooks, mostly part of the language was Pyspark and SQL.
- I created a CONFIGURATION notebook with the purpose to define my bases paths, datasources, and create the paths to bronze, silver and gold layer.
  - ![image](https://user-images.githubusercontent.com/62630272/200132110-986c4c54-53e4-4c3d-a300-4723f7f8e2fb.png)
- I created one notebook with Functions to list tables on ADLS, read and save to my Datalake.
  - ![image](https://user-images.githubusercontent.com/62630272/200132237-5b3fb40e-1097-47cc-8881-a5ecd660bbb9.png)
- Finally, we can chain the tasks, ingestion and curation in one single pipeline.
 - ![image](https://user-images.githubusercontent.com/62630272/200135367-9d54d9e3-cd59-4955-b142-d34233bc81b0.png)
### I won't go into many details because all of the code is on this repo.

## Process Streaming
- Azure Stream Analytics to process and send the data to a Power BI dataset. The demand was to get the distributed medicines on the current day, so the query needs to sum the number of medicines, grouped by NDC and day. The query made was that:
![image](https://user-images.githubusercontent.com/62630272/200185483-aa53ea1e-71a1-403c-97a9-3a3db45f25b8.png)


## Serve Layer
- The serving layer, the option was SQL Serverless Pool. We can create EXTERNAL TABLES or VIEWS on top of our data on the ADLS Gen2. To serve the data to Power BI, I created the database called *IKHOSPITAL_DW* then we can generate our table on that one.
- To create the tables, we can use the UI of Synapse, navigate to ADLS Gen2, choose the table, right-click, and CREATE EXTERNAL TABLE. 
- Second I created one Script to be more specific on the name of the EXTERNAL PROVIDERS, DATA SOURCES, and SCOPED CREDENTIAL, which you can use SAS, ACCESS KEYS, or MANAGED IDENTITY.
 - ![image](https://user-images.githubusercontent.com/62630272/200133289-341e05d1-2ce9-4f93-b145-9e109a967ab6.png)
- To the Power BI Developer read the tables is necessary an user. Then I created one user called *PBI_Reader*, I gave the right credentials, GRANTS to SELECthe DATABASE *IKHOSPITAL_DW* and the user can get/query the tables on Power BI.
  - ![image](https://user-images.githubusercontent.com/62630272/200133565-635a55d6-a30a-4cee-a7fc-4c8dc2aed1b2.png)

## Analytics Layer
- Having the user created, we can import our tables to Power BI and start create ANALYTICS on top of that tables.
  - ![image](https://user-images.githubusercontent.com/62630272/200133683-ebd5c75c-f82d-49b4-a427-9badb1c3e53b.png)
- We can use SQL Authentication OR AAD authentication.
> Keep in mind, the tables are small that's why we choose *import mode*, however if we are discussing a large dataset, always a good idea thinking about other methods, like *Direct Query* with *Incremental refreshs*, since our data is stored as **Delta tables**
### Power BI Desktop
- I built one simple report, telling the Overview of the Hospital, we can go further and do other measures.
![image](https://user-images.githubusercontent.com/62630272/200185590-cf483999-be5f-4c4c-92b5-58f18bece294.png)
### Power BI Service
- It's time to publish the report and put together the streaming dataset.
![image](https://user-images.githubusercontent.com/62630272/200185832-cd268c95-1c83-4f71-9d33-0e965b4cf30d.png)
![FinalDash](https://user-images.githubusercontent.com/62630272/200186415-7a5d4d9d-6f7d-4ac3-baec-ed7e97949f4d.gif)

> Only for demo purposes, the dashboard is not SO fancy, is a mess I would say, but as you can notice, we can put together data coming from **streaming** and **batch**. The streaming Raw Data is being consolidated together with the raw data with the **batch**, at the same **bronze** container.


 
