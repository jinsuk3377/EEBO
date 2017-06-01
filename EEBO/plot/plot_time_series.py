"""Make time series plots."""


#--- Provide access.
#
import matplotlib.pyplot as plt
import matplotlib.dates as mpld


def time_series(times, values,
    timeAxisLabel,
    valueAxisLabel, plotTitle=None,
    valueRange=[None, None],
    seriesArgs={'linestyle':'-', 'marker':None, 'color':'blue'},
    gridArgs={'alpha':0.5}
    ):
    """
    Plot *values* as function of *times*.

    **Args:**

    - *times*, array-like sequence of :class:`datetime` objects.
    - *values*, array-like sequence of floating-point data.
    - *valueRange*, a two-element list giving the extents of the y-axis.
    - *seriesArgs*, dictionary of arguments for controlling the series, or ``None``.
    - *gridArgs*, dictionary of arguments for controlling the grid, or ``None``.

    **Notes:**

    - Each key in *seriesArgs* is the name of :class:`matplotlib.lines.Line2D` property that can be
      set by matplotlib's :meth:`pyplot.plot`.  These include 'color', 'linestyle',
      'linewidth', 'marker', 'fillstyle', and 'alpha'.  The corresponding value is
      an allowed value for that property.  For example:
      ``{'color':'green', 'linestyle':'--', 'linewidth':2.1, 'marker':'+', 'alpha':0.8}``
    - *gridArgs* has the same structure as *seriesArgs*.  For example:
      ``{'color':'blue', 'linestyle':'-.', 'linewidth':0.3, 'alpha':0.8}``.
    """
    #
    # Check inputs.
    assert( len(times) > 1 )
    assert( len(values) == len(times) )
    assert( type(timeAxisLabel) == str )
    assert( type(valueAxisLabel) == str )
    assert( len(valueRange) == 2 )
    assert( (seriesArgs is None) or (type(seriesArgs)==dict) )
    assert( (gridArgs is None) or (type(gridArgs)==dict) )
    #
    # Create figure.
    mainfig = plt.figure()
    plot1 = mainfig.add_subplot(111)
    #
    # Plot.
    if( seriesArgs is None ):
        plot1.plot(times, values, linestyle='-', marker=None)
    else:
        plot1.plot(times, values, **seriesArgs)
    #
    # Format.
    mainfig.autofmt_xdate()
    plot1.set_xlabel(timeAxisLabel)
    #
    plot1.set_ylabel(valueAxisLabel)
    if( valueRange[0] is not None ):
        plot1.set_ylim(bottom=valueRange[0])
    if( valueRange[1] is not None ):
        plot1.set_ylim(top=valueRange[1])
    #
    if( plotTitle is not None ):
        plot1.set_title(plotTitle)
    #
    if( gridArgs is not None ):
        plot1.grid(**gridArgs)
    #
    return( mainfig )
    #
    # End :func:`time_series`.
