"""Make heatmap given a grid of daily (?) data."""


#--- Provide access.
#
import numpy as np
import scipy.stats
#
import matplotlib.pyplot as plt
# import matplotlib.dates as mpld
#
from matplotlib import cm
#
import datetime as dto


# TODO: Should have a value for square feet or should we pass a grid of EUIs?


def heatmap(x_val, values, x_label, y_label, units_label):
    """
    Plots *values* as a heatmap.

    **Args:**

    - *values*, 2D array sequence of values
    - *x_label*, string for x-axis labels, default to 'kW/sf' (?)
    - *y_label*, string for y-axis labels, default to 'dates'
    """
    #
    # Implementation note: this function uses :func:`matplotlib.pyplot.pcolormesh` to make vectors.
    #
    # Check input.
    assert (x_val.shape == values.shape)
    assert (type(x_label) == str)
    assert (type(y_label) == str)
    assert (type(units_label) == str)

    # Relics of old code
    upper5 = scipy.stats.scoreatpercentile(values,per=95)
    lower5 = scipy.stats.scoreatpercentile(values,per=5)
    rowCt, colCt = values.shape
    # print rowCt, colCt, lower5, upper5

    x_coor,y_coor = np.meshgrid(np.arange(0,colCt),np.arange(0,rowCt))
    # TODO: y_coor should be a string or a float not a datetime object

    mainfig = plt.figure()
    plot1 = mainfig.add_subplot(111)


    htmap = plot1.pcolormesh(x_coor,y_coor,values,
        norm=None, vmin=lower5, vmax=upper5,
        cmap=cm.coolwarm,)
    # TODO: Change ``cmap`` to be more general

    cbar = plt.colorbar(htmap, shrink=0.9)
    cbar.set_label(units_label)

    # TODO: Figure out how to set the tickmarks with the correct dates.
    # This is a boiler plate fix to have the tickmarks be on every Monday.
    # Need to investigate matplotlib.dates
    # Nonetype breaks strftime.
    if rowCt < 7:
        tickSpacing = 1
    else:
        tickSpacing = 7
    plot1.set_yticks(range(0,rowCt,tickSpacing))
    makeLabel = lambda datetime: datetime.strftime('%m/%d/%y') if( datetime is not None ) else None
    plot1.set_yticklabels([makeLabel(dt[0]) for dt in x_val[0:rowCt:tickSpacing]])

    # Format.
    plot1.set_xlim(0,colCt-1)
    plot1.set_ylim(0,rowCt-1)
    plot1.tick_params(axis='both', which='major', labelsize=10)
    plot1.set_title('Heat map of data for uploaded data')
    plot1.set_xlabel(x_label)
    plot1.set_ylabel(y_label)
    # plot1.grid(True)

    return mainfig
