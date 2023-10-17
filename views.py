try:
    from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QListView, QListWidgetItem, \
        QPushButton, QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QFormLayout, \
        QTableWidgetItem, QInputDialog
    from PyQt6.QtGui import QIcon, QPainter, QFont, QMovie
    from PyQt6 import uic, QtCore, QtGui
    from PyQt6.QtCore import Qt, QTimer, QDateTime, QSize, QDateTime, QDate
    import sys
    from SRC.settings import *
    from SRC.data import *
    import re
    from datetime import datetime
    import json
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
                self.home.move(0, 0)
                self.home.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", "Ha ocurrido un error inesperado" + str(e))


class Login(QMainWindow):
    def __init__(self):
        self.open_window = None
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/login.ui", self)
            self.setFixedSize(QSize(600, 510))
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
            passwd = self.passwordinput.text()

            password = hash_pass(pass_auth_user_get_input=passwd)
            response = data_user_send_post_log(user_log_data_send_input=user, pass_log_data_send_input=password)
            if response:
                self.close()
                if self.open_window is None:
                    self.open_window = Home()
                self.open_window.show()
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
            self.setFixedSize(QSize(1290, 825))
            self.setWindowTitle(APP_REQUERIMENTS[1])
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.times = datetime.now().strftime("%H:%M:%S")
            self.timering.setText(self.times)
            # self.date.setText(datetime.now().strftime("%d/%m/%Y"))
            self.fecha.setText(datetime.now().strftime("%d/%m/%Y"))
            self.timee = QTimer(self)
            self.timee.timeout.connect(self.timere)
            self.timee.start(1000)
            self.name_enterprise.setText(USER_SESSION["COMPANY_NAME"])
            self.add.clicked.connect(self.Add_Item)
            self.clearr.clicked.connect(self.clearing)
            self.status.clicked.connect(self.connected)
            self.searchbutton.clicked.connect(self.search)
            self.closebutton.clicked.connect(self.close_facturation)
            self.minimizedbutton.clicked.connect(self.minimized_facturation)  

            self.information_1.clicked.connect(lambda: self.open_information(APP_INFORMATIONS["info1"]))
            self.information_2.clicked.connect(lambda: self.open_information(APP_INFORMATIONS["info2"]))

            session_ac = check_session()
            if "LOGUED" not in USER_SESSION and session_ac is False:
                self.status.setText("Desconectado")
                icon = QIcon('IMGS/34.png')
                self.status.setIcon(icon)
                self.status.setIconSize(QSize(12, 12))

            else:
                self.status.setText("Conectado")
                icon = QIcon('IMGS/35.png')
                self.status.setIcon(icon)
                self.status.setIconSize(QSize(12, 12))
        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

    def search(self):
        session_ac = check_session()
        if "LOGUED" in USER_SESSION and session_ac:
            id = self.id.text()
            data = search_product(id_product=id)
            if data:
                self.productname.setText(data["Name"])
                self.productID.setText(id)
                self.available.setText(str(data["Quantity"]))
                self.cd.setText(data["Expiration_date"])
                self.price.setText(data["Price"])
            else:
                QMessageBox.information(self, "Error", "El producto no se ha encontrado.")
        else:
            QMessageBox.information(self, "Error", "Para completar esta actividad debe entrar en el servidor.")
            self.close()
            LAST_WINDOW["last"] = "Facturation"
            self.altern = Alter_log()
            self.altern.show()

    def close_facturation(self):
        self.close()
    def minimized_facturation(self):
        self.showMinimized()


    def connected(self):
        session_ac = check_session()
        if "LOGUED" in USER_SESSION and session_ac:
            QMessageBox.information(self, "Conectado", "Este dispositivo está conectado al servidor y se puede realizar cualquier actividad.")
        else:
            self.close()
            LAST_WINDOW["last"] = "Facturation"
            self.altern = Alter_log()
            self.altern.show()


    def clearing(self):
        # Obtén el número total de filas en el QTableWidget
        num_filas = self.tableWidget_2.rowCount()

        # Elimina cada fila una por una, comenzando desde la última fila y retrocediendo
        for i in range(num_filas - 1, -1, -1):
            self.tableWidget_2.removeRow(i)

    def Add_Item(self):

        next_row = self.tableWidget_2.rowCount()
        Quantity = self.quantity.value()
        product = self.productname.text()
        ID_PRODUCT = self.productID.text()
        PRICE = self.price.text()
        self.available.text()
        INPUTS = [product, ID_PRODUCT, PRICE]

        trying = True
        exists = False

        for input in INPUTS:
            if input.isspace() or input == "":
                QMessageBox.critical(self, "Error", "Primero debes agregar el Articulo.")
                trying = False
                break

        if trying is True:
            if Quantity > int(self.available.text()):
                QMessageBox.information(self, "Error", "Solo quedan {} disponibles.".format(self.available.text()))
            elif Quantity == 0:
                QMessageBox.information(self, "Error", "Debes agregar la cantidad.")
            else:
                table = self.tableWidget_2  # Reemplaza con la referencia correcta a tu QTableWidget
                for row in range(table.rowCount()):
                    for column in range(table.columnCount()):
                        item = table.item(row, column)
                        if item is not None:
                            value = item.text()
                            if value == ID_PRODUCT:
                                exists = True
                                quantity = self.tableWidget_2.item(int(row), 2).text()
                                quantity = self.tableWidget_2.item(int(row), 2).text()
                                quantity = self.tableWidget_2.item(int(row), 2).text()
                                quantity = self.tableWidget_2.item(int(row), 2).text()

                                totalquantity = int(quantity) + Quantity

                                qnt = QTableWidgetItem(str(totalquantity))



                                self.tableWidget_2.setItem(row, 2, qnt)
                                self.clear_windows_inputs()

                        else:
                            pass
                if exists is False:
                    self.cd.text()
                    ITBIS = int(Quantity) * float(PRICE) * 0.18
                    TOTAL = int(Quantity) * float(PRICE) + ITBIS
                    TOTAL_WITHOUT_ITBIS = int(Quantity) * float(PRICE)

                    ITBIS_FRMT = "{:,.2f}".format(ITBIS)
                    SUB_TOTAL_FRMT = "{:,.2f}".format(TOTAL_WITHOUT_ITBIS)
                    TOTAL_FRMT = "{:,.2f}".format(TOTAL)

                    producto_item1 = QTableWidgetItem(product)
                    producto_item2 = QTableWidgetItem(ID_PRODUCT)
                    producto_item3 = QTableWidgetItem(str(Quantity))
                    producto_item4 = QTableWidgetItem(str(PRICE))
                    producto_item5 = QTableWidgetItem(f"0.00")
                    producto_item6 = QTableWidgetItem(SUB_TOTAL_FRMT)
                    producto_item7 = QTableWidgetItem(ITBIS_FRMT)
                    producto_item8 = QTableWidgetItem(TOTAL_FRMT)

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

                    # PROCESAR Y CALCULAR

                    # FUNCION DEL SUBTOTAL.
                    SUB = self.tableWidget_2.item(next_row, 5).text()
                    PP = re.sub(r'\.\d+', '', SUB)
                    PP = PP.replace(",", "")

                    to_sum = int(PP)

                    sum_text = self.subtotal_input.text()
                    print(sum_text)
                    sum_number = int(re.sub(r'\.\d+', '', sum_text).replace(",", ""))

                    total_sub = to_sum + sum_number
                    SUB = format(total_sub)

                    self.subtotal_input.setText(SUB)


                    # FUNCION PARA EL DESCUENTO.
                    DESC = self.tableWidget_2.item(next_row, 4).text()
                    DESC = re.sub(r'\.\d+', '', DESC)
                    DESC = DESC.replace(",", "")

                    DESC_TO_SUM = int(DESC)

                    DESC_SUM = float(self.discount.text())

                    TOTAL_DESC = DESC_TO_SUM + DESC_SUM
                    DESC_FORMAT = format(TOTAL_DESC)

                    self.discount.setText(DESC_FORMAT)

                    self.clear_windows_inputs()


    def open_information(self, message):
        QMessageBox.information(self, "Información", message)

    def timere(self):
        try:
            self.times = datetime.now().strftime("%H:%M:%S")
            self.timering.setText(self.times)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

    
