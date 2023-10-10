from views import Login, Facturation
from PyQt6.QtWidgets import QApplication
import sys

class Add_data_Table(Facturation):
    print("corriendo")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())