# settings_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QFileDialog, QPushButton, QGridLayout
from PySide6.QtCore import Qt, QSize

class AnalysisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        width = 900
        height = 500
        self.setFixedSize(QSize(width, height))
        self.setWindowTitle("Loxi Analysis")
        
        container = QWidget()
        self.setCentralWidget(container)
        
        layout = QGridLayout()
        container.setLayout(layout)
        
        self.file_label = QLabel("Video")
        layout.addWidget(self.file_label, 0, 0)
        
        self.file_path_label=QLabel("")
        layout.addWidget(self.file_path_label, 0, 1)
        
        self.browse = QPushButton("Select video")
        self.browse.clicked.connect(self.browse_video)
        layout.addWidget(self.browse, 0, 2)
        
        self.start_analysis = QPushButton("Start analysis")
        self.start_analysis.clicked.connect(self.analyse)
        self.start_analysis.setVisible(False)
        layout.addWidget(self.start_analysis, 1, 1)
        
        self.status_label = QLabel("")
        layout.addWidget(self.status_label, 2, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
    
    def browse_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "(*.mp4)")
        if file_path:
            self.file_path_label.setText(file_path)
            self.start_analysis.setVisible(True)

    def analyse(self):
        self.start_analysis.setVisible(False)
        self.browse.setDisabled(True)
        self.status_label.setText("Analyzing...")
        
