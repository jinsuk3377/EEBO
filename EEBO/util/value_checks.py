"""Helper fcns for unit tests."""


#--- Provide access.
#
import math


def nearlySame(xxs, yys, absTol=1e-12, relTol=1e-6):
    """Compare two numbers or arrays, checking all elements are nearly equal."""
    #
    # Coerce scalar to array if necessary.
    if( not hasattr(xxs, '__iter__') ):
        xxs = [xxs]
    if( not hasattr(yys, '__iter__') ):
        yys = [yys]
    #
    # Initialize.
    lenXX = len(xxs)
    nearlySame = (len(yys) == lenXX)
    #
    idx = 0
    while( nearlySame and idx<lenXX ):
        xx = xxs[idx]
        absDiff = math.fabs(yys[idx]-xx)
        if( absDiff>absTol and absDiff>relTol*math.fabs(xx) ):
            print('Not nearly same:', xx, yys[idx], 'idx:',idx, 'absDiff:',absDiff, 'relDiff:',absDiff/math.fabs(xx))
            nearlySame = False
        #
        # Prepare for next iteration.
        idx += 1
    #
    return( nearlySame)
    #
    # End :func:`nearlySame`.
