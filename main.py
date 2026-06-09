# main.py
from PySide6.QtWidgets import QApplication
from home_window import MainWindow

app = QApplication([])

window = MainWindow()
window.show()

app.exec()