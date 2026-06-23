from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt

class TableModel(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        #self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        self.info = {"reaction_time": {"low": "After the bot appears, you engage immediately", "below_average": "After the bot appears, you engage with a small delay", "average": "Your reaction time is average", "above_average": "After the bot appears, you engage with a high delay", "high": "After a bot appears, you take too long to enagage with it"},
                    "flick_accuracy": {"low": "Your flick is precise", "below_average": "Your flick is good", "average": "Your flick accuracy is average", "above_average": "Your flick accuracy is bad", "high": "You over or under flick"},
                    "headshot_percentage": {"low": "You have a bad headshot count", "below_average": "You have a low headshot count", "average": "You have an average headshot count", "above_average": "You have a good headshot count", "high": "You have an excellent headshot count"},
                    "shot_efficiency": {"low": "You use very few bullets/bot", "below_average": "You use a couple of bullets/bot", "average": "You use an average number of bullets/bot", "above_average": "You use many bullets/bot", "high": "You use too many bullets/bot"},
                    "time_on_target": {"low": "After placing the crosshair on the head, you imediately fire", "below_average": "After placing the crosshair on the head, you take a few moments to fire", "average": "You spend an average time to fire after the crosshair placement", "above_average": "After placing the crosshair on the head, you fire with a high delay", "high": "After placing the crosshair on the head, you hesitate to fire"},
                    "time_to_kill": {"low": "You kill a bot quickly", "below_average": "You kill a bot shortly after it appears", "average": "You kill a bot in average time", "above_average": "You kill a bot with a delay after it appears", "high": "You take too long to kill a bot"}}
    
    
    def create_table(self, stats, score, limits):
        self.data = stats
        self.score = score
        self.limits = limits
        
        self.column_labels = ["Value", "Additional info", "Score"]
        self.row_labels = [label for label in stats.keys() if label not in ["headshots", "shots"]]
        
        self.setColumnCount(len(self.column_labels))
        self.setRowCount(len(self.row_labels))
        
        self.set_column_labels()
        self.set_row_labels(limits)
        
        self.populate_table(limits)
        
        header = self.horizontalHeader()
        header.setSectionResizeMode(self.column_labels.index("Additional info"), QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        
    def set_column_labels(self):
        self.setHorizontalHeaderLabels(self.column_labels)
    
    
    def set_row_labels(self, limits):
        headers = [label.replace("_", " ").capitalize() for label in self.row_labels]
        self.setVerticalHeaderLabels(headers)
        for item in range(len(headers)):
            if self.verticalHeaderItem(item).text() != "Headshot percentage":
                self.verticalHeaderItem(item).setToolTip(f"Best: (close to) {limits[self.row_labels[item]]["range"][0]} -> Worst: over {limits[self.row_labels[item]]["range"][1]}")
            else:
                self.verticalHeaderItem(item).setToolTip(f"Best: {limits[self.row_labels[item]]["range"][1]} -> Worst: {limits[self.row_labels[item]]["range"][0]}")

    
    
    def gather_info(self):
        information = {}
        average_range = 10
        past_average_range = 25

        for stat, value in self.data.items():
            if stat not in ["headshots", "shots"]:
                max_limit_value = max(self.limits[stat]["range"][0], self.limits[stat]["range"][1])
                average_limit_low = ((50 - average_range)/100)*max_limit_value
                average_limit_high = ((50 + average_range)/100)*max_limit_value
                under_average_value = ((50 - (average_range + past_average_range))/100)*max_limit_value
                over_average_value = ((50 + (average_range + past_average_range))/100)*max_limit_value

                if value < average_limit_low:
                    if value < under_average_value:
                        information[stat] = "low"
                    else:
                        information[stat] = "below_average"
                elif average_limit_low <= value <= average_limit_high:
                    information[stat]= "average"
                elif value > average_limit_high:
                    if value < over_average_value:
                        information[stat] = "above_average"
                    else:
                        information[stat] = "high"
        
        return information

    def set_color_of_cell(self, table_item, status, mode):
        if (status == "low" and mode == "descending") or (status == "high" and mode =="ascending"):
            table_item.setBackground(QtGui.QColor(168, 61, 42)) 
        elif (status == "below_average" and mode == "descending") or (status == "above_average" and mode =="ascending"):
            table_item.setBackground(QtGui.QColor(186, 112, 74))
        elif status == "average":
            table_item.setBackground(QtGui.QColor(168, 134, 42))   
        elif (status == "above_average" and mode == "descending") or (status == "below_average" and mode =="ascending"):
            table_item.setBackground(QtGui.QColor(163, 189, 72))
        else:
            table_item.setBackground(QtGui.QColor(42, 168, 57))

    def populate_table(self, limits):
        value_column = self.column_labels.index("Value")
        meaning_column = self.column_labels.index("Additional info")
        score_column = self.column_labels.index("Score")
        information = self.gather_info()        
        
        for i in range(len(self.row_labels)):
            label = self.row_labels[i]
            value_item =  QtWidgets.QTableWidgetItem(str("{:.4f}".format(self.data[label])))
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(i, value_column, value_item)
            
            meaning_item = QtWidgets.QTableWidgetItem(self.info[label][information[label]])            
            self.set_color_of_cell(meaning_item, information[label], limits[label]["mode"])
            self.setItem(i, meaning_column, meaning_item)
        
        self.setSpan(0, score_column, len(self.row_labels), 1)
        score_item = QtWidgets.QTableWidgetItem(str("{:.2f}".format(self.score*100)))
        score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(0, score_column, score_item)
        