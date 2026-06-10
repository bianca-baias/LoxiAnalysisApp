# settings_window.py
from PySide6.QtWidgets import QMainWindow

class ResultsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Results")