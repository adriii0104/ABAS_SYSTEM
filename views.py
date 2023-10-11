try:
    from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QListView, QListWidgetItem, \
        QPushButton, QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QFormLayout, \
        QTableWidgetItem
    from PyQt6.QtGui import QIcon, QPainter, QFont, QMovie
    from PyQt6 import uic, QtCore, QtGui
    from PyQt6.QtCore import Qt, QTimer, QDateTime, QSize
    import sys
    from SRC.settings import *
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
            self.setFixedSize(QSize(480, 440))
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
                        self.open_window = home()
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
            self.setFixedSize(QSize(1400, 840))
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.setWindowTitle(APP_REQUERIMENTS[1])

            self.times = datetime.now().strftime("%H:%M:%S")
            self.timering.setText(self.times)

            self.date.setText(datetime.now().strftime("%d/%m/%Y"))
            self.closes.clicked.connect(self.close_app)

            self.timee = QTimer(self)
            self.timee.timeout.connect(self.timere)
            self.timee.start(1000)

            self.name_enterprise.setText(USER_SESSION["enterprise_name"])

            self.information_1.clicked.connect(lambda: self.open_information(APP_INFORMATIONS["info1"]))
            self.information_2.clicked.connect(lambda: self.open_information(APP_INFORMATIONS["info2"]))

        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

    def open_information(self, message):
        QMessageBox.information(self, "Información", message)

    def close_app(self):
        try:
            self.close()
        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al cerrar la aplicación: " + str(e))

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

        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

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
            self.setFixedSize(QSize(211, 861))
            self.setWindowTitle("Inicio")
            self.factbutton.clicked.connect(self.open_facturation)

        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

    def close_assets(self):
        self.close()

    def open_facturation(self):
        self.facturation_window = Facturation()
        self.facturation_window.show()



   
        
     

