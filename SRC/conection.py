import requests
from tkinter import messagebox



def check_connection():
    try:
        response = requests.get("http://127.0.0.1:5000")
        if response.status_code == 200:
            return True
        else:
            messagebox.showinfo("Ha ocurrido un error inesperado.", "Ha ocurrido un error inesperado, "
                                                                    "por favor revisa tu conexión a internet.")
            return False
    except requests.exceptions.ConnectionError:
        messagebox.showinfo("Ha ocurrido un error inesperado.", "Ha ocurrido un error inesperado, "
                                                                "por favor revisa tu conexión a internet.")
        return False
