import numpy as np
import pandas as pd

from pipeline.config import PRECIP_PATH, CENTRAL_BANK_PATH, MILK_PRICE_PATH
from pipeline.config import PRECIP_DATE_COL, BANK_DATE_COL, DATE_FORMAT
from pipeline.config import MONTH_COL, YEAR_COL
from pipeline.config import REPLACE_MILK_COLS

import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

import logging
logger = logging.getLogger('DATA_WRANGLING')
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',)


def load_data():
    """ 
    Load all csv files into pandas DataFrame,
    cast some columns into right types
    """
    logger.info(f"Loading data from disk ...")
    # Load csvs
    precipitaciones_df = pd.read_csv(PRECIP_PATH)
    banco_central_df = pd.read_csv(CENTRAL_BANK_PATH)
    milk_price_df = pd.read_csv(MILK_PRICE_PATH)
    
    return precipitaciones_df, banco_central_df, milk_price_df

def format_data(precipitaciones_df, banco_central_df, milk_price_df):
    """
    Format columns to correct types and names
    """
    logger.info(f"Formatting datasets for date columns ...")
    # Cast datetime columns (according to jupyter nb)
    precipitaciones_df[PRECIP_DATE_COL] = pd.to_datetime(precipitaciones_df[PRECIP_DATE_COL], 
                                                         format = DATE_FORMAT)
    precipitaciones_df = precipitaciones_df.sort_values(by = PRECIP_DATE_COL, 
                                                        ascending = True).reset_index(drop = True)
    
    banco_central_df[BANK_DATE_COL] = banco_central_df[BANK_DATE_COL].apply(lambda x: x[0:10])
    banco_central_df[BANK_DATE_COL] = pd.to_datetime(banco_central_df[BANK_DATE_COL], 
                                                     format = DATE_FORMAT, 
                                                     errors = 'coerce')
    
    milk_price_df.rename(columns = REPLACE_MILK_COLS, inplace = True)
    milk_price_df[MONTH_COL] = pd.to_datetime(milk_price_df[MONTH_COL], format = '%b')
    
    return precipitaciones_df, banco_central_df, milk_price_df
    
    
    
    
    