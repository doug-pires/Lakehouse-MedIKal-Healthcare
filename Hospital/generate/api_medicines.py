"""

The Food and Drug Administration is responsible for protecting the public health by ensuring the safety, efficacy,
and security of human and veterinary drugs, biological products, and medical devices; and by ensuring the safety of our nation's food supply, cosmetics, and products that emit radiation.

"""


import requests
import json

# https://open.fda.gov/apis/drug/label/how-to-use-the-endpoint/

qty_medicines = 10
params = {"limit": str(qty_medicines)}
r = requests.get("https://api.fda.gov/drug/label.json", params=params)

# print(dir(r))

# print(r.text)

# number_of_medicines = int(params.get('limit'))
medicines = []
only_ndc = []
for i in range(0, qty_medicines):

    # Loads to PYTHON
    drugs = json.loads(r.text)

    try:
        drug = drugs["results"][i]["openfda"]

        if bool(drug):

            fields_to_use = ["brand_name", "generic_name", "manufacturer_name",
                             "product_ndc", "product_type", "route", "substance_name"]

            t = {k: drug[k][0] for k in drug}
            t2 = {key: value for key, value in t.items() if key in fields_to_use}
            medicines.append([t2])

        # Get Product NDC to send events

    except:
        pass

product_ndc = [p[0]['product_ndc'] for p in medicines]

if __name__ == '__main__':
    print(medicines)
    # product_ndc = [p[0]['product_ndc'] for p in medicines]
    # print(brand_name)
