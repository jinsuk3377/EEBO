
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
        self.setFixedSize(573, 743)
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(10, 44, 141, 101))
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
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(10, 250, 551, 481))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 551, 24))
        self.textEdit.setObjectName("textEdit")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(160, 70, 421, 441))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(10, 150, 141, 91))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.radioButton_2 = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 30, 90, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_3 = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 50, 90, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton_4.setGeometry(QtCore.QRect(10, 70, 101, 16))
        self.radioButton_4.setObjectName("radioButton_4")
        self.calendarWidget = QtWidgets.QCalendarWidget(self)
        self.calendarWidget.setGeometry(QtCore.QRect(290, 44, 272, 191))
        self.calendarWidget.setObjectName("calendarWidget")
        self.frame_3 = QtWidgets.QFrame(self)
        self.frame_3.setGeometry(QtCore.QRect(160, 40, 120, 201))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.radioButton_5 = QtWidgets.QRadioButton(self.frame_3)
        self.radioButton_5.setGeometry(QtCore.QRect(10, 10, 90, 16))
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_6 = QtWidgets.QRadioButton(self.frame_3)
        self.radioButton_6.setGeometry(QtCore.QRect(10, 30, 90, 16))
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_7 = QtWidgets.QRadioButton(self.frame_3)
        self.radioButton_7.setGeometry(QtCore.QRect(10, 50, 90, 16))
        self.radioButton_7.setObjectName("radioButton_7")
        self.main_widget = QtWidgets.QWidget(self)
        #self.main_widget.setGeometry(QtCore.QRect(150, 365, 400, 440))
        self.main_widget.setGeometry(QtCore.QRect(10, 250, 551, 481))
        self.qvBoxLayout = QtWidgets.QVBoxLayout(self.main_widget)
        
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "BSI_Lab"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        for i in range(len(self.df_day.columns)):
            item = self.listWidget.item(i)
            item.setText(_translate("Form", self.df_day.columns[i]))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.radioButton.setText(_translate("Form", "Heatmap(default)"))
        self.radioButton_2.setText(_translate("Form", "Energy"))
        self.radioButton_3.setText(_translate("Form", "Load Profile"))
        self.radioButton_4.setText(_translate("Form", "Load Duration"))
        
        self.radioButton_5.setText(_translate("Form", "Select1"))
        self.radioButton_6.setText(_translate("Form", "Select2"))
        self.radioButton_7.setText(_translate("Form", "Select3"))
        
        self.textEdit.setHtml(_translate("Form", "File Name"))
        
    def itemClickedEvent(self, item):
        self.plot_Heatmap(column_name=item.text())
        
    def setDefaultPlotting(self):
        self.radioButton.setChecked(True)
        self.plot_Heatmap(column_name=self.listWidget.item(1).text())
        
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

