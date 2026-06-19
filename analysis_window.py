# settings_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QFileDialog, QPushButton, QGridLayout
from PySide6.QtCore import Qt, QSize, QThreadPool
#from analyse import Analysis
from worker import Worker

class AnalysisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        width = 900
        height = 500
        self.setFixedSize(QSize(width, height))
        self.setWindowTitle("Loxi Analysis")
        self.threadpool = QThreadPool()

        container = QWidget()
        self.setCentralWidget(container)
        
        layout = QGridLayout()
        container.setLayout(layout)
        
        self.file_label = QLabel("Video")
        layout.addWidget(self.file_label, 0, 0)
        
        self.file_path_label=QLabel("")
        self.file_path = None
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
        browse_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "(*.mp4)")
        
        if browse_path:
            self.file_path = browse_path
            self.file_path_label.setText(self.file_path)
            self.start_analysis.setVisible(True)
        else:
            self.file_path_label.setText("")
            self.start_analysis.setVisible(False)

    def analyse(self):
        self.start_analysis.setVisible(False)
        self.browse.setDisabled(True)
        
        #yolo_path = r"C:\Users\bianc\Desktop\Facultate\Licenta\LoxiAnalysisApp\files\best.pt"
        yolo_path = r"C:\Users\Gamebox\Desktop\train3-headshots\weights\best.pt"
        
        #video_p = r"C:\Users\bianc\Desktop\Facultate\Licenta\Fisiere\Video\1.4.1.mp4"
        video_path = self.file_path
        
        #results_location = r"C:\Users\bianc\Desktop"
        results_location = r"C:\Users\Gamebox\Desktop\Licenta-diverse"

        #self.threadpool = QThreadPool()
        worker = Worker(results_location, yolo_path, video_path, self.status_label)
        worker.signals.finished.connect(self.update_gui)
        worker.signals.error.connect(self.error_analysis)

        self.threadpool.start(worker)
    
    def update_gui(self):
        self.start_analysis.setVisible(True)
        self.browse.setDisabled(False)
    
    def error_analysis(self, err_info):
        self.status_label.setText(str(err_info))
        self.update_gui()

