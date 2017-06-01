"""Make tick labels with the beginning and end dates."""


#--- Provide access.
#
import datetime as dto


def ticklabel_ymd(datetimeList):
    """
    Make tick labels from datetimes, in format ``yyyy-mm-dd``, based off a list of array indices.
    
    **Args:**
    
    - *datetimeList*, list of datetime entries to be reformatted.
    
    **Returns:** 
    
    - *tickLabels*, list of datetime strings in ``yyyy-mm-dd`` format.    
    """
    #
    # Initialize
    #
    assert (datetimeList is not None)
    tickLabels = list()
    #
    for items in datetimeList:
        tickLabels.append(dto.datetime.strftime(items,'%Y-%m-%d'))
    return ( tickLabels )
    #
    # End :func:`ymd`.
    
    
def ticklabel_ym(datetimeList):
    """
    Make tick labels from datetimes, in format ``yyyy-mm``, based off a list of array indices.
    
    **Args:**
    
    - *datetimeList*, list of datetime entries to be reformatted.
    
    **Returns:** 
    
    - *tickLabels*, list of datetime strings in ``yyyy-mm`` format.    
    """
    #
    # Initialize
    #
    assert (datetimeList is not None)
    tickLabels = list()
    #
    for items in datetimeList:
        tickLabels.append(dto.datetime.strftime(items,'%Y-%m'))
    return ( tickLabels )
    #
    # End :func:`ym`.   
    
    
def ticklabel_my_slash(datetimeList):
    """
    Make tick labels from datetimes, in format ``yyyy/mm``, based off a list of array indices.
    
    **Args:**
    
    - *datetimeList*, continuous stream of datetime entries to be reformatted.
    
    **Returns:** 
    
    - *tickLabels*, list of datetime strings in ``yyyy/mm`` format.
    """
    #
    # Initialize
    #
    assert (datetimeList is not None)
    tickLabels = list()
    #
    for items in datetimeList:
        tickLabels.append(dto.datetime.strftime(items,'%m/%Y'))
    return ( tickLabels )
    #
    # End :func:`ym`.   
 
 
def ticklabel_start_end_ym(startDateList, endDateList):
    """
    Make tick labels from datetimes, in format ``start yyyy/mm-end yyyy/mm``, based off a list of starting and ending array indices.
    
    **Args:**
    
    - *startDateList*, list of datetime entries.
    - *endDateList*, list of datetime entries.  
    
    **Returns:** 
    
    - *tickLabels*, list of datetime strings in ``start yyyy/mm-end yyyy/mm`` format.
    """
    #
    # Initialize
    #
    assert (len(startDateList) == len(endDateList))
    assert (startDateList[0] < endDateList[0])
    tickLabels = list()
    valCt = len(startDateList)
    #
    start_ym = ticklabel_my_slash(startDateList)
    end_ym = ticklabel_my_slash(endDateList)
    #
    for items in range(valCt):
        tickLabels.append(start_ym[items]+'-'+end_ym[items])
    return ( tickLabels )
    #
    # End :func:`ym`.