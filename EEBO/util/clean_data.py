"""
Utilities for cleaning data, e.g., to remove ``NAN`` entries.

**Notes:**

- A number of functions in this module work with ``selector`` objects.  A
  ``selector`` accepts or rejects elements of an array.  Thus, applying a
  ``selector`` to an array results in an array with the same number, or fewer,
  of elements as the original.
- In the current implementation, a ``selector`` is a list of booleans, with
  ``True`` marking accepted elements, and ``False`` marking rejected elements.
  However, user are not expected to know this, and probably are better off
  treating ``selector`` objects as opaque.
"""


#--- Provide access.
#
import numpy as np


def makeSelector_finite(values):
    """
    Return a ``selector`` object that rejects ``NAN`` and ``Inf`` entries.

    **Args:**

    - *values*, array-like sequence of entries to inspect (float).

    **Returns:**

    - *selector*, an object that can be used with :func:`applySelector` to pull
      out, from any array of the same size, the entries corresponding to those
      accepted from *values*.
    """
    #
    # Mark for acceptance all elements of *values* that are finite (not ``NAN``
    # and not ``Inf``).
    return( map(np.isfinite, values) )
    #
    # End :func:`makeSelector_finite`.


def makeSelector_notNone(values):
    """
    Return a ``selector`` object that rejects ``None`` entries.

    **Args:**

    - *values*, array-like sequence of entries to inspect.

    **Returns:**

    - *selector*, an object that can be used with :func:`applySelector` to pull
      out, from any array of the same size, the entries corresponding to those
      accepted from *values*.
    """
    #
    # Mark for acceptance all elements of *values* that are not ``None``.
    return( map(lambda xx: xx is not None, values) )
    #
    # End :func:`makeSelector_notNone`.


def getSelectorRejectCt(selector):
    """
    Return the number of entries a ``selector`` object will reject.
    """
    #
    return( selector.count(False) )
    #
    # End :func:`getSelectorRejectCt`.


def applySelector(selector, values):
    """
    Pull out, from *values*, just the elements accepted by *selector*.

    **Args:**

    - *selector*, a ``selector`` object, as returned by, e.g.,
      :func:`makeSelector_finite` or :func:`combineSelector_narrowing`.

    - *values*, array-like sequence from which to accept or reject elements.

    **Returns:**

    - *selectedVals*, a list of accepted elements from *values*.

    **Notes:**

    - *values* must have at least as many entries as *selector* (though it may
      have more).
    """
    #
    # Check inputs.
    selectCt = len(selector)
    assert( len(values) >= selectCt )
    #
    # Accept all elements of *values* where *selector* is ``True``.
    return( [values[idx] for idx in range(selectCt) if selector[idx]] )
    #
    # End :func:`applySelector`.


def combineSelector_narrowing(*selectors):
    """
    Return a ``selector`` object that accepts only elements that all inputs accept.

    **Args:**

    - A comma-separated list of ``selector`` objects.

    **Returns:**

    - *narrowSelector*, a ``selector`` object that only accepts an element of
      an array if every input ``selector`` object accepts that element.  Called
      "narrowing" because it will never accept more elements than the most
      stringent of the inputs.

    **Notes:**

    - Each ``selector`` object in *selectors* must refer to the same length of
      array.  That is, the total number of elements that each can accept or reject
      must be the same.
    """
    #
    # Check inputs.
    selectorCt = len(selectors)  # Number of selectors to process.
    assert( selectorCt > 0 )
    selectCt = len(selectors[0])  # Number of entries in each selector.
    for selIdx in range(1, selectorCt):
        assert( len(selectors[selIdx]) == selectCt )
    #
    # Create a new selector (to avoid mutating the first input).
    narrowSelector = list(selectors[0])
    #
    for selIdx in range(1, selectorCt):
        # Accept only elements where both selectors agree.
        #   Strategy: zip *narrowSelector* with next selector, to give a list of
        # tuples of the corresonding elements.  Map a function over that list.
        # The function takes a tuple and returns ``True`` if both elements in
        # the tuple are ``True``.
        narrowSelector = map(lambda boolTuple: boolTuple[0] and boolTuple[1], zip(narrowSelector, selectors[selIdx]))
        #
        # TODO: There must be a "functional" way to run over all the inputs at once.
    #
    return( narrowSelector )
    #
    # End :func:`combineSelector_narrowing`.


