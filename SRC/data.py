import requests

url = "http://127.0.0.1:5000/apirequest_data_abas_system"

def Add_inventory(**kwargs):
    print(kwargs["article"])
    print(kwargs["code"])
    print(kwargs["unit_price"])
    print(kwargs["brand"])
    print(kwargs["active"])
    print(kwargs["itbis"])
    print(kwargs["description"])
    print(kwargs["date_expired"])
    print(kwargs["category"])



    dic = {
        "data":{"quantity": kwargs["quantity"],
            "Name": kwargs["article"],
            "Price": kwargs["unit_price"],
            "Quantity": kwargs["quantity"],
            "Avaliable": kwargs["active"],
            "Itbis 18%": kwargs["itbis"],
            "Description": kwargs["description"],
            "Expiration_date": kwargs["date_expired"],
            "Category": kwargs["category"],
            "Enterprise_sell": kwargs["brand"]

        },
        "inventory_id": kwargs["code"],
        "enterprise_id": "0001"

         }
    response = requests.post(url, json=dic, verify=False)

