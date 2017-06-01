"""Utilities for working with :class:`datetime` and :class:`date` objects."""


#--- Provide access.
#
import datetime as dto


def findLatestEntryBefore(datetimes, tCut, startIdx=None, blockIdx=None):
    """
    Find the latest entry in *datetimes* that falls before *tCut*.

    **Args:**

    - *datetimes*, array-like sequence of times (:class:`date` or :class:`datetime`).
    - *tCut*, time to bound from below (same type as *datetimes*).
    - *startIdx*, first index (inclusive) to consider in *datetimes*.
      Defaults to 0 (i.e., consider first entry).
    - *blockIdx*, last index (exclusive) to consider in *datetimes*.
      Defaults to ``len(datetimes)`` (i.e., consider last entry).

    **Returns:**

    - *beforeIdx*, largest index such that ``startIdx <= beforeIdx < blockIdx``,
      and such that ``datetimes[beforeIdx]`` falls before *tCut*.

    **Notes:**

    - *datetimes* must be monotone increasing.
    - Every entry in *datetimes* must have the same type, i.e., either all
      :class:``date`` or all :class:``datetime``.
    - If *tCut* falls before ``datetimes[startIdx]``, it is not possible to
      find a meaningful result.  In this case, return the closest permitted
      index.

    **Enhancements:**

    - If *datetimes* are evenly spaced, can find desired index directly.  And even
      if only nearly-evenly spaced, may still be able to find it faster than via
      bisection.  Consider rewrite to first assume even spacing, and to use
      bisection only if that assumption fails.
    """
    #
    # Check inputs.
    dtCt = len(datetimes)
    assert( isinstance(datetimes[0],dto.date) )
    assert( type(tCut) == type(datetimes[0]) )
    if( startIdx is None ):
        startIdx = 0
    assert( startIdx >= 0 )
    if( blockIdx is None ):
        blockIdx = dtCt
    assert( blockIdx <= dtCt )
    assert( startIdx < blockIdx )
    #
    # Convenience constants.
    cutYear  = tCut.year
    cutMonth = tCut.month
    cutDay   = tCut.day
    haveDateOnly = ( type(datetimes[0]) == dto.date )
    #
    # Find the latest entry before *tCut*.
    #    That is, assume *datetimes* are in order, and find the largest
    # *beforeIdx* such that ``datetimes[beforeIdx]`` comes before *tCut*.
    #   Use a bisection search.
    #   First point to test is just before *blockIdx*, because need to know if
    # that comes before *tCut*.
    beforeIdx = startIdx
    afterOrOnIdx = blockIdx - 1
    testIdx = afterOrOnIdx
    while( True ):
        #
        # Here, assume:
        # - *testIdx* has a valid candidate index.
        # - beforeIdx <= testIdx <= afterOrOnIdx.  In general, expect inequality,
        #   but inequality possible when begin and finish search.
        #
        tTest = datetimes[testIdx]
        #
        # Test using attributes as long as possible, then switch to finding a
        # :class:`timedelta` object, and calling methods on it.
        testYear = tTest.year
        if( testYear < cutYear ):
            beforeIdx = testIdx
        elif( testYear > cutYear ):
            afterOrOnIdx = testIdx
        else:
            testMonth = tTest.month
            if( testMonth < cutMonth ):
                beforeIdx = testIdx
            elif( testMonth > cutMonth ):
                afterOrOnIdx = testIdx
            else:
                testDay = tTest.day
                if( testDay < cutDay ):
                    beforeIdx = testIdx
                elif( testDay>cutDay or haveDateOnly ):
                    afterOrOnIdx = testIdx
                else:
                    # Here, have time information (i.e., :class:`datetime` object),
                    # and year, month, and day are equal.
                    delta = (tCut - tTest).total_seconds()
                    if( delta > 0 ):
                        beforeIdx = testIdx
                    else:
                        afterOrOnIdx = testIdx
        #
        # Here, just updated either *beforeIdx* or *afterOrOnIdx*, tightening
        # the bound on the latest *datetime* entry before *tCut*.
        if( afterOrOnIdx - beforeIdx <= 1 ):
            break
        #
        # Prepare for next iteration.
        testIdx = (beforeIdx + afterOrOnIdx) / 2
    #
    # Here, *beforeIdx* and *afterOrOnIdx* bound *tCut*, provided it fell
    # within the original bounds.
    #
    return( beforeIdx )
    #
    # End :func:`findLatestEntryBefore`.


