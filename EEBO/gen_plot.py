#generate plot

"""
Generate raw elements of a building analysis.

**Notes:**

- In general, these fcns make plots and find summary statistics, but do not set
  the final output format.  Final output is controlled by format-specific
  generation functions (e.g., in :mod:`gen_html`).  Those should call the
  functions defined here, in order to do any building-specific analysis.

**Enhancements:**

- The grand vision is that the plotting fcns will become more general and more
  more capable, and these routines will call the plotting functions to assemble
  the particular figure of interest.  Currently, many of the plot routines are
  very specific to buildings (e.g., :mod:`plot.plot_load_duration` plots a load
  duration curve).  Eventually, building-specific analyses should be handled
  here (e.g., finding a load-duration curve, then handing off the data to a
  generic plotting function).  For now, though, a lot of the functions here are
  just thin wrappers.
- Similarly, analysis routines ought to achieve a greater separation between
  building-specific routines (like integrating power to find energy over a year)
  and general routines (like integrating points), and the building-specific
  bits should migrate here.
- All fcns here should catch Exceptions thrown by underlying work routines,
  log those exceptions to some standard error-handler, and return ``False`` to
  indicate a failure.  Goal is to not propagate Exceptions up to caller, which
  is assumed to be an output-directed routine.  If caller wants to note failure
  status in output, that's fine, but it shouldn't have to catch exceptions.
"""


#--- Provide access.
#
import datetime as dto
#
from util import make_ticklabels as mtl
#
from util import calc_statistics as a_stat
from util import calc_energy_from_power as cep
#
#from ..energy_star.target_finder import gen_xml_tgtfndr as gxml
#from ..energy_star.target_finder import retrieveEnergyStarScore_tgtfndr as rtgf
#
from plot import plot_energy_sig as plt_es
from plot import plot_heatmap as plt_heat
from plot import plot_load_duration as plt_ldc
from plot import plot_time_series as plt_ts
from plot import plot_longitudinal_bm as plt_lbm
from plot import plot_cross_sectional_bm as plt_cbm
#

def genDailySummary(loadsByDay, bldgMetaData,
    replacements):
    #
    """
    Given an array *loadsByDay*, find the daily summary statistics, storing
    them in *replacements*.

    **Returns:**

    - *success*, ``True`` if successfully wrote the results.

    **Args:**

    - *loadsByDay*, a ``numpy`` array, each row of which corresponds to a unique day.
    - *bldgMetaData*, dictionary of measurement units and other metadata.
    - *replacements*, dictionary to be filled in.
    """
    #
    # TODO: There's a fair amount of data manipulation going on here.  It's all pretty
    # straightforward, but still it would be good to get it under test.
    #
    # Check inputs.
    # TODO: Eventually want to handle other units.
    loadUnitsStr = bldgMetaData['load-units']
    assert( loadUnitsStr == 'kW' )
    #
    floorAreaSf = float(bldgMetaData['floor-area'])
    assert( floorAreaSf > 0 )
    assert( bldgMetaData['floor-area-units'] == 'sf' )
    #
    # Find statistics.
    summaryStats = a_stat.gridStats(loadsByDay, 'r')
    loadVariability = a_stat.variability(loadsByDay)
    #
    # Load intensities (load normalized by floor area).
    replacements['{:summary-load-intensity-units:}'] = 'W/sf'
    maxLoadIntensity = summaryStats['max'] * 1e3 / floorAreaSf
    replacements['{:summary-overall-max-load-intensity:}'] = "{0:.2f}".format(maxLoadIntensity)
    minLoadIntensity = summaryStats['min'] * 1e3 / floorAreaSf
    replacements['{:summary-overall-min-load-intensity:}'] = "{0:.2f}".format(summaryStats['min'])
    #
    # Loads.
    replacements['{:summary-load-units:}'] = loadUnitsStr
    replacements['{:summary-ave-daily-peak-load:}'] = "{0:.2f}".format(summaryStats['peak95'].mean())
    replacements['{:summary-ave-daily-base-load:}'] = "{0:.2f}".format(summaryStats['base5'].mean())
    replacements['{:summary-ave-daily-load-range:}'] = "{0:.2f}".format(summaryStats['range95_5'].mean())
    #
    # Dimensionless values.
    replacements['{:summary-ave-daily-bp-load-ratio:}'] = "{0:.2f}".format(summaryStats['bpratio'].mean())
    replacements['{:summary-load-variability:}'] = "{0:.2f}".format(loadVariability)
    #
    return( True )
    #
    # End :func:`genDailySummary`.