def interpolateBadEntries_linear(values, runCtMax=1, times=None):
    """
    Replace bad entries in an array, using linear interpolation.

    **Args:**

    - *values*, array-like sequence of values in which to replace bad entries
      (float).
    - *runCtMax*, maximum number of bad entries in a row to replace.  If more
      than *runCtMax* entries in a row are bad, leave them alone.
    - *times*, optional array-like sequence of times to use as basis for
      linearization (float).

    **Returns:**

    - *cleanedVals*, numpy array of *values*, but with runs of up to
      *runCtMax* bad entries replaced.

    **Notes:**

    - Bad entries are as tested by :func:`numpy.isfinite`.  This identifies
      ``NAN`` (not-a-number) and ``Inf`` (positive or negative infinity)
      entries as bad.
    - Always returns a copy of *values*.  Thus, the caller may freely mutate
      *cleanedVals* without fear of affecting the data in *values*.
    - Where linear interpolation is not possible (at the beginning and end of
      *values*), replace bad entries with the outermost good entry from *values*.
    - If *times* is ``None``, the linearization assumes that the indices into
      *values* are evenly spaced in some sense.
    - If *times* are given, the linearization assumes the entries in *values*
      are samples at the given times.
    """
    #
    # Check inputs.
    assert( hasattr(values, '__iter__') )
    valCt = len(values)
    if( times is not None ):
        assert( len(times) == valCt )
    #
    # Protect caller's data from mutation.
    #   Also, convert ints to floats if necessary.
    cleanedVals = np.array(values, dtype=float)
    #
    # Run through *cleanedVals* looking for bad entries.
    checkIdx = 0
    while( True ):
        #
        # Here, assume *checkIdx* has index of the next entry in *cleanedVals*
        # to inspect.
        while( checkIdx<valCt and np.isfinite(cleanedVals[checkIdx]) ):
            checkIdx += 1
        if( checkIdx >= valCt ):
            break
        #
        # Here, *checkIdx* marks a bad entry.
        firstBadIdxInRun = checkIdx
        while( checkIdx<valCt and not np.isfinite(cleanedVals[checkIdx]) ):
            checkIdx += 1
        #
        # Here, *checkIdx* marks a good entry, or reached end of array.  Have
        # a run of consecutive bad indices into *cleanedVals*.  The run begins
        # at *firstBadIdxInRun*, and ends at index ``checkIdx - 1``, inclusive.
        runCt = checkIdx - firstBadIdxInRun
        if( runCt <= runCtMax ):
            #
            # Here, replace bad entries in *cleanedVals*.
            if( firstBadIdxInRun==0 and checkIdx<valCt ):
                fillVal = cleanedVals[checkIdx]
                __replaceConst(cleanedVals, firstBadIdxInRun, checkIdx, fillVal)
            elif( firstBadIdxInRun>0 and checkIdx>=valCt ):
                fillVal = cleanedVals[firstBadIdxInRun-1]
                __replaceConst(cleanedVals, firstBadIdxInRun, checkIdx, fillVal)
            elif( firstBadIdxInRun>0 and checkIdx<valCt ):
                goodIdxLeft = firstBadIdxInRun - 1
                if( times is None ):
                    __replaceLin_equispaced(cleanedVals, goodIdxLeft, checkIdx)
                else:
                    __replaceLin_times(cleanedVals, goodIdxLeft, checkIdx, times)
            #
            # Here, done replacing this run of bad entries.
            #   Note there's a chance that no replacement was made, if entire
            # array is bad.
        #
        # Here, *checkIdx* marks a good entry in *cleanedVals*, that terminates
        # a run of bad entries in *values*.  That run may or may not have been
        # cleaned up in *cleanedVals*.
        #
        # Prepare to continue search.
        checkIdx += 1
    #
    # Here, filled in bad indices by linear interpolation where possible.
    #
    return( cleanedVals )
    #
    # End :func:`interpolateBadEntries_linear`.


def __replaceConst(values, startIdx, blockIdx, newVal):
    """
    Replace entries in *values*, from indices *startIdx* (inclusive) through
    *blockIdx* (exclusive), with a constant *newVal*.  Mutate *values*.
    """
    #
    # Check inputs.
    valCt = len(values)
    assert( type(values) == np.ndarray )
    assert( values.ndim == 1 )
    assert( startIdx >= 0 )
    assert( blockIdx <= valCt )
    assert( startIdx < blockIdx )
    #
    values[startIdx:blockIdx] = newVal
    #
    # End :func:`__replaceConst`.


def __replaceLin_equispaced(values, goodIdxLeft, goodIdxRight):
    """
    Replace entries in *values*, from indices ``goodIdxLeft+1`` through
    ``goodIdxRight-1`` inclusive, with points on a line between the
    points ``(goodIndexLeft, values[goodIndexLeft])`` and
    ``(goodIndexRight, values[goodIndexRight])``.  Assume the indices are
    evenly spaced.
    """
    #
    # Check inputs.
    valCt = len(values)
    assert( type(values) == np.ndarray )
    assert( values.dtype == float )  # np.issubdtype(values.dtype, float)?
    assert( values.ndim == 1 )
    assert( goodIdxLeft >= 0 )
    assert( goodIdxRight < valCt )
    assert( goodIdxLeft+1 < goodIdxRight )
    #
    replaceCt = goodIdxRight - goodIdxLeft + 1  # Includes good indices.
    values[goodIdxLeft:goodIdxRight+1] =  \
        np.linspace(values[goodIdxLeft], values[goodIdxRight], replaceCt)
    #
    # End :func:`__replaceLin_equispaced`.


def __replaceLin_times(values, goodIdxLeft, goodIdxRight, times):
    """
    Replace entries in *values*, from indices ``goodIdxLeft+1`` through
    ``goodIdxRight-1`` inclusive, with points on a line between the
    points ``(times[goodIndexLeft], values[goodIndexLeft])`` and
    ``(times[goodIndexRight], values[goodIndexRight])``.  Assume the indices
    are spaced according to the values in *times*.
    """
    #
    # Check inputs.
    valCt = len(values)
    assert( type(values) == np.ndarray )
    assert( values.dtype == float )  # np.issubdtype(values.dtype, float)?
    assert( values.ndim == 1 )
    assert( goodIdxLeft >= 0 )
    assert( goodIdxRight < valCt )
    assert( goodIdxLeft+1 < goodIdxRight )
    assert( len(times) == valCt )
    # Not checked: entries in *times* are monotone increasing.
    #
    startVal = values[goodIdxLeft]
    startTime = times[goodIdxLeft]
    #
    slope = (float(values[goodIdxRight]) - startVal) / (times[goodIdxRight] - startTime)
    #
    for idx in xrange(goodIdxLeft+1, goodIdxRight):
        newVal = startVal + slope*(times[idx] - startTime)
        values[idx] = newVal
    #
    # End :func:`__replaceLin_times`.
