import numpy as np
import pandas as pd
from joblib import dump

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import SelectKBest, mutual_info_regression

from pipeline.config import TEST_SET_SIZE, SEED_SPLIT, SEED_NUMPY
from pipeline.config import SELECTOR_K_GRID, REGRESSION_ALPHA_GRID, POLYNOMIAL_DEGREE_GRID
from pipeline.config import CV_FOLDS, ARTIFACT_PATH


import logging
logger = logging.getLogger('TRAINING')
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',)

def set_numpy_seed():
    """
    Setting the numpy seed
    """
    logger.info(f"Setting the numpy seed for randomness")
    np.random.seed(SEED_NUMPY)
    
def split_train_set(X,y):
    """
    Splitting the labelled set in training and validation datasets.
    """
    logger.info(f"Splitting dataset in training and validation")
    return train_test_split(X, y,
                            test_size=TEST_SET_SIZE,
                            random_state=SEED_SPLIT)
    
    
def find_best_model(X_train, y_train):
    """
    Getting the best model through GridSearch for the fixed
    sklearn configuration
    """
    
    
    # Create sklearn pipeline
    pipe = Pipeline([('scale', StandardScaler()),
                     ('selector', SelectKBest(mutual_info_regression)),
                     ('poly', PolynomialFeatures()),
                     ('model', Ridge())])
    
    # Hyperparameters to tune
    k = SELECTOR_K_GRID
    alpha= REGRESSION_ALPHA_GRID
    poly = POLYNOMIAL_DEGREE_GRID
    
    # Searching through the grid of hp
    logger.info(f"Running the Grid Search ...")
    grid = GridSearchCV(estimator = pipe,
                        param_grid = dict(selector__k=k,
                                          poly__degree=poly,
                                          model__alpha=alpha),
                        cv = CV_FOLDS,
                        scoring = 'r2')
    
    grid.fit(X_train, y_train)
    return grid

def evaluate_model(grid, X_test, y_test):
    """
    Getting final metrics for the best model
    """
    
    y_predicted = grid.predict(X_test)
    rmse = mean_squared_error(y_test, y_predicted)
    r2 = r2_score(y_test, y_predicted)
    logger.info(f"Root Mean Square Error (RMSE) for validation test: {rmse}")
    logger.info(f"R2 Score for validation test: {r2}")


def get_final_model(grid, X_train, y_train):
    """
    Use the best hyperparameters to fit best model 
    and get a Pipeline object
    """
    
    best_params = grid.best_params_ 
    logger.info("Fitting final pipeline with best hyperparams:")
    logger.info(f"{best_params}")
    pipe = Pipeline([('scale', StandardScaler()),
                     ('selector', SelectKBest(score_func = mutual_info_regression,
                                             k = best_params['selector__k'])),
                     ('poly', PolynomialFeatures(degree = best_params['poly__degree'])),
                     ('model', Ridge(alpha = best_params['model__alpha']))])
    pipe.fit(X_train, y_train)
    
    logger.info("Creating pipeline file ...")
    dump(pipe, ARTIFACT_PATH)
    logger.info("Done.")
    return ARTIFACT_PATH
    