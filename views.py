try:
    from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QListView, QListWidgetItem, QPushButton, QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QFormLayout
    from PyQt6.QtGui import QIcon, QPainter, QFont, QMovie
    from PyQt6 import uic, QtCore, QtGui
    from PyQt6.QtCore import Qt, QTimer, QDateTime, QSize
    import sys
    from SRC.settings import APP_REQUERIMENTS
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
            QMessageBox.critical(self, "Error", "Error al iniciar la aplicación: " + str(e))

    def open_windows(self):
        try:
            self.close()
            self.login = Login()
            self.login.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", "Error al iniciar la aplicación: " + str(e))


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
            self.cerrar.clicked.connect(self.closed)
            self.minimizar.clicked.connect(self.minimizedd)
        except Exception as e:
            QMessageBox.critical(self, "Error", "Error al iniciar la aplicación: " + str(e))

    def closed(self):
        self.close()
    def minimizedd(self):
        self.showMinimized()

class Facturation(QMainWindow):
    def __init__(self):
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("UI/facturation.ui", self)
            self.setFixedSize(QSize(780, 640))
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.setWindowTitle(APP_REQUERIMENTS[1])
            self.closes.clicked.connect(self.close_app)

        except Exception as e:
            QMessageBox.critical(self, "Error", "Error al iniciar la aplicación: " + str(e))

    def close_app(self):
        try:
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", "Error al cerrar la aplicación: " + str(e))





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())
