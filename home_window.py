from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import QSize, Qt
from analysis_window import AnalysisWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.analysis_window = AnalysisWindow(self)
        
        width = 900
        height = 500
        self.setFixedSize(QSize(width, height))
        self.setWindowTitle("Loxi Analysis")
        
        container = QWidget()
        self.setCentralWidget(container)
        
        layout = QHBoxLayout()
        container.setLayout(layout)
        
        get_started_button = QPushButton("Get started")
        get_started_button.setObjectName("browse-button")
        get_started_button.setFixedWidth(125)
        get_started_button.clicked.connect(self.move_to_analysis)
        
        layout.addWidget(get_started_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addSpacing(40)
        
    def move_to_analysis(self):
        self.analysis_window.show()
        self.hide()
