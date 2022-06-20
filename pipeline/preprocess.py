import numpy as np
import pandas as pd

from pipeline.config import PRECIP_DATE_COL, BANK_DATE_COL
from pipeline.config import PIB_COLS, IMACEC_COLS, IV_COL
from pipeline.config import TARGET_COL
from pipeline.config import MONTH_COL, YEAR_COL

import logging
logger = logging.getLogger('PREPROCESSING')
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',)

def convert_int(x):
    """
    Delete points in string and convert to int
    """
    return int(x.replace('.', ''))

def to_100(x): 
    """
    Custom logic to convert to float string numbers within the 85 - 120 range
    """
    x = x.split('.')
    if x[0].startswith('1'): #es 100+
        if len(x[0]) >2:
            return float(x[0] + '.' + x[1])
        else:
            x = x[0]+x[1]
            return float(x[0:3] + '.' + x[3:])
    else:
        if len(x[0])>2:
            return float(x[0][0:2] + '.' + x[0][-1])
        else:
            x = x[0] + x[1]
            return float(x[0:2] + '.' + x[2:])
        
def drop_duplicate_bank_rows(banco_central_df):
    """
    Clean repeated rows from the datasets
    """
    logger.info(f"Dropping duplicates ...")
    banco_central_df.drop_duplicates(subset = BANK_DATE_COL, inplace = True)
    banco_central_df = banco_central_df[~banco_central_df[BANK_DATE_COL].isna()]
    return banco_central_df
    
    
def clean_bank_num_features(banco_central_df):
    """
    Clean numeric features of the bank dataset to get the real bounded values and
    create final bank dataset with filtered columns
    """
    logger.info(f"Cleaning and getting final features for bank dataset ...")
    cols_pib = PIB_COLS
    cols_pib.extend([BANK_DATE_COL])
    banco_central_pib = banco_central_df[cols_pib]
    banco_central_pib = banco_central_pib.dropna(how = 'any', axis = 0)

    for col in cols_pib:
        if col == BANK_DATE_COL:
            continue
        else:
            banco_central_pib[col] = banco_central_pib[col].apply(lambda x: convert_int(x))

    banco_central_pib.sort_values(by = BANK_DATE_COL, ascending = True)
    banco_central_pib
    
    cols_imacec = IMACEC_COLS
    cols_imacec.extend([BANK_DATE_COL])
    banco_central_imacec = banco_central_df[cols_imacec]
    banco_central_imacec = banco_central_imacec.dropna(how = 'any', axis = 0)

    for col in cols_imacec:
        if col == BANK_DATE_COL:
            continue
        else:
            banco_central_imacec[col] = banco_central_imacec[col].apply(lambda x: to_100(x))
            assert(banco_central_imacec[col].max()>100)
            assert(banco_central_imacec[col].min()>30)

    banco_central_imacec.sort_values(by = BANK_DATE_COL, ascending = True)
    banco_central_imacec
    
    banco_central_iv = banco_central_df[[IV_COL, BANK_DATE_COL]]
    banco_central_iv = banco_central_iv.dropna() 
    banco_central_iv = banco_central_iv.sort_values(by = BANK_DATE_COL, ascending = True)
    banco_central_iv[IV_COL] = banco_central_iv[IV_COL].apply(lambda x: to_100(x))
    
    banco_central_num = pd.merge(banco_central_pib, banco_central_imacec, on = BANK_DATE_COL, how = 'inner')
    banco_central_num = pd.merge(banco_central_num, banco_central_iv, on = BANK_DATE_COL, how = 'inner')
    
    return banco_central_num

def merge_datasets(precipitaciones_df, banco_central_df, milk_price_df):
    """
    Merge input and clean datasets to create the final training dataset.
    Returns X (dataframe with feature vectors) and y (vector with the target column)
    """
    
    logger.info(f"Creating date columns for merging ...")
    precipitaciones_df[MONTH_COL] = precipitaciones_df[PRECIP_DATE_COL].apply(lambda x: x.month)
    precipitaciones_df[YEAR_COL] = precipitaciones_df[PRECIP_DATE_COL].apply(lambda x: x.year)
    banco_central_df[MONTH_COL] = banco_central_df[BANK_DATE_COL].apply(lambda x: x.month)
    banco_central_df[YEAR_COL] = banco_central_df[BANK_DATE_COL].apply(lambda x: x.year)
    milk_price_df[MONTH_COL] = milk_price_df[MONTH_COL].apply(lambda x: x.month)
    
    logger.info(f"Merging all input datasets ...")
    train_df = pd.merge(milk_price_df, precipitaciones_df, on = [MONTH_COL, YEAR_COL], how = 'inner')
    train_df.drop(PRECIP_DATE_COL, axis = 1, inplace = True)
      
    train_df = pd.merge(train_df, banco_central_df, on = [MONTH_COL, YEAR_COL], how = 'inner')
    train_df.drop(BANK_DATE_COL, axis =1, inplace = True)
    
    logger.info(f"Final dataset with shape: {train_df.shape}")
    X = train_df.drop([TARGET_COL], axis = 1)
    logger.info(f"Final training dataset with columns: {list(X.columns)}, len:{len(X.columns)}")
    y = train_df[TARGET_COL]
    
    return X, y