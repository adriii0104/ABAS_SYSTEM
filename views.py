try:
    from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QListView, QListWidgetItem, \
        QPushButton, QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QFormLayout, \
        QTableWidgetItem
    from PyQt6.QtGui import QIcon, QPainter, QFont, QMovie
    from PyQt6 import uic, QtCore, QtGui
    from PyQt6.QtCore import Qt, QTimer, QDateTime, QSize
    import sys
    from SRC.settings import *
    from SRC.data import Add_inventory
    from datetime import datetime
except Exception as e:
    pass


class Main(QMainWindow):
    def __init__(self):
        self.home = None
        self.login = None
        try:
            super().__init__()
            uic.loadUi("UI/mainwindow.ui", self)
            self.setWindowTitle(APP_REQUERIMENTS[1])
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            QTimer.singleShot(2222, self.open_windows)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

    def open_windows(self):
        try:
            check = check_log()
            if not check:
                self.close()
                self.login = Login()
                self.login.show()
            else:
                self.close()
                self.home = Home()
                self.home.show()
        except Exception as e:
            print(e)


class Login(QMainWindow):
    def __init__(self):
        self.open_window = None
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/login.ui", self)
            self.setFixedSize(QSize(width, height))
            self.setWindowTitle(APP_REQUERIMENTS[1])
            self.version.setText(APP_REQUERIMENTS[0])
            self.Togglepassword.clicked.connect(self.toggle_echo_mode)
            self.Loginbutton.clicked.connect(self.login)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

    def login(self):
        try:
            user = self.inputuser.text()
            password = self.passwordinput.text()
            if user == "admin":
                if password == "1234":
                    proccess_log(enterprise_name="Grupo ramos SRL", logued=True, id=1, facturation=1)
                    self.close()
                    if self.open_window is None:
                        self.open_window = Home()
                    self.open_window.show()
                else:
                    QMessageBox.critical(self, "Error", "Las credenciales son invalidas.")
            else:
                QMessageBox.critical(self, "Error", "Las credenciales son invalidas.")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

    def toggle_echo_mode(self):
        current_echo_mode = self.password.echoMode()

        if current_echo_mode == QLineEdit.EchoMode.Password:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)

class Facturation(QMainWindow):
    def __init__(self):
        try:
            # Aqui se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/facturation.ui", self)
            self.setFixedSize(QSize(int(1400), int(ph)))
            self.setWindowTitle(APP_REQUERIMENTS[1])
            self.times = datetime.now().strftime("%H:%M:%S")
            self.timering.setText(self.times)
            self.date.setText(datetime.now().strftime("%d/%m/%Y"))
            self.fecha.setText(datetime.now().strftime("%d/%m/%Y"))
            self.timee = QTimer(self)
            self.timee.timeout.connect(self.timere)
            self.timee.start(1000)
            self.name_enterprise.setText(USER_SESSION["enterprise_name"])
            self.add.clicked.connect(self.Add_Item)
            self.clearr.clicked.connect(self.clearing)

            self.information_1.clicked.connect(lambda: self.open_information(APP_INFORMATIONS["info1"]))
            self.information_2.clicked.connect(lambda: self.open_information(APP_INFORMATIONS["info2"]))

        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

    def clearing(self):
        # Obtén el número total de filas en el QTableWidget
        num_filas = self.tableWidget_2.rowCount()

        # Elimina cada fila una por una, comenzando desde la última fila y retrocediendo
        for i in range(num_filas - 1, -1, -1):
            self.tableWidget_2.removeRow(i)

    def Add_Item(self):
        next_row = self.tableWidget_2.rowCount()
        Quantity = self.quantity.value()

        producto_item1 = QTableWidgetItem(f"Producto1")
        producto_item2 = QTableWidgetItem(f"{next_row + 1}")
        producto_item3 = QTableWidgetItem(str(Quantity))
        producto_item4 = QTableWidgetItem(f"Producto4")
        producto_item5 = QTableWidgetItem(f"Producto5")
        producto_item6 = QTableWidgetItem(f"Producto6")
        producto_item7 = QTableWidgetItem(f"Producto7")
        producto_item8 = QTableWidgetItem(f"Producto8")
        producto_item9 = QTableWidgetItem(f"Producto9")


        self.tableWidget_2.insertRow(next_row)  # Insertar una nueva fila
        self.tableWidget_2.setItem(next_row, 0, producto_item1)
        self.tableWidget_2.setItem(next_row, 1, producto_item2)
        self.tableWidget_2.setItem(next_row, 2, producto_item3)
        self.tableWidget_2.setItem(next_row, 3, producto_item4)
        self.tableWidget_2.setItem(next_row, 4, producto_item5)
        self.tableWidget_2.setItem(next_row, 5, producto_item6)
        self.tableWidget_2.setItem(next_row, 6, producto_item7)
        self.tableWidget_2.setItem(next_row, 7, producto_item8)

        self.quantity.setValue(0)


    def open_information(self, message):
        QMessageBox.information(self, "Información", message)

    def timere(self):
        try:
            self.times = datetime.now().strftime("%H:%M:%S")
            self.timering.setText(self.times)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))
class registerassets(QMainWindow):
    def __init__(self):
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/registerassets.ui", self)
            self.setFixedSize(QSize(780, 640))
            self.setWindowTitle("Registrar activo")
            self.cancelbutton.clicked.connect(self.close_assets)

        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

    def close_assets(self):
        self.close()


class Module_products_un(QMainWindow):
    def __init__(self):
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/modulo_producto_unidad.ui", self)

            self.setFixedSize(QSize(860, 780))
            self.setWindowTitle("Inventario")
            self.add_button.clicked.connect(self.add_data)

        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))


    def add_data(self):
        Quantity = self.quantity.value()
        article = self.name_art.text()
        Add_inventory(quantity=Quantity, name_art=article)
        self.quantity.setValue(0)
        self.name_art.setText("")





    def close_assets(self):
        self.close()

    def minimized_assets(self):
        self.showMinimized()



class Home(QMainWindow):
    def __init__(self):
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/home.ui", self)
            self.setFixedSize(QSize(width, height))
            self.setWindowTitle("Inicio")
            self.facturationbutton.clicked.connect(self.open_facturation)
            self.inventorybutton.clicked.connect(self.open_inventory)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))
    def close_assets(self):
        self.close()
    def open_facturation(self):
        self.facturation_window = Facturation()
        self.facturation_window.move(225, 40)
        self.facturation_window.show()

    def open_inventory(self):
        self.inventory_window = Module_products_un()
        self.inventory_window.move(225, 40)
        self.inventory_window.show()