def genLoadProfilePlot(datetimes, loads, loadUnitsStr,
    figWritePath):
    #
    """
    Generate the load profile plot, of *loads* versus *datetimes*.

    **Returns:**

    - *success*, ``True`` if successfully generated the figure.

    **Args:**

    - *figWritePath*, path to save figure.
    """
    #
    # TODO: Clip to two months.
    #
    mainfig = plt_ts.time_series(datetimes, loads,
        timeAxisLabel='Date',
        valueAxisLabel='power [' +loadUnitsStr +']', valueRange=[0, None],
        plotTitle='Time Series Load Profile')
    if( mainfig is None ):
        return( False )
    #
    mainfig.savefig(figWritePath)
    #
    return( True )
    #
    # End :func:`genLoadProfilePlot`.


def genHeatMap(timesByDay, loadsByDay, loadUnitsStr,
    figWritePath):
    """
    Generate the heat map plot, of *loadsByDay* versus *timesByDay*.

    **Returns:**

    - *success*, ``True`` if successfully generated the figure.

    **Args:**

    - *figWritePath*, path to save figure.
    """
    #
    # TODO: Clip to one year.  For efficiency, may want to clip outside this fcn,
    # since so many fcns want one year.  This fcn can still test for more than a
    # year, and only clip if necessary.
    #
    mainfig = plt_heat.heatmap(timesByDay, loadsByDay,
        x_label='hour of day', y_label='date', units_label=loadUnitsStr)
    if( mainfig is None ):
        return( False )
    #
    # TODO: normalize by floor area.
    # TODO: Labeling x-axis as 'hour of day' but this is not inherent in array
    # *timesByDay*-- they could be minutes, or 15-minute intervals.  Could
    # peek into *timesByDay* and adjust values if necessary, or could just
    # make explicit that caller has to do this.  But right now there's no
    # control or documentation of this fact.
    #
    mainfig.savefig(figWritePath)
    #
    return( True )
    #
    # End :func:`genHeatMap`.


def genEnergySignaturePlot(oats, loads, oatUnitsStr, loadUnitsStr,
    figWritePath):
    #
    """
    Generate the energy signature plot, of *loads* versus *oats*.

    **Returns:**

    - *success*, ``True`` if successfully generated the figure.

    **Args:**

    - *figWritePath*, path to save figure.
    """
    #
    # TODO: Clip to one year.  For efficiency, may want to clip outside this fcn,
    # since so many fcns want one year.  This fcn can still test for more than a
    # year, and only clip if necessary.
    #
    weatherSensitivity = a_stat.findSpearmanRank(loads, oats)
    mainfig = plt_es.energy_sig(oats, loads,
        temperatureAxisLabel='outside air temperature [' +oatUnitsStr +']',
        valueAxisLabel='power [' +loadUnitsStr +']',
        metric = weatherSensitivity,
        valueRange=[0, None])
    if( mainfig is None ):
        return( False )
    #
    mainfig.savefig(figWritePath)
    #
    return( True )
    #
    # End :func:`genEnergySignaturePlot`.


def genLoadDurationCurve(loads, loadUnitsStr,
    figWritePath):
    #
    """
    Generate the load duration curve for *loads*.

    **Returns:**

    - *success*, ``True`` if successfully generated the figure.

    **Args:**

    - *figWritePath*, path to save figure.
    """
    #
    # TODO: Consider an overlay, when have more than a year's worth of data, of
    # the load duration for just the past year, along with load duration for
    # the entire data set.
    #
    mainfig = plt_ldc.load_duration(loads, 'power', loadUnitsStr,
        asPercent=True,
        loadRange=[0,None])
    if( mainfig is None ):
        return( False )
    #
    mainfig.savefig(figWritePath)
    #
    return( True )
    #
    # End :func:`genLoadDurationCurve`.


