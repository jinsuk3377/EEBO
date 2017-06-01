"""Integrate load into energy."""


#--- Provide access.
#
import datetime as dto
import numpy as np
import math
#
from . import calc_simpsons_rule as simp
#
from . import clean_data as clean
from . import datetime_utils as dtutil


#--- Constants.
#
__DAY_PER_SEC = 1.0 / (60*60*24)


def calc_annual_energy(loads, datetimes):
    """
    Find annual energy for as many full years as have data.

    **Args:**

    - *loads*, array-like sequence of power data [kW] (float).
    - *datetimes*, array-like sequence of ``datetime`` objects.

    **Returns:**

    - *yearlyEnergies*, [0] list of total energy [kW.h] (integral of *loads* over
      time), [1] list of starting dates, [2] list of ending dates, 
      for as many whole years as have data.

    **Notes:**

    - The "years" of interest are 365-day periods, not calendar years.  For
      example, if the last datum is from a day "7/13/2013", then the last
      identified year runs from "7/14/2012" through "7/13/2013".
    - Elements of *yearlyEnergies* are in chronological order.  That is, the
      most recent year appears as the last element in the list.
    - Any ``NAN`` values in *loads* are discarded.  That effectively means any
      sequence of ``NAN`` values will get integrated as if some weighted average
      of the good loads on either side of the missing sequence, held over the
      entire gap.

    **Enhancements:**

    - Return dates over which integrations performed (e.g., in a corresponding
      list, or via tuples).
    """
    #
    # Check inputs.
    assert( len(loads) == len(datetimes) )
    assert( isinstance(datetimes[0],dto.date) )
    #
    # Remove ``NAN`` values if necessary.
    if( np.any(np.isnan(loads)) ):
        goodLoads = clean.makeSelector_finite(loads)
        loadsClean = clean.applySelector(goodLoads, loads)
        datesClean = clean.applySelector(goodLoads, datetimes)
    else:
        # Note the assignments here just create references to the existing data,
        # rather than copying data.  So no big storage or speed implication.
        loadsClean = loads
        datesClean = datetimes
    #
    # Notes - identifying which data to pass to the integrator:
    #
    #   In general, the integration routine needs to have one value from some
    # date that is not in the range of dates it's supposed to integrate.  To
    # see why, consider integrating power over a single day, where data are
    # reported every six hours:
    # power ->  1   1   1   1   1
    # time  -> 00  06  12  18  24
    # day   ->  M   M   M   M   M
    #   Since power is constant at 1 kW, the energy over the day is 24 kW.h.
    #   Note that, for the integrator to consider the whole day, it needs to
    # start on Monday 0h, and run through Monday 24h.
    #   However, one of those bounding values won't be labeled as shown in the
    # diagram above.  Either:
    # - Monday 0h is labeled as Sunday 24h, or
    # - Monday 24h is labeled as Tuesday 0h.
    #   In fact, the Python ``datetime`` class takes the second option.
    # Therefore, in order to find the energy use on Monday, the first reading
    # from Tuesday has to be included in the integration.
    #
    # Notes - interpolating at date transitions:
    #
    #   If data do not fall exactly on the day transition, some interpolation
    # is needed.  Suppose data are reported every six hours as shown:
    # power ->  1   1  ----  1   1
    # time  -> 14  20  24/0  2   8
    # day   ->  M   M   M/T  T   T
    #   Let XX represent the cumulative energy consumption up to Monday 20h.
    # Then the cumulative consumption up to Tuesday 2h is XX + 6 kW.h.
    # Interpolating 4/6 of the way through the interval, the cumulative
    # consumption up to Monday 24h is XX + 4 kW.h.
    #
    # Notes - handling last date available:
    #
    #   Because ``datetime`` objects label midnight as time 0 of the day
    # just starting, treat the date of the last entry in *datesClean* as the
    # the date that starts a year.
    #   Consider the case that the last entry in *datesClean* is at exactly
    # midnight (say, on 9-September).  Then the data support treating a year as
    # starting on 9-September and running through 8-September.
    #   If, on the other hand, the last entry in *datesClean* is sometime
    # in the middle of the day (say, at 2pm on 9-September), then there are not
    # enough data to say a year runs from 9-September through 10-September.
    # Again, the first day of each year is 9-September.
    #
    # Notes - variable names.
    #
    #   Variable names for dates use the following conventions:
    # - Actual dates, which correspond to ``datetime`` or ``date`` entries
    #   in *datesClean*, have names like *currYearStartDate* and *currYearEndDate*.
    #   These may also have an associated index into *datesClean*, named like
    #   *currYearStartIdx* and *currYearEndIdx*.
    # - Theoretical dates, which define when a year begins and ends, have names
    #   like *currYearStartsOn*.
    #
    # Initialize.
    yearlyEnergies = list()    
    #
    # Last date in *datesClean* starts a year (because either it marks midnight
    # of the day before, or it has incomplete data).
    nextYearStartIdx = len(loadsClean) - 1
    if( nextYearStartIdx <= 0 ):
        return( yearlyEnergies )
    nextYearStartsOn = datesClean[nextYearStartIdx]
    #
    # Find the exact date transition if necessary.
    if( type(datesClean[0]) == dto.datetime ):
        #
        # Here, *nextYearStartsOn* has time information.
        #   Coerce it to be a pure ``date``, and adjust *nextYearStartIdx* to
        # mark the earliest ``datetime`` in *datesClean* with this date.
        nextYearStartsOn = dto.datetime(nextYearStartsOn.year, nextYearStartsOn.month, nextYearStartsOn.day, 0)
        nextYearStartIdx = dtutil.findLatestEntryBefore(datesClean, nextYearStartsOn, startIdx=0, blockIdx=nextYearStartIdx+1) + 1
    #
    # Step backward through *loadsClean*, summarizing years.
    while( True ):
        #
        # Here, assume:
        # - *nextYearStartsOn* gives the first date of the year after the year
        #   of interest.  Note that, due to missing data, *datesClean* might
        #   not have a matching date.
        # - *nextYearStartsOn* has the same type as entries in *datesClean*.
        # - *nextYearStartIdx* marks the first entry in *datesClean* that can
        #   belong to the year after the year of interest.
        #
        # Figure out range of data to integrate.
        currYearStartsOn = dtutil.goBackOneYear(nextYearStartsOn)
        prevYearEndIdx = dtutil.findLatestEntryBefore(datesClean, currYearStartsOn, startIdx=0, blockIdx=nextYearStartIdx)
        #
        # Check that data spans a full year, or close to it.
        if( prevYearEndIdx == 0 ):
            earliestDateAvailable = datesClean[0]
            missingDayCt = (earliestDateAvailable - currYearStartsOn).total_seconds() * __DAY_PER_SEC
            if( missingDayCt > 3 ):
                break
        #
        # Here:
        # - *prevYearEndIdx* marks the entry that spans the transition from the
        #   previous year, if one exists, to the current year.
        # - *nextYearStartIdx* marks the entry that spans the transition to the
        #   next year.
        #
        # Find energy use for the current year.
        #   Note have to "block" on ``nextYearStartIdx + 1`` because have to
        # integrate up to the point at *nextYearStartIdx*.
        yearlyEnergy = __integratePtsInTime(loadsClean, datesClean, startIdx=prevYearEndIdx, blockIdx=nextYearStartIdx+1)
        #
        # Adjust *yearlyEnergy* for the transition from previous year to current year.
        sec_excess = (currYearStartsOn - datesClean[prevYearEndIdx]).total_seconds()
        if( sec_excess > 0 ):
            # Excess energy is a fraction (sec_excess/sec_total) of the total
            # energy in the first bin.  Total energy in the first bin is
            # proportional to sec_total, so sec_total cancels out.
            removeEnergy = 0.5*(loadsClean[prevYearEndIdx] + loadsClean[prevYearEndIdx+1]) * sec_excess / 3600.
            yearlyEnergy -= removeEnergy
        #
        # Adjust *yearlyEnergy* for the transition from current year to next year.
        sec_excess = (datesClean[nextYearStartIdx] - nextYearStartsOn).total_seconds()
        if( sec_excess > 0 ):
            removeEnergy = 0.5*(loadsClean[nextYearStartIdx-1] + loadsClean[nextYearStartIdx]) * sec_excess / 3600.
            yearlyEnergy -= removeEnergy
        #
        # Save result.
        yearlyEnergies.append(( yearlyEnergy, 
                                currYearStartsOn, 
                                datesClean[nextYearStartIdx-1] ))
        #
        # Prepare for next iteration.
        if( prevYearEndIdx == 0 ):
            break
        nextYearStartsOn = currYearStartsOn
        nextYearStartIdx = prevYearEndIdx + 1
    #
    # Here, *yearlyEnergies* has desired values, but in the wrong order (since
    # worked backward through years, but want most recent year at end of list).
    yearlyEnergies.reverse()
    #
    return( yearlyEnergies)
    #
    # End :func:`calc_annual_energy`.


