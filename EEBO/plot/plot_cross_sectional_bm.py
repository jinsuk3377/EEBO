""""Makes the cross-sectional benchmarking plot"""


#--- Provide access.
#
import numpy as np
import datetime as dto
#
import matplotlib.pyplot as plt

def crossSection_bm(value,
                 dateAxisLabel,
                 valueAxisLabel="energy",
                 valueRange=[None, None]):

    """
    Creates additional arguments for cross-sectional benchmarking.

    **Args:**

    - *values*, array-like sequence of floating point data
    - *valueAxisLabel*, string argument used for axis labels
    - *plotTitle*, string argument used for ploat title
    - *valueRange*, a two-element list giving the extents of the y-axis.

    **Returns:**

    - *mainfig*, :class:`matplotlib` figure, or ``None`` if there are not enough
      data to complete the plot.

    **Notes:**

    - For Cross-sectional Benchmarking, the score is calculated through Portfolio Manager.
    """
    #
    # Check inputs.
    assert (type(valueAxisLabel) == str)
    assert (type(dateAxisLabel) == str)
    assert (np.isfinite(value))
    #
    # Hex Color Codes 
    blue_hex = '#0033CC' 
    green_hex = '#006600' 
    red_hex = '#CC3300'
    #
    mainfig = plt.figure()
    plot = mainfig.add_subplot(111)
    #
    plot.axhspan (ymin=50, ymax=75, color=green_hex, alpha=0.25)
    plot.axhspan (ymin=75, ymax=100, color=green_hex, alpha=0.95)
    #
    plot.bar(0.5,value,0.20,color=blue_hex,align='center',label='electricity')
    #
    plot.set_xlabel('For the 12-month period ending:\n'+str(dateAxisLabel))
    # Sets the width of the window.
    plot.set_xlim(left=0, right=1) 
    #
    plot.set_ylabel(valueAxisLabel)
    if( valueRange[0] is not None ):
        plot.set_ylim(bottom=valueRange[0])
    if( valueRange[1] is not None ):
        plot.set_ylim(top=valueRange[1])
    #
    # 
    ytickmarks = np.arange(0,125,25)
    plot.set_yticks(ytickmarks) # This makes the x-tick marks invisible.
    #
    plot.set_xticks([]) # This makes the x-tick marks invisible.
    #
    plot.set_title('Cross-Sectional Benchmarking \n ENERGY STAR Score='+str(value))
    mainfig.tight_layout()
    #
    return( mainfig )
    #
    # End :func:`longtitud_bm`.