class registersuppliers(QMainWindow):
    def __init__(self):
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/registersuppliers.ui", self)
            self.setFixedSize(QSize(540, 490))
            self.setWindowTitle("Registrar aproveedor")
            self.codeinput.setText(next(self.sequencecode()))
            self.codeinput.setReadOnly(True)
            self.cancelbutton.clicked.connect(self.close_assets)
            self.savebutton.clicked.connect(self.add_supplier)

        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

    def sequencecode(self):
        for number in range(1, 1001):
            yield f"P{number:04}"

    def close_assets(self):
        self.close()

    def add_supplier(self):
        Code = self.codeinput.text()
        Name = self.nameinput.text()
        Rnc = self.rncinput.text()
        Type = self.typebox.currentText()
        Direction = self.directioninput.text()
        Phone = self.phoneinput.text()
        Email = self.emailinput.text()
        Website = self.websiteinput.text()

        add_newsupplier(code=Code, name=Name, rnc=Rnc, type=Type, direction=Direction, 
                        phone=Phone, email=Email, website=Website)


        self.nameinput.setText("")
        self.rncinput.setText("")
        self.typebox.itemText(1)
        self.directioninput.setText("")
        self.phoneinput.setText("")
        self.emailinput.setText("")
        self.websiteinput.setText("")