def calc_monthly_energy(loads, datetimes, monthCt):
    """
    Find monthly energy for as many full months as have data.

    **Args:**

    - *loads*, array-like sequence of power data [kW] (float).
    - *datetimes*, array-like sequence of ``datetime`` objects.
    - *monthCt*, number of months to go back

    **Returns:**

    - *monthlyEnergies*, list of total energy [kW.h] (integral of *loads* over
      time) for as many whole months as have data.

    **Notes:**

    - The "months of interest are "numerical" months. If the last datum is "7/13/2013", 
      then the last identified month is "7/13/2013" to "8/13/2013". Stepping back over a 
      month is the same for a month with 31 days and a month with 28 days. After the 
      final month, the days will be adjusted to the last day of the month, if necessary. 
    - Elements of *monthlyEnergies* are in chronological order.  That is, the
      most recent month appears as the last element in the list.
    - Any ``NAN`` values in *loads* are discarded.  That effectively means any
      sequence of ``NAN`` values will get integrated as if some weighted average
      of the good loads on either side of the missing sequence, held over the
      entire gap.

    **Enhancements:**

    - Return dates over which integrations performed (e.g., in a corresponding
      list, or via tuples).
    """
    #
    # Check inputs.
    assert( len(loads) == len(datetimes) )
    assert( isinstance(datetimes[0],dto.date) )
    #
    # Remove ``NAN`` values if necessary.
    if( np.any(np.isnan(loads)) ):
        goodLoads = clean.makeSelector_finite(loads)
        loadsClean = clean.applySelector(goodLoads, loads)
        datesClean = clean.applySelector(goodLoads, datetimes)
    else:
        # Note the assignments here just create references to the existing data,
        # rather than copying data.  So no big storage or speed implication.
        loadsClean = loads
        datesClean = datetimes
    #
    # Notes - identifying which data to pass to the integrator:
    #
    #   In general, the integration routine needs to have one value from some
    # date that is not in the range of dates it's supposed to integrate.  To
    # see why, consider integrating power over a single day, where data are
    # reported every six hours:
    # power ->  1   1   1   1   1
    # time  -> 00  06  12  18  24
    # day   ->  M   M   M   M   M
    #   Since power is constant at 1 kW, the energy over the day is 24 kW.h.
    #   Note that, for the integrator to consider the whole day, it needs to
    # start on Monday 0h, and run through Monday 24h.
    #   However, one of those bounding values won't be labeled as shown in the
    # diagram above.  Either:
    # - Monday 0h is labeled as Sunday 24h, or
    # - Monday 24h is labeled as Tuesday 0h.
    #   In fact, the Python ``datetime`` class takes the second option.
    # Therefore, in order to find the energy use on Monday, the first reading
    # from Tuesday has to be included in the integration.
    #
    # Notes - interpolating at date transitions:
    #
    #   If data do not fall exactly on the day transition, some interpolation
    # is needed.  Suppose data are reported every six hours as shown:
    # power ->  1   1  ----  1   1
    # time  -> 14  20  24/0  2   8
    # day   ->  M   M   M/T  T   T
    #   Let XX represent the cumulative energy consumption up to Monday 20h.
    # Then the cumulative consumption up to Tuesday 2h is XX + 6 kW.h.
    # Interpolating 4/6 of the way through the interval, the cumulative
    # consumption up to Monday 24h is XX + 4 kW.h.
    #
    # Notes - handling last date available:
    #
    #   Because ``datetime`` objects label midnight as time 0 of the day
    # just starting, treat the date of the last entry in *datesClean* as the
    # the date that starts a month.
    #   Consider the case that the last entry in *datesClean* is at exactly
    # midnight (say, on 9-September).  Then the data support treating a month as
    # starting on 9-September and running through 8-August.
    #   If, on the other hand, the last entry in *datesClean* is sometime
    # in the middle of the day (say, at 2pm on 9-September), then there are not
    # enough data to say a month runs from 9-September through 10-August.
    # Again, the first day of each month is 9-September.
    #
    # Notes - variable names.
    #
    #   Variable names for dates use the following conventions:
    # - Actual dates, which correspond to ``datetime`` or ``date`` entries
    #   in *datesClean*, have names like *currMonthStartDate* and *currMonthEndDate*.
    #   These may also have an associated index into *datesClean*, named like
    #   *currMonthStartIdx* and *currMonthEndIdx*.
    # - Theoretical dates, which define when a month begins and ends, have names
    #   like *currMonthStartsOn*.
    #
    # Initialize.
    monthlyEnergies = list()
    #
    # Last date in *datesClean* starts a month (because either it marks midnight
    # of the day before, or it has incomplete data).
    nextMonthStartIdx = len(loadsClean) - 1
    if( nextMonthStartIdx <= 0 ):
        return( monthlyEnergies )
    nextMonthStartsOn = datesClean[nextMonthStartIdx]
    #
    # Find the exact date transition if necessary.
    if( type(datesClean[0]) == dto.datetime ):
        #
        # Here, *nextMonthStartsOn* has time information.
        #   Coerce it to be a pure ``date``, and adjust *nextMonthStartIdx* to
        # mark the earliest ``datetime`` in *datesClean* with this date.
        nextMonthStartsOn = dto.datetime(nextMonthStartsOn.year, nextMonthStartsOn.month, nextMonthStartsOn.day, 0)
        nextMonthStartIdx = dtutil.findLatestEntryBefore(datesClean, nextMonthStartsOn, startIdx=0, blockIdx=nextMonthStartIdx+1) + 1
    #
    # Step backward through *loadsClean*, summarizing months.
    while( True ):
        #
        # Here, assume:
        # - *nextMonthStartsOn* gives the first date of the month after the month
        #   of interest.  Note that, due to missing data, *datesClean* might
        #   not have a matching date.
        # - *nextMonthStartsOn* has the same type as entries in *datesClean*.
        # - *nextMonthStartIdx* marks the first entry in *datesClean* that can
        #   belong to the year after the year of interest.
        #
        # Figure out range of data to integrate.
        currMonthStartsOn = dtutil.goBackMonths(nextMonthStartsOn,monthCt)
        prevMonthEndIdx = dtutil.findLatestEntryBefore(datesClean, currMonthStartsOn, startIdx=0, blockIdx=nextMonthStartIdx)
        #
        # Check that data spans a full year, or close to it.
        if( prevMonthEndIdx == 0 ):
            earliestDateAvailable = datesClean[0]
            missingDayCt = (earliestDateAvailable - currMonthStartsOn).total_seconds() * __DAY_PER_SEC
            if( missingDayCt > 3 ):
                break
        #
        # Here:
        # - *prevMonthEndIdx* marks the entry that spans the transition from the
        #   previous year, if one exists, to the current year.
        # - *nextMonthStartIdx* marks the entry that spans the transition to the
        #   next year.
        #
        # Find energy use for the current year.
        #   Note have to "block" on ``nextMonthStartIdx + 1`` because have to
        # integrate up to the point at *nextMonthStartIdx*.
        monthlyEnergy = __integratePtsInTime(loadsClean, datesClean, startIdx=prevMonthEndIdx, blockIdx=nextMonthStartIdx+1)
        #
        # Adjust *monthlyEnergy* for the transition from previous year to current year.
        sec_excess = (currMonthStartsOn - datesClean[prevMonthEndIdx]).total_seconds()
        if( sec_excess > 0 ):
            # Excess energy is a fraction (sec_excess/sec_total) of the total
            # energy in the first bin.  Total energy in the first bin is
            # proportional to sec_total, so sec_total cancels out.
            removeEnergy = 0.5*(loadsClean[prevMonthEndIdx] + loadsClean[prevMonthEndIdx+1]) * sec_excess / 3600.
            monthlyEnergy -= removeEnergy
        #
        # Adjust *monthlyEnergy* for the transition from current year to next year.
        sec_excess = (datesClean[nextMonthStartIdx] - nextMonthStartsOn).total_seconds()
        if( sec_excess > 0 ):
            removeEnergy = 0.5*(loadsClean[nextMonthStartIdx-1] + loadsClean[nextMonthStartIdx]) * sec_excess / 3600.
            monthlyEnergy -= removeEnergy
        #
        # Save result.
        monthlyEnergies.append(( monthlyEnergy, 
                               currMonthStartsOn, 
                               datesClean[nextMonthStartIdx-1] ))
        #
        # Prepare for next iteration.
        if( prevMonthEndIdx == 0 ):
            break
        nextMonthStartsOn = currMonthStartsOn
        nextMonthStartIdx = prevMonthEndIdx + 1
    #
    # Here, *monthlyEnergies* has desired values, but in the wrong order (since
    # worked backward through months, but want most recent year at end of list).
    monthlyEnergies.reverse()
    #
    return( monthlyEnergies )
    #
    # End :func:`calc_monthly_energy`.
    
    
