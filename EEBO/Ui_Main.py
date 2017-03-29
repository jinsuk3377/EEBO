# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

import sys
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt

class Ui_Main (QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        super(Ui_Main, self).__init__()
        self.setupUi(self)
        self.plot_Heatmap()
        
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(571, 522)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(10, 70, 131, 351))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(20, 430, 121, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(20, 450, 90, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(Form)
        self.radioButton_3.setGeometry(QtCore.QRect(20, 470, 90, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(Form)
        self.radioButton_4.setGeometry(QtCore.QRect(20, 490, 101, 16))
        self.radioButton_4.setObjectName("radioButton_4")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(160, 70, 421, 441))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 370, 24))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(390, 9, 75, 26))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(470, 9, 90, 26))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "BSI_Lab"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Form", "textlist1"))
        item = self.listWidget.item(1)
        item.setText(_translate("Form", "textlist2"))
        item = self.listWidget.item(2)
        item.setText(_translate("Form", "textlist3"))
        item = self.listWidget.item(3)
        item.setText(_translate("Form", "textlist4"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.radioButton.setText(_translate("Form", "Heatmap(default)"))
        self.radioButton_2.setText(_translate("Form", "Energy"))
        self.radioButton_3.setText(_translate("Form", "Load Profile"))
        self.radioButton_4.setText(_translate("Form", "Load Duration"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">File Path</p></body></html>"))
        self.pushButton.setText(_translate("Form", "Select"))
        self.pushButton_2.setText(_translate("Form", "Run Analysis"))
        
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

    # https://plot.ly/python/heatmaps-contours-and-2dhistograms-tutorial/   
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
 
    def plot_Heatmap(self):
        width = 650  # plot width 
        height = 800  # plot height
        
        df_day = self.df_to_day()
        # Make heatmap object
        for i in range(len(df_day.columns)):
            column_name = df_day.columns[i]
            
            df_in = df_day[column_name].reset_index()
            z_day = df_day[column_name].reset_index(drop=True)
            
            the_months, the_days, Z_dayXmonth = self.dates_to_dayXmonth(df_in, z_day)
            # the_months = x-axis, the_days = y-axis, Z_dayXmonth = data
            
            # XAxistitle='Months in sample'
            # YAxistitle='Days of the month', # y-axis title
            
            extent = [the_months[0], the_months[-1], the_days[0], the_days[-1]]
            
            plt.figure(i + 1)
            plt.title(column_name)
            plt.imshow(Z_dayXmonth, interpolation='none', extent=extent, origin='low', aspect=0.25)
            plt.colorbar()
            
        plt.show()
        print("plot done")
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Window = Ui_Main()
    Window.show()
    sys.exit(app.exec_())

