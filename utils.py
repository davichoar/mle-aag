import numpy as np
import pandas as pd
from constants import REPLACE_COLS, FINAL_COLS
from constants import DATE_KEY, MONTH_COL, YEAR_COL

def map_columns(df):
    """
    Replace input keys in request for columns used in the pipeline.
    Return a single row df with training columns
    """
    _df = df.copy()
    _df.rename(columns=REPLACE_COLS, inplace=True)
    return _df

def get_date_parts(df):
    """
    Obtain month and year from date in request
    """
    _df = df.copy()
    _df.loc[:,MONTH_COL] = _df[DATE_KEY].apply(lambda x: x.month)
    _df.loc[:,YEAR_COL] = _df[DATE_KEY].apply(lambda x: x.year)
    _df.drop(columns=DATE_KEY,inplace=True)
    return _df
    

def format_dataframe(request):
    """
    Transform pydantic request to pandas dataframe
    """
    dict_request = request.dict()
    df = pd.json_normalize(dict_request, sep='_')
    df = map_columns(df)
    df = get_date_parts(df)
    print(df.to_dict())
    return df[FINAL_COLS]