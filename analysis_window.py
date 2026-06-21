# settings_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QFileDialog, QPushButton, QGridLayout, QHBoxLayout, QProgressBar, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QSize, QThreadPool
from worker import Worker
from results_table import TableModel


class AnalysisWindow(QMainWindow):
    def __init__(self, home_window):
        super().__init__()
        
        window_width = 900
        window_height = 500
        self.setFixedSize(QSize(window_width, window_height))
        self.setWindowTitle("Loxi Analysis")
        
        self.threadpool = QThreadPool()
        self.home_window = home_window        
        
        self.limits = {"reaction_time": {"range": [0, 2], "mode": "ascending"}, "time_to_kill": {"range": [0, 2], "mode": "ascending"}, "flick_accuracy": {"range": [0, 40], "mode": "ascending"}, "time_on_target": {"range": [0, 1], "mode": "ascending"}, "headshot_percentage": {"range": [0, 1], "mode": "descending"}, "shot_efficiency": {"range": [1, 5], "mode": "ascending"}}
        self.yolo_path = r"C:\Users\bianc\Desktop\Facultate\Licenta\LoxiAnalysisApp\files\best.pt"
        
        container = QWidget()
        self.setCentralWidget(container)
        
        self.layout = QGridLayout()
        container.setLayout(self.layout)
        
        self.table = TableModel()
        self.table.setFixedWidth(85/100*window_width)
        
        self.layout.addWidget(self.table, 3, 0, 1, 4, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.table.setVisible(False)
        self.layout.setRowStretch(3, 1)

        self.horizontal_layout = QHBoxLayout()
        self.vertical_layout = QVBoxLayout()
        
        self.status_label = QLabel("")
        self.vertical_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter, stretch=0)
        
        self.spinner = QProgressBar()
        self.spinner.setRange(0, 0)  # Sets both min and max to 0
        self.spinner.setTextVisible(False)  # Hides any percentage text
        self.spinner.setVisible(False)
        self.vertical_layout.addWidget(self.spinner, alignment= Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, stretch=1)
        
        self.layout.addLayout(self.vertical_layout, 2, 1, 1, 2)
        
        # Labels
        self.file_label = QLabel("Video: ")
        self.horizontal_layout.addWidget(self.file_label, stretch=0)
        
        self.file_path_label=QLabel("")
        self.file_path = None
        self.horizontal_layout.addWidget(self.file_path_label, stretch=1)
        
        self.layout.addLayout(self.horizontal_layout, 0, 0, 1, 3)
        
        # Buttons
        self.browse = QPushButton("Select video")
        self.browse.clicked.connect(self.browse_video)
        self.layout.addWidget(self.browse, 0, 3, 1, 1)
        
        self.start_analysis = QPushButton("Start analysis")
        self.start_analysis.clicked.connect(self.analyse)
        self.start_analysis.setVisible(False)
        self.layout.addWidget(self.start_analysis, 1, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter)
        
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.go_to_homepage)
        self.home_button.setVisible(True)
        self.layout.addWidget(self.home_button, 5, 0)
        
        self.start_new = QPushButton("New Analysis")
        self.start_new.clicked.connect(self.reset_ui)
        self.start_new.setVisible(False)
        self.layout.addWidget(self.start_new, 5, 3)

    
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
        self.status_label.setVisible(True)
        self.start_analysis.setVisible(False)
        self.browse.setDisabled(False)
        self.start_new.setVisible(False)
        self.table.setVisible(False)
        self.spinner.setVisible(False)


    def analyse(self):
        try:
            self.start_analysis.setVisible(False)
            self.browse.setDisabled(True)
            self.home_button.setDisabled(True)
            self.spinner.setVisible(True)
            video_path = self.file_path
            
            worker = Worker(self.yolo_path, video_path, self.status_label, self.limits)
            worker.signals.finished.connect(self.successful_analysis)
            worker.signals.error.connect(self.error_analysis)
            
            self.threadpool.start(worker)
        except Exception as e:
            #print(e)
            self.error_analysis(f"Error while running the anaysis: {e}")
    
    
    def update_gui(self):
        self.home_button.setDisabled(False)
        self.start_new.setVisible(True)
        self.spinner.setVisible(False)
    
    def display_table(self, statistics, score):
        try:
            #print(f"Displaying table. \nScore={score}, \nStats={statistics}")
            self.status_label.setVisible(True)
            self.status_label.setText("Results")

            self.table.create_table(statistics, score, self.limits)
            
            self.table.doItemsLayout()
            total_height = (
                self.table.horizontalHeader().height() +
                sum(self.table.rowHeight(i) for i in range(self.table.rowCount())) +
                self.table.frameWidth() * 2 
            )
            self.table.setFixedHeight(total_height)
            
            self.table.setVisible(True)
            self.table.setShowGrid(False)
        except Exception as e:
            #print(e)
            self.error_analysis(f"Error while creating table: {e}")
            
            
    def successful_analysis(self, statistic, score):
        self.update_gui()
        self.status_label.setText("Analysis complete")
        self.status_label.setVisible(True)
        self.display_table(statistic, score)


        
    def error_analysis(self, err_info):
        self.status_label.setText(str(err_info))
        self.status_label.setVisible(True)
        self.table.setVisible(False)
        self.update_gui()

