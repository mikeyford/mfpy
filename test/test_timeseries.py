import unittest
import pandas as pd
from pandas.testing import assert_frame_equal as assert_df
import numpy as np
from mytools import timeseries


df_input = pd.DataFrame({'id': ['1.01', '1.01', '2.02', '3.03' , '3.03'],
                         'date': pd.to_datetime(['2001-02-01', '2001-01-01', 
                                                 '2001-01-01', '2001-02-01', '2001-01-01']),
                         'feature': [False, False, False, True, True]},
                          index=[0, 1, 2, 3, 4])

df_expected_false = pd.DataFrame({'id': ['1.01', '1.01', '2.02'],
                                  'date': pd.to_datetime(['2001-01-01', '2001-02-01', 
                                                          '2001-01-01']),
                                  'feature': [False, False, False]},
                                   index=[1, 0, 2])

df_expected_event_delta = pd.DataFrame({'id': ['1.01', '1.01', '2.02', '3.03' , '3.03'],
                                        'date': pd.to_datetime(['2001-01-01', '2001-02-01', '2001-01-01', 
                                                                '2001-01-01', '2001-02-01']),
                                        'feature': [False, False, False, True, True],
                                        'feature_delta': [np.NaN, np.NaN, np.NaN, 0, 1]},
                                         index=[0, 1, 2, 3, 4])


def reset_col_order(df):
    return df.sort_index(axis=1)


class TestUtilsFunctions(unittest.TestCase):
  
    def test_sample_id_hists(self):
        df_input_filtered = (df_input.groupby('id')
                                     .filter(lambda x: sum(x.feature) == 0)) 
        assert_df(reset_col_order(timeseries.sample_id_hists(df_input_filtered, id_col='id', 
                                                             additional_sort_col='date', frac=1)),
                                      reset_col_order(df_expected_false))
        
    
    def test_event_delta(self):
        assert_df(reset_col_order(timeseries.event_delta(df_input, 'id', 'date', 
                                                         'feature', period='M').reset_index(drop='id')),
                                  reset_col_order(df_expected_event_delta),
                 check_dtype=False)

        
if __name__ == '__main__':
    unittest.main()
