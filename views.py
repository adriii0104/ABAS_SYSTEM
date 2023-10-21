try:
    from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QListView, QListWidgetItem, \
        QPushButton, QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QFormLayout, \
        QTableWidgetItem, QInputDialog
    from PyQt6.QtGui import QIcon, QPainter, QFont, QMovie
    from PyQt6 import uic, QtCore, QtGui
    from PyQt6.QtCore import Qt, QTimer, QDateTime, QSize, QDateTime, QDate
    from SRC.settings import *
    from SRC.data import *
    import re
    from datetime import datetime
    import json
    from SRC.json_modify import reminder_session
    from SRC.conection import check_connection
    from tkinter import messagebox
except Exception as e:

    pass


class Main(QMainWindow):
    def __init__(self):
        self.home = None
        self.login = None
        try:
            super().__init__()
            uic.loadUi("UI/mainwindow.ui", self)
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            QTimer.singleShot(2222, self.open_windows)
        except Exception as e:
            messagebox.showinfo(
                "Error", "Error al iniciar la aplicación: " + str(e))

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
            messagebox.showinfo("Ha ocurrido un error inesperado.",
                                "Ha ocurrido un error inesperado" + str(e))


class Login(QMainWindow):
    def __init__(self):
        self.open_window = None
        super().__init__()
        chk = check_connection()
        if chk:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            uic.loadUi("UI/login.ui", self)
            self.setFixedSize(QSize(600, 510))
            self.setWindowTitle(USER_SESSION["COMPANY_NAME"] + " - (Iniciar Sesión)" if "COMPANY_NAME" in USER_SESSION else "Login")
            self.version.setText(APP_REQUERIMENTS[0])
            self.Togglepassword.clicked.connect(self.toggle_echo_mode)
            self.Loginbutton.clicked.connect(self.login)

    def login(self):
        try:
            chk = check_connection()
            if chk:
                user = self.inputuser.text()
                passwd = self.passwordinput.text()

                password = hash_pass(pass_auth_user_get_input=passwd)
                response = data_user_send_post_log(
                    user_log_data_send_input=user, pass_log_data_send_input=password)
                if response:
                    self.close()
                    if self.open_window is None:
                        self.open_window = Home()
                    self.open_window.show()
                else:
                    messagebox.showinfo(
                        "Ha ocurrido un error inesperado.", "Las credenciales son invalidas.")
        except Exception as e:
            messagebox.showinfo("Ha ocurrido un error inesperado.",
                                "Ha ocurrido un error inesperado" + str(e))

    def toggle_echo_mode(self):
        current_echo_mode = self.passwordinput.echoMode()

        if current_echo_mode == QLineEdit.EchoMode.Password:
            self.passwordinput.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordinput.setEchoMode(QLineEdit.EchoMode.Password)


