import requests


def add_newsupplier(**kwargs):
    dic = {
        "newsupplier":{
            "Name": kwargs["name"],
            "Rnc": kwargs["rnc"],
            "Type": kwargs["type"],
            "Direction": kwargs["direction"],
            "Phone": kwargs["phone"],
            "Email": kwargs["email"],
            "Website": kwargs["website"],
        },
        "supplier_id": kwargs["code"],
        "enterprise_id": "0001"

         }

    for letra, valor in dic.items():
        print(valor)



