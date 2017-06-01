"""Calculate basic statistics for a dataset."""


#--- Provide access.
#
import numpy as np
import math as mt


def gridStats(values, user_axis):
    """
    Given a matrix, calculate the statistics for each row or column, ignoring
    ``NAN`` values.

    **Args:**

    - *values*, array-like sequence of values.
    - *user_axis*, direction the statistics are calculated (string).
      ``user_axis='c'``: calculate for each column.
      ``user_axis='r'``: calculate for each row.

    **Returns:**

    - *statDict*, a dictionary of statistics.  For a key such as 'mean', the
      value is an array giving the mean for each row (or column).

    **Notes:**

    - The 'peak95' is the 95th percentile of the data (not the maximum).
    - Similarly, the 'base5' is the 5th percentile of the data (not the minimum).
    - Interpolation may be used, especially for small data sets.  This means the
      values reported as peak and base may not actually exist in the data set.
    - "Array-like" means list, tuple, numpy array, etc.
    """
    #
    if (user_axis[0] == 'c' or user_axis[0] == 'C'):
        axisnum = 0
    else:
        axisnum = 1
    #
    # Mask off ``NANs``, to remove them from analysis.
    dtGrid = np.ma.masked_array(values,np.isnan(values))
    #
    statDict = dict()
    statDict['mean'] = dtGrid.mean(axis=axisnum)
    statDict['stdev'] = dtGrid.std(axis=axisnum)
    #
    # Fill in ``NAN`` entries with the mean, in order to keep :func:`numpy.percentile`
    # from returning ``NAN``.
    dtGrid = dtGrid.filled(dtGrid.mean())
    statDict['max'] = np.max(dtGrid)
    statDict['min'] = np.min(dtGrid)
    statDict['peak95'] = np.percentile(dtGrid,95,axis=axisnum)
    statDict['base5'] = np.percentile(dtGrid,5,axis=axisnum)
    statDict['bpratio'] = np.ma.masked_invalid( np.divide(statDict['base5'],statDict['peak95']) )
    statDict['range95_5'] = np.ma.masked_invalid( np.subtract(statDict['peak95'],statDict['base5']) )
    #
    return( statDict )
    #
    # End :func:`gridStats`.


