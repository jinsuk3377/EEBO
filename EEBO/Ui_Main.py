
import sys
import datetime

from PyQt5 import QtCore, QtWidgets

import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#http://stackoverflow.com/questions/8653092/using-matplotlib-axes-with-ginput-and-imshow
class MyMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100, data=None, column_name=None):
        self.fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi)
        self.data = data
        self.column_name = column_name
        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class HeatMapMplCanvas (MyMplCanvas):
    
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
    
    # https://plot.ly/python/heatmaps-contours-and-2dhistograms-tutorial/
    def compute_initial_figure(self):
        dt = self.data
        column_name = self.column_name
            
        df_in = dt[column_name].reset_index()
        z_day = dt[column_name].reset_index(drop=True)
        
        the_months, the_days, Z_dayXmonth = self.dates_to_dayXmonth(df_in, z_day)
        
        extent = [the_months[0], the_months[-1], the_days[0], the_days[-1]]
        
        self.axes.clear()
        self.axes.set_title(column_name)
        
        #http://matplotlib.org/examples/pylab_examples/colorbar_tick_labelling_demo.html
        cax = self.axes.imshow(Z_dayXmonth, interpolation='none', extent=extent, origin='low', aspect=0.25)
        cbar = self.fig.colorbar(cax)
        
    def dates_to_dayXmonth(self, df_in, z_in):
        
        # http://stackoverflow.com/questions/31613018/datetime64ns-to-timestamp-string-in-pandas
        dates = pd.DatetimeIndex(df_in['Date']).to_native_types()
        
        # (1.1) List of months for all item in dates 
        months = np.array([datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m')
                           for date in dates])
        
        # (1.2) Find indices of first day of the months
        _, ind_tmp = np.unique(months, return_index=True)  # -> array([90,212,31,0, ...])
        the_months_ind = np.sort(ind_tmp).tolist()  # -> array([0,31,59,90, ...])
    
        # (1*) Use these indices to make list months' name
        the_months = months[the_months_ind].astype(np.int)
        N_the_months = len(the_months)  # 8 months, in our case, from Jan to Aug
        
        # (2*) Make list of days of the month 
        N_the_days = 31
        the_days = np.arange(1, N_the_days + 1)  # [1, ..., 31]
    
        # (3.1) Make tmp array filled with NaNs
        Z_tmp = np.empty((N_the_days, N_the_months))
        Z_tmp.fill(np.nan)
    
        # (3.2) Make list of indices to fill in Z_tmp month by month
        fill_i = the_months_ind + [len(months)]
    
        # (3.3) Loop through months
        for i in range(N_the_months):
            i0 = fill_i[i]  # get start
            i1 = fill_i[i + 1]  #  and end index
            delta_i = i1 - i0  # compute their difference (either 30,31 or 28)
            Z_tmp[0:delta_i, i] = z_in[i0:i1]  # fill in rows of 
    
        # (3*) Copy tmp array to output variable
        Z = Z_tmp
    
        return (the_months, the_days, Z)  # output coordinates for our plot


class Ui_Main (QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi()
        self.df_day = self.df_to_day()
        self.retranslateUi()
        self.setDefaultPlotting()
        
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
        
        mainMenu = self.menuBar()
        self.importAction = QtWidgets.QAction("&Import File", self)
        self.importAction.setShortcut('Ctrl+I')
        #self.importAction.triggered.connect([Import csv/xlsx file])
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
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "EEBO"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        for i in range(len(self.df_day.columns)):
            item = self.listWidget.item(i)
            item.setText(_translate("Form", self.df_day.columns[i]))
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
        
    def itemClickedEvent(self, item):
        self.plot_Heatmap(column_name=item.text())
        
    def setDefaultPlotting(self):
        self.radioButton.setChecked(True)
        self.plot_Heatmap(column_name=self.listWidget.item(1).text())
    
    def radioButtonClicked(self):
        if self.radioButton_5.isChecked():
            self.df_to_min10()
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
    
    
    # http://jsideas.net/python/2015/08/30/daily_to_weekly.html
    def df_to_day(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
        
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
        
        df = df.drop(df.columns[0], 1)
        
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('D', how={df.columns[i]:np.sum}))
        
        return pd.concat(daily_df, axis=1)
    
    def df_to_week(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
        
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
        
        df = df.drop(df.columns[0], 1)
        
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('W', how={df.columns[i]:np.sum}))
        
        return pd.concat(daily_df, axis=1)
    
    def df_to_month(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
        
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
        
        df = df.drop(df.columns[0], 1)
        
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('M', how={df.columns[i]:np.sum}))
        
        return pd.concat(daily_df, axis=1)
    
    def df_to_min10(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
         
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
         
        df = df.drop(df.columns[0], 1)
         
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('10T', how={df.columns[i]:np.sum}))
         
        return pd.concat(daily_df, axis=1)
     
    def df_to_min15(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
         
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
         
        df = df.drop(df.columns[0], 1)
         
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('15T', how={df.columns[i]:np.sum}))
         
        return pd.concat(daily_df, axis=1)
     
    def df_to_min30(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
         
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
         
        df = df.drop(df.columns[0], 1)
         
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('30T', how={df.columns[i]:np.sum}))
         
        return pd.concat(daily_df, axis=1)
     
    def df_to_min60(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
         
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
         
        df = df.drop(df.columns[0], 1)
         
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('60T', how={df.columns[i]:np.sum}))
         
        return pd.concat(daily_df, axis=1)
    
    def plot_Heatmap(self, column_name):
        
        hc = HeatMapMplCanvas(self.main_widget, width=5, height=4, dpi=100, data=self.df_day, column_name=column_name)
        
        #http://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
        for i in reversed( range(self.qvBoxLayout.count()) ): 
            self.qvBoxLayout.itemAt(i).widget().deleteLater()
            
        self.qvBoxLayout.addWidget(hc)
                
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Window = Ui_Main()
    Window.show()
    sys.exit(app.exec_())

