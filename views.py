try:
    from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QListView, QListWidgetItem, QPushButton, QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QFormLayout
    from PyQt6.QtGui import QIcon, QPainter, QFont, QMovie
    from PyQt6 import uic, QtCore, QtGui
    from PyQt6.QtCore import Qt, QTimer, QDateTime, QSize
    import sys
    from SRC.settings import APP_REQUERIMENTS
    from datetime import datetime
except Exception as e:
    QMessageBox.critical("Error", "Error al iniciar la aplicación: " + str(e))


class Main(QMainWindow):
    def __init__(self):
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
            self.close()
            self.login = Login()
            self.login.show()
        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))


class Login(QMainWindow):
    def __init__(self):
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/login.ui", self)
            self.setFixedSize(QSize(480, 440))
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.setWindowTitle(APP_REQUERIMENTS[1])
            self.version.setText(APP_REQUERIMENTS[0])
            self.close.clicked.connect(self.close_login)
            self.minimized.clicked.connect(self.minimized_login)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

    def close_login(self):
        self.close()

    def minimized_login(self):
        self.showMinimized()


class Facturation(QMainWindow):
    def __init__(self):
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/facturation.ui", self)
            self.setFixedSize(QSize(1400, 840))
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.setWindowTitle(APP_REQUERIMENTS[1])

            self.fecha.setText(datetime.now().strftime("%d/%m/%Y"))
            self.closes.clicked.connect(self.close_app)

            self.timee = QTimer(self)
            self.timee.timeout.connect(self.timere)
            self.timee.start(1000)

        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))

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


class assets(QMainWindow):
    def __init__(self):
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/assets.ui", self)
            self.setFixedSize(QSize(780, 675))
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.setWindowTitle(APP_REQUERIMENTS[1])
            self.close.clicked.connect(self.close_assets)
            self.cancel.clicked.connect(self.close_assets)
            self.minimized.clicked.connect(self.minimized_assets)

        except Exception as e:
            QMessageBox.critical(
                self, "Error", "Error al iniciar la aplicación: " + str(e))
    
    def close_assets(self):
        self.close()

    def minimized_assets(self):
        self.showMinimized()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = assets()
    window.show()
    sys.exit(app.exec())
