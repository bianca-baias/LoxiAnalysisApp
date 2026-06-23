# main.py
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6 import QtGui
from home_window import MainWindow
from pathlib import Path
import sys


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path


def set_app_icons(app, image_path):
    myappid = "loxianalysis.1.1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app.setWindowIcon(QtGui.QIcon(str(image_path)))


def apply_stylesheet(app, sheet_path, bacground_path):
    with open(sheet_path, "r") as f:
        _style = f.read()
        _style = _style.replace("__BACKGROUND__", str(bacground_path).replace("\\", "/"))
        app.setStyleSheet(_style)


app = QApplication([])

icon_image_path = resource_path("images/icon.jpg")
background_image = resource_path("images/background.jpg")
sheet_path = resource_path("style/style.qss")

set_app_icons(app, icon_image_path)
apply_stylesheet(app, sheet_path,background_image)

window = MainWindow()

window.show()

app.exec()