def findSpearmanRank(xValues, yValues):
    """
    Given two arrays, find the Spearman rank correlation coefficient.

    **Args:**

    - *xValues* and *yValues*, array-like sequences of values.

    **Returns:**

    - *spearmanCoeff*, the Spearman rank correlation coefficient between the arrays.

    **Notes:**

    - To calculate weather sensitivity, *xValues* are outside air temperatures and
      the *yValues* are the corresponding demand for the given time interval.
    - Missing (or corrupt) values should be coded as ``NAN``.  Any entry for which
      :func:`numpy.isnan` returns ``True`` will be excluded from the analysis.
    - "Array-like" means list, tuple, numpy array, etc.

    **Enhancements:**

    - Allow the use of filters, e.g., to analyze only data recorded at certain
      hours of the day, only from weekdays, etc.
    """
    #
    # Check inputs.
    valCt = len(xValues)
    assert( valCt > 1 )
    assert( len(yValues) == valCt )
    #
    # Require numpy arrays with floating-point numbers.
    if( type(xValues)!=np.ndarray or isinstance(xValues[0],int) ):
        xValues = np.array(xValues, dtype=np.float)
    if( type(yValues)!=np.ndarray or isinstance(yValues[0],int) ):
        yValues = np.array(yValues, dtype=np.float)
    #
    # Exclude all (x,y) pairs for which either *xValues* or *yValues* has a
    # ``NAN`` entry.
    #   Rationale: suppose *xValues* represents the outside air temperature,
    # and *yValues* represents demand.  If missing an OAT observation, don't
    # want to penalize the fact that do have a demand measurement.  Therefore
    # need to exclude all pairs where at least one has ``NAN`` values.
    #   Note do this before find the ranks.
    nanLocs = np.logical_or(
        np.ma.masked_invalid(xValues).mask,
        np.ma.masked_invalid(yValues).mask
        )
    nanCt = np.count_nonzero(nanLocs)
    if( nanCt == valCt ):
        # Here, pathological case of no good pairs.
        return( 0 )
    elif( nanCt > 0 ):
        # Mark ``NAN`` in all pairs where one of the rows has a ``NAN``.
        xValues[nanLocs] = float('nan')
        yValues[nanLocs] = float('nan')
    #
    # Rank the values.
    #   Note ``NAN`` mapped to rank 0.
    xRanks = __rankForSpearman(xValues)
    yRanks = __rankForSpearman(yValues)
    #
    # Subtract out mean rank, so each resulting vector has mean of zero.
    #   When finding mean, exclude all (x,y) pairs for which either *xValues*
    # or *yValues* is ``NAN``.
    if( nanCt == 0 ):
        # Here, no ``NAN`` values.
        xRanksZeroMean = xRanks - xRanks.mean()
        yRanksZeroMean = yRanks - yRanks.mean()
    else:
        # Here, need to subtract out the mean of the non-``NAN`` entries, and
        # end up with an array for which an inner product does not get any
        # contribution from the ``NAN`` entries.
        #   A natural way to do this should be using "masked arrays".  However,
        # in tests, :func:`numpy.inner` and :func:`numpy.dot` did not seem to
        # handle masked arrays gracefully.  Specifically, they sometimes gave
        # wrong values, and no pattern was apparent as to what conditions
        # triggered the problem.
        #   Therefore the strategy here is to explicitly set the rank of
        # entries with ``NAN`` values to zero (this was done above), then to
        # find the mean by dividing the sum of entries by the appropriate count
        # of non-``NAN`` entries.  Finally, after subtracting that mean, re-set
        # the rank of ``NAN`` entries to zero, so that they don't contribute
        # anything to inner products.
        #
        valCt -= nanCt
        #
        xRanksZeroMean = xRanks - xRanks.sum()/valCt
        xRanksZeroMean[nanLocs] = 0
        #
        yRanksZeroMean = yRanks - yRanks.sum()/valCt
        yRanksZeroMean[nanLocs] = 0
    #
    # Find Spearman rank correlation coefficient.
    spearmanCoeff = np.inner(xRanksZeroMean, yRanksZeroMean) / np.sqrt(
        np.inner(xRanksZeroMean,xRanksZeroMean) * np.inner(yRanksZeroMean,yRanksZeroMean)
        )
    #
    return( spearmanCoeff )
    #
    # End :func:`findSpearmanRank`.


def pearson_coeff(xValues, yValues):
    """
    Given two arrays, find the Pearson correlation coefficient.

    **Args:**

    - *xValues* and *yValues*, array-like sequences of values.

    **Returns:**

    - *pearsonCoeff*, the Pearson correlation coefficient between the arrays.

    **Notes:**

    - To calculate weather sensitivity, *xValues* are outside air temperatures and
      the *yValues* are the corresponding the demand for the given time interval.
    - Missing (or corrupt) values should be coded as ``NAN``.  Any entry for which
      :func:`numpy.isnan` returns ``True`` will be excluded from the analysis.
    - "Array-like" means list, tuple, numpy array, etc.
    """
    #
    # TODO: Both here and for :func:`findSpearmanRank`, need code to detect
    # divide-by-zero error that occurs when all points in a vector are the
    # same.  Probably should just return 0 for those cases, but need to check
    # to see what is standard practice.
    #
    # Check inputs.
    assert( len(xValues) == len(yValues) )
    #
    xxZeroMean = xValues - np.mean(xValues)
    yyZeroMean = yValues - np.mean(yValues)
    #
    # Find Pearson correlation coefficient.
    pearsonCoeff = np.inner(xxZeroMean, yyZeroMean) / np.sqrt(
        np.inner(xxZeroMean,xxZeroMean) * np.inner(yyZeroMean,yyZeroMean)
        )
    #
    return( pearsonCoeff )
    #
    # End :func:`pearson_coeff`.