class Module_products_un(QMainWindow):
    def __init__(self):
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/modulo_producto_unidad.ui", self)
            self.setFixedSize(QSize(870, 1200))
            self.setWindowTitle("Inventario")
            date = QDate.currentDate()
            self.date_expired.setDate(date)
            self.date_buy.setText(datetime.now().strftime("%d/%m/%Y"))
            self.add_button.clicked.connect(self.add_data)                

        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))


    def searchsupplier(self):
        pass


    def add_data(self):
        tryded = True
        for qline in self.findChildren(QLineEdit):
            if qline.text().isspace() or qline.text() == "":
                QMessageBox.critical(
                    self, "Error", "Hay uno o más elementos vacíos.")
                tryded = False
                break
        if self.quantity.value() == 0:
                QMessageBox.critical(
                    self, "Error", "La cantidad debe ser mayor a 0.")
                tryded = False
        if self.category.currentText() == "Selecciona":
            QMessageBox.critical(self, "Error", "Debes seleccionar la categoría.")
            tryded = False
        if tryded:
            date = QDate.currentDate()
            Article = self.article.text()
            Unit_price = self.unit_price.text()
            Quantity = self.quantity.value()
            Avaliable = self.active.isChecked()
            Itbis = self.itbis.isChecked()
            Description = self.description.text()
            Date_expired = self.date_expired.text()
            Category = self.category.currentText()
            Brand = self.brand.text()
            Code = self.code.text()
            Add_inventory(quantity=Quantity, article=Article, code=Code, unit_price=Unit_price, 
                          active=Avaliable, itbis=Itbis, description=Description, 
                          date_expired=Date_expired, category=Category, brand=Brand)
            self.article.setText("")
            self.unit_price.setText("")
            self.quantity.setValue(0)
            self.code.setText("")
            self.active.setChecked(False)
            self.itbis.setChecked(False)
            self.description.setText("")
            self.date_expired.setDate(date)
            self.category.itemText(1)
            self.brand.setText("")




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
            self.menubar.setFixedSize(QSize(151, int(ph)))
            self.setFixedSize(QSize(width, int(ph)))
            self.setWindowTitle("Inicio")
            self.facturationbutton.clicked.connect(self.open_facturation)
            self.inventorybutton.clicked.connect(self.open_inventory)
            self.suppliersbutton.clicked.connect(self.open_suppliers)

            self.facturation = Facturation()
        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))
    

    def open_facturation(self):
        self.facturation_window = Facturation()
        self.facturation_window.move(152, 32)
        self.facturation_window.show()

    def open_inventory(self):
        if "LOGUED" in USER_SESSION:
            self.inventory_window = Module_products_un()
            self.inventory_window.move(155, 35)
            self.inventory_window.show()
        else:
            LAST_WINDOW["last"] = "Inventory"
            self.altern = Alter_log()
            self.altern.show()
    
    def open_suppliers(self):
        self.suppliers_window = registersuppliers()
        self.suppliers_window.move(155, 35)
        self.suppliers_window.show()


class Alter_log(QMainWindow):
    def __init__(self):
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/altern_log.ui", self)
            self.setWindowTitle("Please Log")
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.closer.clicked.connect(self.closedd)
            self.log.clicked.connect(self.login)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))
    def closedd(self):
        self.close()

    def login(self):
        passwd = self.input_password.text()
        password = hash_pass(pass_auth_user_get_input=passwd)

        with open("JSON/temporary.json", "r", encoding="utf-8") as check:
            checked = json.load(check)
            user = checked["user_information"]["user"]

        
        if self.setlogin.isChecked():
            with open("JSON/temporary.json", "r", encoding="utf-8") as to_read:
                check_information = json.load(to_read)

                check_information["user_information"]["active"] = True

            with open("JSON/temporary.json", "w", encoding="utf-8") as to_write:
                json.dump(checked, to_write, indent=4)
                
            
        response = data_user_send_post_log(user_log_data_send_input=user, pass_log_data_send_input=password)
        if response:
            self.close()
            if LAST_WINDOW["last"] == "Facturation":
                self.last = Facturation()
                self.last.show()
            elif LAST_WINDOW["last"] == "Inventory":
                self.last = Module_products_un()
                self.last.show()
        else:
            QMessageBox.information(self, "Error", "Credenciales invalidas.")