def genLongitudBenchmark(datetimes, loads, loadUnitsStr, gasLoads, gasUnitsStr,
    figWritePath):
    #
    """
    Generate the longitudinal benchmarking plot.

    **Returns:**

    - *success*, ``True`` if successfully generated the figure.

    **Args:**

    - *figWritePath*, path to save figure.

    **Notes:**

    - Require at least two year's worth of data in order to make the plot.
    """
    #
    #
    yearlyElectricityLabel = "Annual Electricity [kWh]"
    #
    yearlyElectricity = cep.calc_annual_energy(loads,datetimes)
    #
    if( len(yearlyElectricity) <= 1 ):
        return( False )
    #    
    # Extract data
    yearlyElectricityTotal = [column[0] for column in yearlyElectricity]
    yearlyStartDate = [column[1] for column in yearlyElectricity]
    yearlyEndDate = [column[2] for column in yearlyElectricity]    
    yearlyTickLabels = mtl.ticklabel_start_end_ym(yearlyStartDate, yearlyEndDate)
    #
    #
    if ( gasLoads is not None):
        yearlyGas = cep.calc_annual_energy(gasLoads,datetimes)
        yearlyGasTotal = [column[0] for column in yearlyGas]
        yearlyGasAxisLabel="Annual Natural Gas [kBtu]"
    else:
        yearlyGasTotal = None
        yearlyGasAxisLabel = None
    #    
    mainfig = plt_lbm.longtitud_bm(yearlyElectricityTotal, yearlyTickLabels,
        value1AxisLabel=yearlyElectricityLabel,
        timesAxisLabel="Datetime",
        plotTitle="Longitudinal Benchmarking",
        valueRange=[None, None],
        values2=yearlyGasTotal,
        value2AxisLabel=yearlyGasAxisLabel)
    if( mainfig is None ):
        return( False )
    #
    mainfig.savefig(figWritePath)
    #
    return( True )
    #
    # End :func:`genLongitudBenchmark`.
    
def genCrossSectionBenchmark(datetimes, loads, bldgMetaData, replacements, 
    gasLoads, xmlWritePath, figWritePath):
    #
    """
    Generate the cross sectional benchmarking plot.

    **Returns:**

    - *success*, ``True`` if successfully generated the figure.

    **Args:**

    - *figWritePath*, path to save figure.
    - *xmlWritePath*, path to save xml file. 

    **Notes:**

    - Require at least two year's worth of data in order to make the plot.
    """
    #       
    # Fill replacement keys 
    yearlyElectricity = cep.calc_annual_energy(loads,datetimes)
    #
    if( len(yearlyElectricity) <= 1 ):
        return( False )
    #    
    # Extract energy data.
    energyUse_list = list()
    energyUse_list.append( ('Electric','kWh (thousand Watt-hours)',int(yearlyElectricity[0][0])) )
    #
    if ( gasLoads is not None):
        yearlyGas = cep.calc_annual_energy(gasLoads,datetimes)
        energyUse_list.append( ('Natural Gas','kBtu (thousand Btu)',int(yearlyGas[0][0])) )
    #
    '''
    # Generate XML files and strings
    targetFinder_xml = gxml.gen_xml_targetFinder(bldgMetaData,energyUse_list,xmlWritePath)
    PMMetrics = rtgf.retrieveScore(targetFinder_xml)
    #
    if ( PMMetrics['designScore'][0].isdigit() ):
        pmScore = float(PMMetrics['designScore'][0])
        pmEndDate = dto.datetime.strftime(yearlyElectricity[0][2],'%Y-%m-%d')
        mainfig = plt_cbm.crossSection_bm(pmScore,pmEndDate,'ENERGY STAR score',valueRange=[None,100])
    else: 
        return( False )
        
    if( mainfig is None ):
        return( False )
    #                                    
    mainfig.savefig(figWritePath)
    #
    return( True )
    #
    # End :func:`genCrossSectionBenchmark`.
    '''
