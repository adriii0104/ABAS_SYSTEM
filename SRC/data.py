

url = "http://127.0.0.1:5000/apirequest_data_abas_system"

def Add_inventory(**kwargs):
    print(kwargs["quantity"])
    print(kwargs["name_art"])


#response = requests.post(url, json=data, verify=False)