try:
    from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QListView, QListWidgetItem, QPushButton, QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QFormLayout
    from PyQt6.QtGui import QIcon, QPainter, QFont, QMovie
    from PyQt6 import uic, QtCore, QtGui
    from PyQt6.QtCore import Qt, QTimer, QDateTime, QSize
    import sys
    from SRC.settings import *
except Exception as e:
        QMessageBox.critical("Error", "Error al iniciar la aplicación: " + str(e))



class Login(QMainWindow):
    def __init__(self):
        try:
            # Aquí se carga la interfaz gráfica, SIEMPRE DEBEMOS LLAMAR A SUPER Y AL UIC PARA PODER.
            super().__init__()
            uic.loadUi("C:/Users/el_nd/OneDrive/Escritorio/ABAS_SYSTEM/dist/views/_internal/UI/login.ui", self)

            self.setWindowTitle(APP_REQUERIMENTS[1])
            self.setFixedSize(QSize(680, 330))
            self.version.setText(APP_REQUERIMENTS[0])
            self.app_name.setText(APP_REQUERIMENTS[1])

        except Exception as e:
            QMessageBox.critical(self, "Error", "Error al iniciar la aplicación: " + str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())
