import pandas as pd
import numpy as np
from functools import partial

def sample_id_hists(df, id_col, additional_sort_col=None, sort=True, **kwargs):
    """
    Generate subsample of complete histories from a dataframe that contains mutiple entries for IDs. 
    
    Args:
        df: pandas dataframe
        id_col: name of column containing ids
        additional_sort_col: name of additional column to use to sort after ids, e.g. 'date'
        sort: boolean, if the results should be sorted by id and additional_sort_col
        kwargs: arguments of pd.Series.sample() to use for sampling ids e.g. frac=0.1, n=1
        
    Returns:
        dataframe containing subset of rows from df
        """
    
    ids = pd.Series(df[id_col].unique())
    sorts = [id_col]
    if additional_sort_col is not None:
        sorts.append(additional_sort_col)
    if sort:
        return (df[df[id_col].isin(ids.sample(**kwargs))]
                             .sort_values(by=sorts)
                             .copy())
    else:
        return df[df[id_col].isin(ids.sample(**kwargs))].copy()


def offset_from_first_event(group, date_col, event_col, event, period, find):
    "Helper function for event_delta()"
    def return_offset_date(loc):
        return (group[group[event_col] == event][date_col]
                                                .iloc[loc]
                                                .to_period(period))
    
    group = group.sort_values(date_col)
    if event in group[event_col].values:
        if find == 'first':
            event_date_to_offset = return_offset_date(0)
        if find == 'last':
            event_date_to_offset = return_offset_date(-1)
        group[event_col+'_delta'] = group[date_col].dt.to_period(period) - event_date_to_offset
    else:
        group[event_col+'_delta'] = np.NaN
    return group


def event_delta(df, groupby_col, date_col, event_col, event=True, period='D', find='first'):
    """
    Calculate offset from first or last event of a specifed type for each IDs history.
    
    Args:
        df: pandas dataframe
        groupby_col: name of column to use for groups e.g. 'id'
        date_col: name of column containing time for offset
        event_col: name of column containing events of interest
        event: type of cell contents to look for, default is True
        period: string for pd.Series.dt offset alias, e.g. 'M' for months, 'D' for calendar days
        find: 'first' or 'last' to return offset from first or last occurence of event respectively
        
    Returns:
        original pandas dataframe with new column 'event_col_delta' appended
        """
    
    if event not in df[event_col].values:
        raise ValueError('No records contain event, will return NaN for every row.')        
    
    partial_offset_func = partial(offset_from_first_event,
                                  date_col=date_col, 
                                  event_col=event_col, 
                                  event=event, 
                                  period=period,
                                  find=find)
    return (df.groupby(groupby_col)
              .apply(partial_offset_func)
              .copy())