class Facturation(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            chk = check_connection()
            # Aqui se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            uic.loadUi("UI/facturation.ui", self)

            self.setFixedSize(QSize(1438, 859))

            self.setWindowTitle(USER_SESSION["COMPANY_NAME"] + " - (Facturación)")
            # self.date.setText(datetime.now().strftime("%d/%m/%Y"))
            self.fecha.setText(datetime.now().strftime("%d/%m/%Y"))
            self.add.clicked.connect(self.Add_Item)
            self.clearr.clicked.connect(self.clearing)
            self.status.clicked.connect(self.connected)
            self.searchbutton.clicked.connect(self.search)

            self.cnn()
            # seteamos los textos, total, subtotal, itbis y descuento en 0 por defecto.
            self.subtotal_inputt.setText("0")
            self.discount_inputt.setText("0")
            self.itbis_inputt.setText("0")
            self.total_inputt.setText("0")
        except Exception as e:
            messagebox.showinfo("Ha ocurrido un error inesperado.",
                                "Ha ocurrido un error inesperado" + str(e))

    def cnn(self):
        session_ac = check_session()
        chk = check_connection()
        if chk is False or "LOGUED" not in USER_SESSION and session_ac is False:
            self.status.setText(
                "Desconectado, presiona aquí para intentar reconectar")
            icon = QIcon('IMGS/34.png')
            self.status.setIcon(icon)
            self.status.setIconSize(QSize(12, 12))
            self.status.clicked.connect(self.cnn if chk is False else self.opening_loguer)
        else:
            self.status.setText("Conectado")
            icon = QIcon('IMGS/35.png')
            self.status.setIcon(icon)
            self.status.setIconSize(QSize(12, 12))

    def search(self):
        try:
            chk = check_connection()
            if chk:
                session_ac = check_session()
                if "LOGUED" in USER_SESSION or session_ac:
                    id = self.id.text()
                    data = search_product(id_product=id)
                    if data:
                        self.productname.setText(data["Name"])
                        self.productID.setText(id)
                        self.available.setText(str(data["Quantity"]))
                        self.cd.setText(data["Expiration_date"])
                        self.price.setText(data["Price"])
                    else:
                        messagebox.showinfo(
                            "Error.", "El producto no se ha encontrado.")
                else:
                    messagebox.showinfo(
                        "Error.", "Para completar esta actividad debe entrar en el servidor.")
                    self.opening_loguer
            else:
                self.cnn()
        except Exception:
            messagebox.showinfo("Error inesperado.",
                                "Ha ocurrido un error inesperado.")
            

    def opening_loguer(self):
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
        chk = check_connection()
        if "LOGUED" in USER_SESSION or session_ac and chk:
            messagebox.showinfo(
                "Conectado", "Este dispositivo está conectado al servidor y se puede realizar cualquier actividad.")
        else:
            pass

    def clearing(self):
        # Obtén el número total de filas en el QTableWidget
        num_filas = self.tableWidget_2.rowCount()

        # Elimina cada fila una por una, comenzando desde la última fila y retrocediendo
        for i in range(num_filas - 1, -1, -1):
            self.tableWidget_2.removeRow(i)

        self.subtotal_inputt.setText("0")
        self.discount_inputt.setText("0")
        self.itbis_inputt.setText("0")
        self.total_inputt.setText("0")

    def Add_Item(self):
        try:
            chk = check_connection()
            if chk:
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
                        messagebox.showinfo(
                            "Error", "Primero debes agregar el Articulo.")
                        trying = False
                        break

                if trying is True:
                    if Quantity > int(self.available.text()):
                        messagebox.showinfo(
                            "Error", "Solo quedan {} disponibles.".format(self.available.text()))
                    elif Quantity == 0:
                        messagebox.showinfo(
                            "Error", "Debes agregar la cantidad")
                    else:
                        table = self.tableWidget_2  # Reemplaza con la referencia correcta a tu QTableWidget
                        for row in range(table.rowCount()):
                            for column in range(table.columnCount()):
                                item = table.item(row, column)
                                if item is not None:
                                    value = item.text()
                                    if value == ID_PRODUCT:
                                        exists = True
                                        quantity = self.tableWidget_2.item(
                                            int(row), 2).text()
                                        PRICE_MD = self.tableWidget_2.item(
                                            int(row), 3).text()
                                        SUBTOTAL_MD = float(
                                            self.tableWidget_2.item(int(row), 5).text())
                                        current_itbis = float(
                                            self.tableWidget_2.item(int(row), 6).text())
                                        current_total = float(
                                            self.tableWidget_2.item(int(row), 7).text())

                                        last_price = Quantity * float(PRICE_MD)

                                        last_itbis = (
                                            int(Quantity) * float(PRICE_MD)) * 0.18

                                        total_itbis = float(
                                            last_itbis) + float(current_itbis)
                                        totalquantity = int(
                                            quantity) + Quantity

                                        last_total = last_price + current_total + last_itbis

                                        total_itbis = "{:,.2f}".format(
                                            total_itbis)

                                        last_total = "{:,.2f}".format(
                                            last_total)

                                        last_subtotal = "{:,.2f}".format(
                                            last_price)

                                        qnt = QTableWidgetItem(
                                            str(totalquantity))
                                        snt = QTableWidgetItem(
                                            str(total_itbis))
                                        pnt = QTableWidgetItem(str(last_total))
                                        rnt = QTableWidgetItem(
                                            str(last_subtotal))

                                        self.tableWidget_2.setItem(row, 2, qnt)
                                        self.tableWidget_2.setItem(row, 5, rnt)
                                        self.tableWidget_2.setItem(row, 6, snt)
                                        self.tableWidget_2.setItem(row, 7, pnt)
                                        self.clear_windows_inputs()

                                else:
                                    pass
                        if exists is False:
                            ITBIS = int(Quantity) * float(PRICE) * 0.18
                            TOTAL = int(Quantity) * float(PRICE) + ITBIS
                            TOTAL_WITHOUT_ITBIS = int(Quantity) * float(PRICE)

                            ITBIS_FRMT = "{:,.2f}".format(ITBIS)
                            SUB_TOTAL_FRMT = "{:,.2f}".format(
                                TOTAL_WITHOUT_ITBIS)
                            TOTAL_FRMT = "{:,.2f}".format(TOTAL)

                            producto_item1 = QTableWidgetItem(product)
                            producto_item2 = QTableWidgetItem(ID_PRODUCT)
                            producto_item3 = QTableWidgetItem(str(Quantity))
                            producto_item4 = QTableWidgetItem(str(PRICE))
                            producto_item5 = QTableWidgetItem(f"0.00")
                            producto_item6 = QTableWidgetItem(SUB_TOTAL_FRMT)
                            producto_item7 = QTableWidgetItem(ITBIS_FRMT)
                            producto_item8 = QTableWidgetItem(TOTAL_FRMT)

                            self.tableWidget_2.insertRow(
                                next_row)  # Insertar una nueva fila
                            self.tableWidget_2.setItem(
                                next_row, 0, producto_item1)
                            self.tableWidget_2.setItem(
                                next_row, 1, producto_item2)
                            self.tableWidget_2.setItem(
                                next_row, 2, producto_item3)
                            self.tableWidget_2.setItem(
                                next_row, 3, producto_item4)
                            self.tableWidget_2.setItem(
                                next_row, 4, producto_item5)
                            self.tableWidget_2.setItem(
                                next_row, 5, producto_item6)
                            self.tableWidget_2.setItem(
                                next_row, 6, producto_item7)
                            self.tableWidget_2.setItem(
                                next_row, 7, producto_item8)

                            self.quantity.setValue(0)

                            # PROCESAR Y CALCULAR

                            # FUNCION DEL SUBTOTAL.
                            SUB = self.tableWidget_2.item(next_row, 5).text()
                            PP = re.sub(r'\.\d+', '', SUB)
                            PP = PP.replace(",", "")

                            to_sum = int(PP)

                            sum_text = self.subtotal_inputt.text()
                            sum_number = int(
                                re.sub(r'\.\d+', '', sum_text).replace(",", ""))

                            total_sub = to_sum + sum_number
                            SUB = "{:,.2F}".format(total_sub)

                            self.subtotal_inputt.setText(SUB)

                            # FUNCION PARA EL DESCUENTO.
                            DESC = self.tableWidget_2.item(next_row, 4).text()
                            DESC = re.sub(r'\.\d+', '', DESC)
                            DESC = DESC.replace(",", "")

                            DESC_TO_SUM = int(DESC)

                            DESC_SUM = float(self.discount_inputt.text())

                            TOTAL_DESC = DESC_TO_SUM + DESC_SUM
                            DESC_FORMAT = format(TOTAL_DESC)

                            self.discount_inputt.setText(DESC_FORMAT)

                            self.clear_windows_inputs()
            else:
                self.cnn()
        except Exception as e:
            messagebox.showinfo("Ha ocurrido un error inesperado.",
                                "Ha ocurrido un error inesperado" + str(e))

    def clear_windows_inputs(self):
        self.productname.setText("")
        self.productID.setText("")
        self.available.setText("")
        self.cd.setText("")
        self.price.setText("")

    def open_information(self, message):
        QMessageBox.information(self, "Información", message)



class Suppliers(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
                # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            uic.loadUi("UI/suppliers.ui", self)
            self.setFixedSize(QSize(920, 735))
            self.setWindowTitle("Suplidores")

        except Exception as e:
            messagebox.showinfo("Ha ocurrido un error inesperado.",
                                "Ha ocurrido un error inesperado" + str(e))





class registersuppliers(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            chk = check_connection()
            if chk:
                # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
                uic.loadUi("UI/registersuppliers.ui", self)
                self.setFixedSize(QSize(540, 490))
                self.setWindowTitle("Registrar aproveedor")
                self.codeinput.setText(next(self.sequencecode()))
                self.codeinput.setReadOnly(True)
                self.cancelbutton.clicked.connect(self.close_assets)
                self.savebutton.clicked.connect(self.add_supplier)

        except Exception as e:
            messagebox.showinfo("Ha ocurrido un error inesperado.",
                                "Ha ocurrido un error inesperado" + str(e))

    def sequencecode(self):
        for number in range(1, 1001):
            yield f"F-01{number:10}"

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
            chk = check_connection()
            if chk:
                uic.loadUi("UI/modulo_producto_unidad.ui", self)
                self.setFixedSize(QSize(870, 800))
                self.setWindowTitle("Inventario")
                date = QDate.currentDate()
                self.date_expired.setDate(date)
                self.date_buy.setText(datetime.now().strftime("%d/%m/%Y"))
                self.add_button.clicked.connect(self.add_data)

        except Exception as e:
            messagebox.showinfo("Ha ocurrido un error inesperado.",
                                "Ha ocurrido un error inesperado" + str(e))

    def searchsupplier(self):
        pass

    def add_data(self):
        tryded = True
        for qline in self.findChildren(QLineEdit):
            if qline.text().isspace() or qline.text() == "":
                messagebox.showinfo(
                    "Error.", "Hay uno o mas campos de entrada vacíos.")
                tryded = False
                break
        if self.quantity.value() == 0:
            messagebox.showinfo("Error.", "La cantidad debe ser mayor de 0.")
            tryded = False
        if self.category.currentText() == "Selecciona":
            messagebox.showinfo("Error.", "Debes seleccionar la categoría.")

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
            response = Add_inventory(quantity=Quantity, article=Article, code=Code, unit_price=Unit_price,
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
            if response:
                messagebox

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
            messagebox.showinfo("Error.",
                                "Ha ocurrido un error inesperado" + str(e))

    def open_facturation(self):
        self.facturation_window = Facturation()
        self.facturation_window.move(152, 32)
        self.facturation_window.show()

    def open_inventory(self):
        session_ac = check_session()
        if "LOGUED" in USER_SESSION or session_ac:
            self.inventory_window = Inventory()
            self.inventory_window.move(155, 35)
            self.inventory_window.show()
        else:
            LAST_WINDOW["last"] = "Inventory"
            self.altern = Alter_log()
            self.altern.show()

    def open_suppliers(self):
        self.suppliers_window = Suppliers()
        self.suppliers_window.move(155, 35)
        self.suppliers_window.show()


class Alter_log(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            chk = check_connection()
            if chk:
                # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
                uic.loadUi("UI/altern_log.ui", self)
                self.setWindowTitle("Please Log")
                self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
                self.closer.clicked.connect(self.closedd)
                self.log.clicked.connect(self.login)
        except Exception as e:
            messagebox.showinfo("Error.",
                                "Ha ocurrido un error inesperado" + str(e))

    def closedd(self):
        self.close()

    def login(self):
        chk = check_connection()
        if chk:
            passwd = self.input_password.text()
            password = hash_pass(pass_auth_user_get_input=passwd)

            with open("JSON/temporary.json", "r", encoding="utf-8") as check:
                checked = json.load(check)
                user = checked["user_information"]["user"]

            response = data_user_send_post_log(
                user_log_data_send_input=user, pass_log_data_send_input=password)

            if response:
                self.close()
                if LAST_WINDOW["last"] == "Facturation":
                    self.last = Facturation()
                    self.last.show()
                elif LAST_WINDOW["last"] == "Inventory":
                    self.last = Inventory()
                    self.last.show()
                if self.setlogin.isChecked():
                    reminder_session()
            else:
                messagebox.showinfo("Error", "Credenciales invalidas.")



class Inventory(QMainWindow):
    def __init__(self):
        try:
            super().__init__()

            uic.loadUi("UI/inventory.ui", self)

            self.setFixedSize(QSize(1231, 821))

            self.setWindowTitle(USER_SESSION["COMPANY_NAME"] + " - (Inventario)")

            response = inventory()

            if response is not None:
                for index, items in response.items():
                    next_row = self.inventory.rowCount()


                    producto_item1 = QTableWidgetItem(str(index))
                    producto_item2 = QTableWidgetItem(items["Name"])
                    producto_item3 = QTableWidgetItem(items["Description"])
                    producto_item4 = QTableWidgetItem(str(items["Price"]))
                    producto_item5 = QTableWidgetItem(str(items["Quantity"]))
                    producto_item6 = QTableWidgetItem(str(items["Avaliable"]))
                    producto_item7 = QTableWidgetItem(str(items["Category"]))
                    producto_item8 = QTableWidgetItem(items["Enterprise_sell"])


                    self.inventory.setColumnWidth(0, 140)  # Ajusta el ancho de la columna 1
                    self.inventory.setColumnWidth(1, 140)  # Ajusta el ancho de la columna 1
                    self.inventory.setColumnWidth(2, 280)  # Ajusta el ancho de la columna 1
                    self.inventory.setColumnWidth(3, 70)  # Ajusta el ancho de la columna 1
                    self.inventory.setColumnWidth(4, 70)  # Ajusta el ancho de la columna 1
                    self.inventory.setColumnWidth(5, 120)  # Ajusta el ancho de la columna 1
                    self.inventory.setColumnWidth(6, 140)  # Ajusta el ancho de la columna 1
                    self.inventory.setColumnWidth(7, 140)  # Ajusta el ancho de la columna 1

                    self.inventory.insertRow(
                        next_row)  # Insertar una nueva fila
                    self.inventory.setItem(
                        next_row, 0, producto_item1)
                    self.inventory.setItem(
                        next_row, 1, producto_item2)
                    self.inventory.setItem(
                        next_row, 2, producto_item3)
                    self.inventory.setItem(
                        next_row, 3, producto_item4)
                    self.inventory.setItem(
                        next_row, 4, producto_item5)
                    self.inventory.setItem(
                        next_row, 5, producto_item6)
                    self.inventory.setItem(
                        next_row, 6, producto_item7)
                    self.inventory.setItem(
                        next_row, 7, producto_item8)



            self.addnew.clicked.connect(self.openingadd)
        except Exception as e:
            messagebox.showerror("Error","Ha ocurrido un error inesperado." + str(e))


    def openingadd(self):
        try:
            self.close()
            self.addinventory = Module_products_un()
            self.addinventory.show()
        except Exception as e:
            messagebox.showwarning("Error", "Ha ocurrido un error inesperado" + (str(e)))