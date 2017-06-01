"""Make energy signature plots."""


#--- Provide access.
#
import matplotlib.pyplot as plt
import matplotlib.dates as mpld


def energy_sig(temperature, values,
    temperatureAxisLabel,
    valueAxisLabel, metric=None, valueRange=[None, None]):
    """
    Plot *values* as function of *temperature*.

    **Args:**

    - *temperature*, array-like sequence of :class:`datetime` objects.
    - *values*, array-like sequence of floating-point data.
    - *valueRange*, a two-element list giving the extents of the y-axis.
    """
    #
    # Check inputs.
    assert( len(temperature) > 1 )
    assert( len(values) == len(temperature) )
    assert( type(temperatureAxisLabel) == str )
    assert( type(valueAxisLabel) == str )
    assert( metric is None or isinstance(metric,float) )
    assert( len(valueRange) == 2 )
    # FIXME: Find a way to fill in the gaps for missing values
    #
    # Plot.
    mainfig = plt.figure()
    plot1 = mainfig.add_subplot(111)
    plot1.plot(temperature, values, linestyle='None', marker='o')
    #
    # Format.
    mainfig.autofmt_xdate()
    plot1.set_xlabel(temperatureAxisLabel)
    #
    plot1.set_ylabel(valueAxisLabel)
    if( valueRange[0] is not None ):
        plot1.set_ylim(bottom=valueRange[0])
    if( valueRange[1] is not None ):
        plot1.set_ylim(top=valueRange[1])
    #
    if( metric is not None ):
        plot1.set_title('Energy Signature \n'+
                        'Weather Sensitivity ='+'{0:.2f}'.format(metric))
    #
    # plot1.grid(True)
    #
    return( mainfig )
    #
    # End :func:`plot_energy_sig`.
