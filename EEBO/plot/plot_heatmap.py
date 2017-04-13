import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


#class heatmap(self, plot_Timestamp):
    



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
        
    

    def plot_Heatmap(self, column_name):
        
        hc = HeatMapMplCanvas(self.main_widget, width=5, height=4, dpi=100, data=self.df_day, column_name=column_name)
        
        #http://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
        for i in reversed( range(self.qvBoxLayout.count()) ): 
            self.qvBoxLayout.itemAt(i).widget().deleteLater()
            
        self.qvBoxLayout.addWidget(hc)
