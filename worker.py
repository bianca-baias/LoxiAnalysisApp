from PySide6.QtCore import QObject, QRunnable, Slot, Signal
from analyse import Analysis

class WorkerSignals(QObject):
    finished = Signal() 
    error = Signal(tuple)
    #progress = Signal(tuple) 


class Worker(QRunnable):
    def __init__(self, results_location, yolo_path, video_path, label):
        super().__init__()
        self.results_location = results_location
        self.yolo_path = yolo_path
        self.video_path = video_path
        self.status_label = label
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            print("Thread started")
            analysis_object = Analysis(self.results_location, self.yolo_path, self.video_path, self.status_label)
            analysis_object.run()
        except Exception as e:
            self.signals.error.emit(e)
        finally:
            self.signals.finished.emit()
            print("Ending thread!")
            self.autoDelete()
            
            