def goBackOneYear(currDate):
    """
    Find the date-time that is the equivalent of *currDate*, but a year before.

    **Args:**

    - *currDate*, a ``datetime`` or ``date`` object.

    **Returns:**

    - *sameDatePrevYear*, an` object that is a year back, in terms of the month
      and day, from *currDate*.

    **Notes:**

    - *sameDatePrevYear* has the same class as *currDate*.
    - If *currDate* has time information (i.e., if it is type ``datetime``),
      then *sameDatePrevYear* also will be of type ``datetime``.  However, it
      will have the time information (hour, minute, and so on) set to 0.
    - When stepping back over a year that includes a leap day, don't count that
      leap day as "one day of a 365-day year".  Rather, count it as "one day of
      a 366-day year".  Thus, repeatedly stepping back one year from a fixed
      day (like, say 4-November) will not see the day shifting from 4-November
      when pass through leap years.
    """
    #
    # Check inputs.
    assert( isinstance(currDate,dto.date) )
    #
    targetYear = currDate.year - 1
    targetMonth = currDate.month
    targetDay = currDate.day
    #
    try:
        sameDatePrevYear = dto.date(year=targetYear, month=targetMonth, day=targetDay)
    except:
        # Here, previous year did not have this date.  Assume that's because
        # *currDate* was a leap day, and go back one day earlier in the
        # same month.
        try:
            sameDatePrevYear = dto.date(year=targetYear, month=targetMonth, day=targetDay-1)
        except:
            # Safety code; don't really expect to be here.
            sameDatePrevYear = currDate - dto.timedelta(days=365)
    #
    # Coerce to ``datetime`` if necessary.
    if( type(currDate) == dto.datetime ):
        sameDatePrevYear = dto.datetime(year=sameDatePrevYear.year, month=sameDatePrevYear.month,
            day=sameDatePrevYear.day, hour=0)
    #
    return( sameDatePrevYear )
    #
    # End :func:`goBackOneYear`.


def goBackMonths(currDate, monthCt):
    """
    Find the date-time that is the equivalent of *currDate*, but *monthCt* months before.

    **Args:**

    - *currDate*, a ``datetime`` or ``date`` object.
    - *monthCt*, number of months to go back.

    **Returns:**

    - *sameDayEarlierMonth*, an` object that is *monthCt* months back, in terms of
      the day, from *currDate*.

    **Notes:**

    - *sameDayEarlierMonth* has the same class as *currDate*.
    - If *currDate* has time information (i.e., if it is type ``datetime``),
      then *sameDayEarlierMonth* also will be of type ``datetime``.  However,
      it will have the time information (hour, minute, and so on) set to 0.
    - When stepping back over a month, only "numerical" months are considered.
      That is, stepping back over a month with 28 days counts the same as
      stepping back over a month with 31 days.  However, after reaching the
      final month, the day will be adjusted to the last day of the month,
      if necessary.  For example, stepping one month back form 31-March
      results in 28-February (or 29-February for leap-years), not 31-February.
    """
    #
    # Check inputs.
    assert( isinstance(currDate,dto.date) )
    assert( monthCt >= 0 )
    #
    targetYear = currDate.year
    targetMonth = currDate.month - monthCt
    targetDay = currDate.day
    #
    # For both :class:`date` and :class:`datetime`, ``month`` runs [1..12].
    while( targetMonth < 1 ):
        targetMonth += 12
        targetYear -= 1
    #
    while( True ):
        try:
            sameDayEarlierMonth = dto.date(year=targetYear, month=targetMonth, day=targetDay)
            break
        except:
            # Here, *targetMonth* does not have *targetDay*.  Assume that's
            # because transitioned to a month with fewer days.
            targetDay -= 1
            assert( targetDay > 0 )
        #
        # Here, shifted *targetDay* down by one.  Try creating the day again.
    #
    # Coerce to ``datetime`` if necessary.
    if( type(currDate) == dto.datetime ):
        sameDayEarlierMonth = dto.datetime(year=sameDayEarlierMonth.year, month=sameDayEarlierMonth.month,
            day=sameDayEarlierMonth.day, hour=0)
    #
    return( sameDayEarlierMonth )
    #
    # End :func:`goBackMonths`.
