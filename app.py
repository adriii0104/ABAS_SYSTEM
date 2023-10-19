from views import *
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys

if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = Main()
        window.show()
        sys.exit(app.exec())
