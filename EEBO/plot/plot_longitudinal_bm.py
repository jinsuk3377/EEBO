""""Makes the longitudinal benchmarking plot"""


#--- Provide access.
#
import numpy as np
#
import matplotlib.pyplot as plt


def longtitud_bm(values1, xTickLabels,
                 value1AxisLabel="energy",
                 timesAxisLabel="datetime",
                 plotTitle="Column chart of data",
                 valueRange=[None, None],
                 values2=None,
                 value2AxisLabel="energy"):

    """
    Creates additional arguments for longitudinal benchmarking.

    **Args:**

    - *values*, array-like sequence of floating point data
    - *valueAxisLabel* and *timesAxisLabel*, string argument used for axis labels
    - *valueRange*, a two-element list giving the extents of the y-axis.

    **Returns:**

    - *mainfig*, :class:`matplotlib` figure, or ``None`` if there are not enough
      data to complete the plot.

    **Notes:**

    - For Longitudinal Benchmarking, aggregate the data into annual values.
    - The base value the first full year is considered.
    """
    #
    # Check inputs.
    valCt = len(values1)
    assert( xTickLabels is None or len(xTickLabels)==valCt )
    assert (type(value1AxisLabel) == str)
    assert (type(timesAxisLabel) == str)
    assert( len(valueRange) == 2 )
    #
    # Hex Color Codes 
    blue_hex = '#0033CC' 
    green_hex = '#006600' 
    red_hex = '#CC3300'
    #
    # Require at least two elements to make plot.
    if( valCt < 2 ):
        return( None )
    #
    # Create custom xTickLabels.
    if (xTickLabels == None):
        xTickLabels = list()
        xTickLabels.append('base year')
        for labelItem in range(valCt-1):
            xTickLabels.append('year '+ str(labelItem+1))

    tickPositions = np.arange(valCt)
    barWidth = 0.40
    #
    mainfig = plt.figure()
    plot1 = mainfig.add_subplot(111)
    plot1.bar(tickPositions,values1,barWidth,color=blue_hex,align='center',label='electricity')
    #
    # Format.
    plot1.set_xticklabels(xTickLabels)
    plot1.set_xticks(tickPositions+(barWidth/2.))
    #
    plot1.set_xlabel(timesAxisLabel)
    #
    plot1.set_ylabel(value1AxisLabel, color=blue_hex)
    if( valueRange[0] is not None ):
        plot1.set_ylim(bottom=valueRange[0])
    if( valueRange[1] is not None ):
        plot1.set_ylim(top=valueRange[1])
    #
    #--- Plot for second set of bars 
    if ( values2 != None ) : 
        assert (type(value2AxisLabel == str))
        # Match x-axis with plot1
        plot2 = plot1.twinx()
        #
        plot2.bar(tickPositions+barWidth,values2,barWidth, color=green_hex,align='center',label='naturalgas')
        # Format
        plot2.set_xlabel(timesAxisLabel)
        #
        plot2.set_ylabel(value2AxisLabel, color=green_hex)
        if( valueRange[0] is not None ):    
            plot2.set_ylim(bottom=valueRange[0])
        if( valueRange[1] is not None ):
            plot2.set_ylim(top=valueRange[1])
    #
    plot1.set_title(plotTitle)
    mainfig.tight_layout()

    return( mainfig )
    #
    # End :func:`longtitud_bm`.
