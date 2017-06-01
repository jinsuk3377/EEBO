"""Make load duration plots."""


#--- Provide access.
#
import numpy as np
#
import matplotlib.pyplot as plt
import matplotlib.dates as mpld


def load_duration(loads, y_label='power', y_units='kW',
    asPercent=False,
    loadRange=[None, None]):
    """
    Plot *loads*, sorted in descending order.

    **Args:**

    - *loads*, array-like sequence of floating-point data.
    - *asPercent*, flag indicating how to format the independent (duration) axis.
      If ``True`` express duration as a percent of time.
      If ``False``, express duration as the number of observations.
    - *loadRange*, a two-element list giving the extents of the y (load) axis.
      Set either or both elements of the list to ``None``, in order to accept
      the default extent based on the data.
    """
    #
    # Check inputs.
    assert( type(y_label) == str )
    assert( type(y_units) == str )
    assert( type(asPercent) == bool )
    assert( len(loadRange) == 2 )
    #
    # TODO: Call typical_xy and just be essentially a sort function.
    #
    # Sort in reverse order.
    #   Note native Python :func:`sorted` is broken with respect to NANs.
    sortedLoads = np.sort(loads)
    #
    # Expect a one-dimensional array.
    lastGoodIdx = sortedLoads.shape
    assert( len(lastGoodIdx) == 1 )
    lastGoodIdx = lastGoodIdx[0] - 1
    #
    # Pick off any NANs on the back.
    while( lastGoodIdx>=0 and np.isnan(sortedLoads[lastGoodIdx]) ):
        lastGoodIdx -= 1
    #
    # Create a view into *sortedLoads*, elements 0 through *lastGoodIdx*, in
    # reverse order.
    sortedLoads = sortedLoads[lastGoodIdx::-1]
    #
    # Plot.
    mainfig = plt.figure()
    plot1 = mainfig.add_subplot(111)
    if( asPercent ):
        percentList = np.linspace(start=0, stop=100, num=len(sortedLoads))
        plot1.plot(percentList, sortedLoads)
        plot1.set_xlabel('percent time')
    else:
        plot1.plot(sortedLoads)
        plot1.set_xlabel('number of observations')
    #
    # Format.
    plot1.set_title('Load Duration Curve')
    plot1.set_ylabel(y_label + ' ['+y_units+']')
    if( loadRange[0] is not None ):
        plot1.set_ylim(bottom=loadRange[0])
    if( loadRange[1] is not None ):
        plot1.set_ylim(top=loadRange[1])
    #
    return ( mainfig )
    #
    # End :func:`plot_load_duration`.
