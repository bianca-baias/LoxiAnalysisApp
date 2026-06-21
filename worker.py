from PySide6.QtCore import QObject, QRunnable, Slot, Signal
from analyse import Analysis
from exceptions import NoBotDetected, NoKillDetected

class WorkerSignals(QObject):
    finished = Signal(dict, float) 
    error = Signal(tuple)


class Worker(QRunnable):
    def __init__(self, yolo_path, video_path, label, limits):
        super().__init__()
        
        self.yolo_path = yolo_path
        self.video_path = video_path
        self.status_label = label
        self.statistics = {}
        self.score = 0.0
        self.limits = limits
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            #print("Thread started")
            analysis_object = Analysis(self.yolo_path, self.video_path, self.status_label)
            self.statistics, self.score = analysis_object.run(self.limits)
            self.signals.finished.emit(self.statistics, self.score)
        except NoBotDetected:
            self.signals.error.emit("No bot detected in the video!")
            #print(f"No bot detected in the video selected.")
        except NoKillDetected:
            self.signals.error.emit("No kill detected in the video!")
            #print(f"No kill detected in the video selected.")
        except Exception as e:
            self.signals.error.emit(e)
            #print(f"Error while running the analysis: {e}")
        finally:
            #print("Ending thread!")
            self.autoDelete()
            
            
