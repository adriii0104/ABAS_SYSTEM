import requests
from SRC.settings import USER_SESSION
from tkinter import messagebox

url = "http://127.0.0.1:5000/request_data_abas_system"

def Add_inventory(**kwargs):
    try:
        from SRC.settings import USER_SESSION
        dic = {
            "data": {"quantity": kwargs["quantity"],
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
            "enterprise_id": USER_SESSION["COMPANY_ID"]
             }
        response = requests.post(url, json=dic, verify=False)
        if response.status_code == 200:
            data = response.json()
            messagebox.showinfo(data["title"], data["message"])
        else:
            return False
    except requests.ConnectionError:
        messagebox.showinfo("Ha ocurrido un error inesperado.", "Para realizar esta accion debes estar conectado a internet.")

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
        "enterprise_id": USER_SESSION["COMPANY_ID"]

         }


def data_user_send_post_log(**kwargs):
    try:
        urls = 'http://127.0.0.1:5000/request_data_abas_system/log'

        data = {
            "info_user_data_get_json": kwargs["user_log_data_send_input"],
            "info_pass_data_get_json": kwargs["pass_log_data_send_input"]
        }
        response = requests.post(urls, json=data, verify=False)

        if response.status_code == 200:
            data_returned = response.json()
            if data_returned["logued"] == True:
                from SRC.settings import USER_SESSION, proccess_log

                data_log_succefull = data_returned["log_info"]

                USER_SESSION["LOGUED"] = True
                USER_SESSION["COMPANY_NAME"] = data_log_succefull["company_name"]
                USER_SESSION["COMPANY_ID"] = data_log_succefull["id_enterprise"]
                proccess_log(enterprise_name=USER_SESSION["COMPANY_NAME"], logued=True, id=USER_SESSION["COMPANY_ID"], user= data_log_succefull["user"], facturation=1)
                return True
            else:
                return False
    except requests.ConnectionError:
        messagebox.showinfo("Ha ocurrido un error inesperado.", "Para realizar esta accion debes estar conectado a internet.")

def search_product(**kwargs):
    try:
        from SRC.settings import USER_SESSION
        urls = "http://127.0.0.1:5000/request_data_abas_system/search"

        data = {"enterprise_id": USER_SESSION["COMPANY_ID"], "inventory_id": kwargs["id_product"]}

        response = requests.post(urls, json=data, verify=False)
        if response.status_code == 200:
            DATA = response.json()
            if DATA["found"]:
                return DATA["data"]
            else:
                return False
    except requests.ConnectionError:
        messagebox.showinfo("Ha ocurrido un error inesperado.", "Para realizar esta accion debes estar conectado a internet.")



def inventory():
    url = "http://127.0.0.1:5000/data_request_inventory/ABAS/USER"

    data_url = f"{url}/{USER_SESSION['COMPANY_ID']}"

    response = requests.get(data_url)

    if response.status_code == 200:
        DATA = response.json()
        if DATA["Error"] is True:
            messagebox.showinfo("Mensaje.", "Aún no hay articulosa agregados.")
            return None
        else:
            return DATA["data"]
    else:
        messagebox.showinfo("Error.", "Ha ocurrido un error.")

