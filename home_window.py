from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QLabel, QWidget, QGridLayout, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from analysis_window import AnalysisWindow
from results_window import ResultsWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.analysis_window = AnalysisWindow()
        self.results_window = ResultsWindow()
        
        width = 900
        height = 500
        self.setFixedSize(QSize(width, height))
        self.setWindowTitle("Loxi Analysis")
        
        container = QWidget()
        self.setCentralWidget(container)
        
        horizontal_layout = QHBoxLayout()
        container.setLayout(horizontal_layout)
        
        image = QLabel()
        image_pixmap = QPixmap("images/valorant-logo.png")
        image.setPixmap(image_pixmap.scaled(254, 200))
        image.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        image.setFixedWidth(int(width/2))
        
        get_started_button = QPushButton("Get started")
        get_started_button.setFixedWidth(125)
        get_started_button.clicked.connect(self.move_to_analysis)
        
        horizontal_layout.addWidget(image)
        horizontal_layout.addWidget(get_started_button)
        
    def move_to_analysis(self):
        self.analysis_window.show()
        self.hide()
