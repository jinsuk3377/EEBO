
import set_date
import read_data
import gen_plot
#import plot.plot_timestamp

import sys
import pandas as pd

from PyQt5 import QtCore, QtWidgets

class Ui_Main (QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi()
        self.menuBarUi()
        self.retranslateUi()
        
        #self.setDefaultPlotting()
    '''
    def setDefaultPlotting(self):
        self.radioButton.setChecked(True)
        self.plot_Heatmap(column_name=self.listWidget.item(1).text())
    '''
    def itemClickedEvent(self, item):
        self.plot_Heatmap(column_name=item.text())
        
    def setupUi(self):
        self.setObjectName("Form")
        self.setFixedSize(573, 800)
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(10, 64, 141, 85))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemClicked.connect(self.itemClickedEvent)
        
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(10, 30, 553, 24))
        self.textEdit.setObjectName("textEdit")
        
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(10, 270, 551, 481))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
         
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(10, 160, 141, 120))
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 30, 120, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 50, 120, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 70, 120, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_4.setGeometry(QtCore.QRect(10, 90, 120, 16))
        self.radioButton_4.setObjectName("radioButton_4")
        
        self.calendarWidget = QtWidgets.QCalendarWidget(self)
        self.calendarWidget.setGeometry(QtCore.QRect(290, 64, 272, 191))
        self.calendarWidget.setObjectName("calendarWidget")
        
        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setGeometry(QtCore.QRect(160, 60, 120, 220))
        self.groupBox_2.setObjectName("groupBox_2")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_5.setGeometry(QtCore.QRect(10, 30, 90, 16))
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_5.setChecked(True)
        self.radioButton_5.clicked.connect(self.radioButtonClicked)
        self.radioButton_6 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_6.setGeometry(QtCore.QRect(10, 50, 90, 16))
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_6.clicked.connect(self.radioButtonClicked)
        self.radioButton_7 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_7.setGeometry(QtCore.QRect(10, 70, 90, 16))
        self.radioButton_7.setObjectName("radioButton_7")
        self.radioButton_7.clicked.connect(self.radioButtonClicked)
        self.radioButton_8 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_8.setGeometry(QtCore.QRect(10, 90, 90, 16))
        self.radioButton_8.setObjectName("radioButton_8")
        self.radioButton_8.clicked.connect(self.radioButtonClicked)
        self.radioButton_9 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_9.setGeometry(QtCore.QRect(10, 110, 90, 16))
        self.radioButton_9.setObjectName("radioButton_9")
        self.radioButton_9.clicked.connect(self.radioButtonClicked)
        self.radioButton_10 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_10.setGeometry(QtCore.QRect(10, 130, 90, 16))
        self.radioButton_10.setObjectName("radioButton_10")
        self.radioButton_10.clicked.connect(self.radioButtonClicked)
        self.radioButton_11 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_11.setGeometry(QtCore.QRect(10, 150, 90, 16))
        self.radioButton_11.setObjectName("radioButton_11")
        self.radioButton_11.clicked.connect(self.radioButtonClicked)
        
    def menuBarUi(self):
        mainMenu = self.menuBar()
        self.importAction = QtWidgets.QAction("&Import File", self)
        self.importAction.setShortcut('Ctrl+I')
        #self.importAction.triggered.connect(importFile)
        self.exitAction = QtWidgets.QAction('&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(QtWidgets.qApp.quit)
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.importAction)
        self.fileMenu.addAction(self.exitAction)

        self.helpMenu = mainMenu.addMenu('help')
                
        self.main_widget = QtWidgets.QWidget(self)
        self.main_widget.setGeometry(QtCore.QRect(10, 300, 551, 481))
        self.qvBoxLayout = QtWidgets.QVBoxLayout(self.main_widget)
        
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        
        df_day=set_date.df_to_day()

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "EEBO"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        #for i in range(len(self.df_day.columns)):
        for i in range(len(df_day.columns)):
            item = self.listWidget.item(i)
            item.setText(_translate("Form", df_day.columns[i]))
            #item.setText(_translate("Form", self.df_day.columns[i]))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("Form", "Graph"))
        self.radioButton.setText(_translate("Form", "Heatmap(default)"))
        self.radioButton_2.setText(_translate("Form", "Timestamp"))
        self.radioButton_3.setText(_translate("Form", "Load Profile"))
        self.radioButton_4.setText(_translate("Form", "Load Duration"))
        self.groupBox_2.setTitle(_translate("Form", "Timestamp"))
        self.radioButton_5.setText(_translate("Form", "10min"))
        self.radioButton_6.setText(_translate("Form", "15min"))
        self.radioButton_7.setText(_translate("Form", "30min"))
        self.radioButton_8.setText(_translate("Form", "60min"))
        self.radioButton_9.setText(_translate("Form", "Day"))
        self.radioButton_10.setText(_translate("Form", "Week"))
        self.radioButton_11.setText(_translate("Form", "Month"))
        
        self.textEdit.setHtml(_translate("Form", "File Name"))

    def radioButtonClicked(self):
        #enum
        if self.radioButton_5.isChecked():
            self.df_day=self.df_to_min10()
        elif self.radioButton_6.isChecked():
            self.df_day = self.df_to_min15()
        elif self.radioButton_7.isChecked():
            self.df_day = self.df_to_min30()
        elif self.radioButton_8.isChecked():
            self.df_day = self.df_to_min60()
        elif self.radioButton_9.isChecked():
            self.df_day = self.df_to_day()
        elif self.radioButton_10.isChecked():
            self.df_day = self.df_to_week()
        elif self.radioButton_11.isChecked():
            self.df_day = self.df_to_month()
    
    def importFile(self):
        
        #import UI execute
        #data_path = ui
        df = read_data.readData()
        #read_data.importData(data_path)
    
    #def plot(self):
        
        #select plot type
        #if self.radioButton_5.isChecked():
        #    self.df_day=self.df_to_min10()
        #plot_Timestamp = plot_timestamp(int)
        
        #switch or if elif
        #    call plot(plot_Timestamp)
    
    def generatePlot(self):
        gen_plot()
    
                
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Window = Ui_Main()
    Window.show()
    sys.exit(app.exec_())

