# Lakehouse MedIKal Care 

The main goal of this portfolio is to demo how to create a Lakehouse using Azure services. This new architecture and data storage paradigm combines the characteristics of both data warehouses and data lakes to create a UNIFIED basis for all types of use cases to be built on top of it. **Delta protocol** is the key ingredient that will offer features that span all fours system, DW, DL, Streaming, and Machine Learning. We need to build our lakehouses upon four pillars, reliability, performance, governance, and quality; [Delta](https://delta.io/) is the perfect match for this use case.
---
# Meet the Company
![MedIKal_Care-removebg-preview](https://user-images.githubusercontent.com/62630272/198887790-cfe556eb-0d99-4981-98dd-cde69a50debc.png)

MedIKal Care Healthcare is a private hospital that attends to a variety of patients from different countries, including Portugal, Germany, Brazil, Italy,French,USA,Mexico, and the United Kingdom. They have a large structure concerning, doctors, specialties, different shifts, distribution of medicines in their pharmacies.

# Demands from the Company
The CEO aligned with the Head of IT would like to democratize access to the data for different personas once they have the correct privileges they can consume it.

### Their demands were :
- Build a Lakehouse because down the road, they want to have BI applications, AI, and ML use cases. By doing this we can elaborate an **SSOT** ( Single Source of Truth ) to be used on the future.
> All the data, they have nowadays is stored on two different servers/databases hosted on **Azure**.
- MySQL database
- Postgres database
> Both databases have a common name, called *ikhospital* and they said, all tables within this one, could be used to get insights.
- A third data provider is about to be implemented, a streaming device in each pharmacy, which sends stream data regarding the distribution of medicines for their patients.
- Usage of Power BI to create reports/dashboards. Besides the Lakehouse, they would like to have a Global View of the hospital on the Power BI dashboard.
- They use Azure as a cloud provider and they wanna keep it as it is.

---
# Blueprint of the Architecture