def __integratePtsInTime(loads, datetimes, startIdx=0, blockIdx=None):
    """
    Uses numerical integration to determine the total energy use in the given interval.

    **Args:**

    - *loads*, array-like sequence of power data (float).
    - *datetimes*, array-like sequence of ``datetime`` objects.

    **Notes:**
    - When used to calculate energy use, the interval is calculated in hours.
    """

    assert (len(loads) == len(datetimes))
    #
    # TODO: Consider rewriting this fcn to handle integration directly, via a
    # trapezoidal integration, rather than passing off to Simpson's rule.
    #   A few reasons to do so:
    # - Already stepping through the indices in order to assemble the vectors
    #   that Simpson's rule expects.  So may as well just calculate the results,
    #   and hence save forming the new vectors.
    # - Doing so will remove need to "clean" the data before passing them in
    #   here.  Can just skip ``NAN`` and ``Inf`` values as process.  This saves
    #   yet another round of copying vectors into new memory.
    # - No particular reason to believe, given the coarseness of building energy
    #   data and the swiftness of mode transitions in buildings, that Simpson's
    #   rule gives a better estimate of energy than trapezoidal integration.
    #   And the nice thing about trap integration is that it uses the same rule
    #   by which interpolate the returned results.  That means, can just do the
    #   interpolation in the re-written routine, and hence make the major loop
    #   in fcn calc_annual_energy() a lot cleaner.
    # - The rewritten routine can move into a more general "integrate-data"
    #   module, along with Simpson's, to be available for other uses.
    #
    # Initialize.
    if (blockIdx == None):
        blockIdx = len(loads)
    timesInHours = list()
    valueInHours = list()
    # Convert the datetimes to corresponding hours

    for items in range(startIdx, blockIdx):
        assert( not math.isnan(loads[items]) )
        #
        timesInHours.append( (datetimes[items] - datetimes[0]).total_seconds() / 3600.)
        valueInHours.append(loads[items])

    valuesInt = simp.simpsons(valueInHours, timesInHours)
    return ( valuesInt )
    #
    # End :func:`__integratePtsInTime`.
