"""Integrate a set of values using Simpson's rule."""


#--- Provide access.
#
import numpy as np
from scipy import integrate


def simpsons(values, times=None, interval=1.0):
    """
    Find the time-integral of a set of values, using composite Simpson's rule.

    **Args:**

    - *values*, array-like sequence of values to integrate (float).
    - *times*, array-like sequence of times at which *values* were sampled (float).
    - *interval*, spacing of points in time (float).

    **Returns:**

    - *timeIntegral*, estimated time-integral of *values*.

    **Raises:**

    - For ``NAN`` entries in *values*.

    **Notes:**

    - If given, *times* is used to determine the sample spacing.  Otherwise,
      *interval* is used.
    - In *times*, only differences between entries matter.  That is, shifting
      all *times* up or down by a constant amount does not alter the results.
    - Assume *times* contains monotone-increasing entries, and no missing entries.
    - The estimated solution is fourth-order in the interval.  For example,
      compared to one-hour samples, providing fifteen-minute samples should
      reduce the error by a factor of about (1/4)^4 = 1/256.
    """
    #
    # Note do not allow ``NAN`` entries in *values*, because they make the
    # Simpson's integrator return ``NAN`` (even using masked arrays).
    #
    # Check inputs.
    valCt = len(values)
    assert( valCt >= 2 )
    if( times is None ):
        assert( interval > 0 )
    else:
        assert( len(times) == valCt )
    assert( not np.any(np.isnan(values)) )
    #
    if( times is None ):
        timeIntegral = integrate.simps(values, dx=interval)
    else:
        timeIntegral = integrate.simps(values, times)
    #
    return( timeIntegral )
    #
    # End :func:`simpsons`.
