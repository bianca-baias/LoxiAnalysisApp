from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

class TableModel(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        #self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.info = {"reaction_time": {"low": "After the bot appears, you engage quicly", "average": "Your reaction time is average", "high": "After a bot appears, you take a long time to enagage with it"},
                    "flick_accuracy": {"low": "Your flick is precise", "average": "Your flick accuracy is average", "high": "You over/under flick"},
                    "headshot_percentage": {"low": "You have a low headshot count", "average": "You have an average headshot count", "high": "You have a high headshot count"},
                    "shot_efficiency": {"low": "You use a few bullets/bot", "average": "You have an average shot efficiency", "high": "You use a lot of bullets/bot"},
                    "time_on_target": {"low": "After placing the crosshair on the head, you imediately fire", "average": "You spend an average time to fire after the crosshair placement", "high": "After placing the crosshair on the head, you hesitate to fire"},
                    "time_to_kill": {"low": "You kill a bot quickly", "average": "You kill a bot in average time", "high": "You take too long to kill a bot"}}
    
    
    def create_table(self, stats, score, limits):
        self.data = stats
        self.score = score
        self.limits = limits
        
        self.column_labels = ["Value", "Additional info", "Score"]
        self.row_labels = [label for label in stats.keys() if label not in ["headshots", "shots"]]
        
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(len(self.row_labels))
        
        self.set_column_labels()
        self.set_row_labels()
        
        self.populate_table()
        
        header = self.horizontalHeader()
        header.setSectionResizeMode(self.column_labels.index("Additional info"), QtWidgets.QHeaderView.ResizeMode.Stretch)
        
    def set_column_labels(self):
        self.setHorizontalHeaderLabels(self.column_labels)
    
    
    def set_row_labels(self):
        self.setVerticalHeaderLabels(self.row_labels)
    
    def gather_info(self):
        information = {}
        average_range = 10
        
        for stat, value in self.data.items():
            if stat not in ["headshots", "shots"]:
                average_value = (self.limits[stat]["range"][0] + self.limits[stat]["range"][1]) / 2
                average_limit_low = average_value - (average_range/100*average_value)
                average_limit_high = average_value + (average_range/100*average_value)
                
                if value < average_limit_low:
                    information[stat] = "low"
                elif average_limit_low <= value <= average_limit_high:
                    information[stat]= "average"
                else:
                    information[stat] = "high"
        
        return information

    def populate_table(self):
        value_column = self.column_labels.index("Value")
        meaning_column = self.column_labels.index("Additional info")
        score_column = self.column_labels.index("Score")
        information = self.gather_info()
        
        for i in range(len(self.row_labels)):
            label = self.row_labels[i]
            self.setItem(i, value_column, QtWidgets.QTableWidgetItem(str("{:.4f}".format(self.data[label]))))
            self.setItem(i, meaning_column, QtWidgets.QTableWidgetItem(self.info[label][information[label]]))
        
        self.setSpan(0, score_column, len(self.row_labels), 1)
        self.setItem(0, score_column, QtWidgets.QTableWidgetItem(str("{:.2f}".format(self.score*100))))