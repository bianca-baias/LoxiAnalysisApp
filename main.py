from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout 
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Loxi Analysis")
        
        container = QWidget()
        self.setCentralWidget(container)
        
        layout = QGridLayout(container)
        
        
        name = QLabel("Hello World")
        name.setAlignment(Qt.AlignCenter)
        
        year = QLabel("2026")
        
        layout.addWidget(name, 0, 0)
        layout.addWidget(year, 0, 1)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()