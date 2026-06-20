# main.py
from PySide6.QtWidgets import QApplication
from home_window import MainWindow

app = QApplication([])

with open("style.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

window = MainWindow()

window.show()

app.exec()