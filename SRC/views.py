from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QListView, QListWidgetItem, QPushButton, QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QFormLayout
from PyQt6.QtGui import QIcon, QPainter, QFont, QMovie
from PyQt6 import uic, QtCore, QtGui
from PyQt6.QtCore import Qt, QTimer, QDateTime
import sys


class Login(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi("UI/login.ui", self)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())