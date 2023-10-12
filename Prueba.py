import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QTableView, QWidget
from PyQt6.QtCore import Qt


def search_in_database(search_text):

    results = ['Resultado 1', 'Resultado 2', 'Resultado 3']
    return results

class SearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Barra de Búsqueda')
        self.setGeometry(100, 100, 800, 600)

        self.searchsupplier = QLineEdit()
        self.searchsupplier.setPlaceholderText('Buscar en la base de datos')

        search_layout = QVBoxLayout()
        search_layout.addWidget(self.searchsupplier)

        central_widget = QWidget()
        central_widget.setLayout(search_layout)
        self.setCentralWidget(central_widget)


        self.searchsupplier.textChanged.connect(self.perform_search)

        self.result_view = QTableView()
        self.result_view.horizontalHeader().hide()
        self.result_view.verticalHeader().hide()
f
    def perform_search(self):
        search_text = self.searchsupplier.text()
        results = search_in_database(search_text)  


        results_str = '\n'.join(results)
        self.result_view.setRowCount(len(results))
        for row, result in enumerate(results):
            self.result_view.setItem(row, 0, QTableWidgetItem(result))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SearchApp()
    window.show()
    sys.exit(app.exec())