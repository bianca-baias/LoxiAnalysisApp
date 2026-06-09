# settings_window.py
from PySide6.QtWidgets import QWidget

class ResultsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Results")