def variability(values):
    """
    Calculate the average variability of a matrix.

    **Args:**

    - *values*, array-like sequence of values.

    **Notes:**

    - To calculate load variability, fold values to give one day per row, and
      hour-of-the-day in each column.
    - "Array-like" means list, tuple, numpy array, etc.
    """

    deviation = list()
    dtGrid = np.ma.masked_array(values,np.isnan(values))

    # Calculates the mean value for each column
    # for load variability, rowCt should in days
    # colCt should be hours

    colMeans = dtGrid.mean(axis=0)
    stdev = np.std(dtGrid,axis=0,ddof=1)

    # Normalize this number by dividing it by x_av. This gives a var estimate for each hour
    # Then take these and do a simple average over hours of operation (or peak hours) to get an estimate for the building

    return ( np.mean(np.divide(stdev,colMeans)) )
    #
    # End :func:`variability`.


def __rankForSpearman(values):
    """
    Find the ranks of a vector *values*, as defined for Spearman rank correlation coefficient.

    **Notes:**

    - Rank smallest to largest.
    - Equal values get mean rank.
    - ``NAN`` gets a rank of 0.
    """
    #
    assert( type(values) == np.ndarray )
    assert( values.ndim == 1 )
    #
    # Initialize.
    valCt = len(values)
    #
    # Find indices that would sort *values*.
    #   Example:
    # - values       = [1, 2, 5, 4, 3]
    # - srtdToActIdx = [0, 1, 4, 3, 2]
    #   Note that :func:`numpy.argsort` sorts ``NAN`` as highest.
    srtdToActIdx = np.argsort(values)
    #
    # Initialize *ranks* to treat values as ``NAN`` by default.
    ranks = np.zeros(valCt)
    #
    # Step through *values* in sorted order, assigning ranks.
    lastVal = values[srtdToActIdx[0]]
    startRunIdx = 0
    currIdx = 1
    while( currIdx < valCt ):
        #
        currVal = values[srtdToActIdx[currIdx]]
        if( np.isnan(currVal) ):
            # No need to continue-- uninspected entries already have rank 0.
            break
        #
        # Assign ranks if *currVal* breaks a run of equal entries.
        if( currVal > lastVal ):
            # Here, indices *startRunIdx* to *currIdx*-1, inclusive, all had
            # the same value (*lastVal*).
            #   Their "natural" ranks are *startRunIdx*+1 to *currIdx*,
            # inclusive.  Assign all the indices the mean rank.
            #   Examples:
            # - startRunIdx=0, currIdx=1 ==> mean(1) ==> meanRank=1
            # - startRunIdx=0, currIdx=2 ==> mean(1,2) ==> meanRank=1.5
            # - startRunIdx=0, currIdx=5 ==> mean(1,2,3,4,5) ==> meanRank=3
            # - startRunIdx=1, currIdx=2 ==> mean(2) ==> meanRank=2
            # - startRunIdx=1, currIdx=4 ==> mean(2,3,4) ==> meanRank=3
            # - startRunIdx=1, currIdx=5 ==> mean(2,3,4,5) ==> meanRank=3.5
            # - startRunIdx=1, currIdx=6 ==> mean(2,3,4,5,6) ==> meanRank=4
            meanRank = 0.5 * (startRunIdx + currIdx + 1)
            while( startRunIdx < currIdx ):
                # Note that ``srtdToActIdx[startRunIdx]`` gives an index for
                # which *values* equals *lastVal*.
                ranks[srtdToActIdx[startRunIdx]] = meanRank
                startRunIdx += 1
            # Mark start of a new run.
            #   Note already have ``startRunIdx == currIdx``.
            lastVal = currVal
        #
        # Prepare for next iteration.
        currIdx += 1
    #
    # Here, still need to assign ranks for last entries inspected.
    #   This code should exactly copy that in the loop above.  There are ways
    # around this ugly duplication, but they are themselves ugly.
    meanRank = 0.5 * (startRunIdx + currIdx + 1)
    while( startRunIdx < currIdx ):
        ranks[srtdToActIdx[startRunIdx]] = meanRank
        startRunIdx += 1
    #
    # Here, *ranks* holds ranks, between 1 and *currIdx*, inclusive, for all
    # the non-``NAN`` entries in *values*.
    #   If *values* has no ``NAN`` entries, then *currIdx* == *valCt*.
    # Otherwise, *currIdx* < *valCt*.
    #   All ``NAN`` entries in *values* should have a rank of 0.
    #
    return( ranks )
    #
    # End :func:`__rankForSpearman`.
