# settings_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QFileDialog, QPushButton, QGridLayout
from PySide6.QtCore import Qt, QSize, QThreadPool
from worker import Worker
import os


class AnalysisWindow(QMainWindow):
    def __init__(self, home_window):
        super().__init__()
        
        width = 900
        height = 500
        self.setFixedSize(QSize(width, height))
        self.setWindowTitle("Loxi Analysis")
        self.threadpool = QThreadPool()
        self.home_window = home_window

        container = QWidget()
        self.setCentralWidget(container)
        
        layout = QGridLayout()
        container.setLayout(layout)
        
        # Labels
        self.file_label = QLabel("Video")
        layout.addWidget(self.file_label, 0, 0)

        self.file_path_label=QLabel("")
        self.file_path = None
        layout.addWidget(self.file_path_label, 0, 1)
        
        self.status_label = QLabel("")
        layout.addWidget(self.status_label, 2, 1, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Buttons
        self.browse = QPushButton("Select video")
        self.browse.clicked.connect(self.browse_video)
        layout.addWidget(self.browse, 0, 2)
        
        self.start_analysis = QPushButton("Start analysis")
        self.start_analysis.clicked.connect(self.analyse)
        self.start_analysis.setVisible(False)
        layout.addWidget(self.start_analysis, 1, 1)

        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.go_to_homepage)
        self.home_button.setVisible(True)
        layout.addWidget(self.home_button, 3, 0)

        self.start_new = QPushButton("New Analysis")
        self.start_new.clicked.connect(self.reset_ui)
        self.start_new.setVisible(False)
        layout.addWidget(self.start_new, 3, 2)
    
    
    def browse_video(self):
        browse_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "(*.mp4)")
        
        if browse_path:
            self.file_path = browse_path
            self.file_path_label.setText(self.file_path)
            self.start_analysis.setVisible(True)
            self.status_label.setText("")
        else:
            self.file_path_label.setText("")
            self.start_analysis.setVisible(False)
            self.status_label.setText("Choose a video")


    def go_to_homepage(self):
        self.reset_ui()
        self.home_window.show()
        self.hide()
    

    def reset_ui(self):
        self.file_path = None
        self.file_path_label.setText("")
        self.status_label.setText("")
        self.start_analysis.setVisible(False)
        self.browse.setDisabled(False)
        #self.home_button.setVisible(True)
        self.start_new.setVisible(False)


    def analyse(self):
        self.start_analysis.setVisible(False)
        self.browse.setDisabled(True)
        self.home_button.setVisible(False)
        
        #yolo_path = r"C:\Users\bianc\Desktop\Facultate\Licenta\LoxiAnalysisApp\files\best.pt"
        yolo_path = r"C:\Users\Gamebox\Desktop\train3-headshots\weights\best.pt"
        
        #video_p = r"C:\Users\bianc\Desktop\Facultate\Licenta\Fisiere\Video\1.4.1.mp4"
        video_path = self.file_path
        
        #results_location = r"C:\Users\bianc\Desktop"
        #results_location = r"C:\Users\Gamebox\Desktop\Licenta-diverse"
        #results_location = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 

        #self.threadpool = QThreadPool()
        worker = Worker(yolo_path, video_path, self.status_label)
        worker.signals.finished.connect(self.update_gui)
        worker.signals.error.connect(self.error_analysis)

        self.threadpool.start(worker)
    
    def update_gui(self):
        #self.browse.setDisabled(True)
        self.home_button.setVisible(True)
        self.start_new.setVisible(True)
    
    def error_analysis(self, err_info):
        self.status_label.setText(str(err_info))
        self.update_gui()

