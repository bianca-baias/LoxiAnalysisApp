# main.py
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6 import QtGui
from home_window import MainWindow

def set_app_icons(app, image_path):
    myappid = "loxianalysis.1.1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app.setWindowIcon(QtGui.QIcon(image_path))

def apply_stylesheet(app, sheet_path):
    with open(sheet_path, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)


app = QApplication([])

image_path = "images/icon.jpg"
sheet_path = "style.qss"
set_app_icons(app, image_path)
apply_stylesheet(app, sheet_path)

window = MainWindow()

window.show()

app.exec()