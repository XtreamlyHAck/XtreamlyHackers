import os
import pandas as pd
import pytz
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from pyspark.sql import DataFrame

from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
import joblib

horizon = '1min'
id_project = 'xtreamly-ai'
id_database = 'xtreamly_prepared'
id_table = f'v11-dm-{horizon}'
col_y_title = 'y_1min_stddev'

pd.set_option('display.max_columns', None)


def generate_features(df: DataFrame):
    dm = df.toPandas()

    dm['_time'] = [datetime.fromisoformat(str(t)).replace(tzinfo=pytz.utc) for t in dm['_time']]
    dm = dm.sort_values(by=['_time']).reset_index(drop=True)
    # for r, c in zip(df_dm.iloc[0], df_dm.columns): print(c, r)
    print(dm['_time'].min(), " -> ", dm['_time'].max())

    dt = datetime.strptime('2024-08-01 00:00:00+0000', '%Y-%m-%d %H:%M:%S%z').astimezone(pytz.UTC)
    col_y = [col_y_title]
    col_x = [
        "ids_" + "5min_" + "mean",
        "price_" + "60min_" + "stddev",
        "price_" + "1min_" + "stddev",
        "ids_" + "1min_" + "mean",
        "price_" + "1440min_" + "stddev",
        "transactions_" + "60min_" + "mean",
        "price_" + "15min_" + "stddev",
        "vwap_" + "60min_" + "mean",
        "price_" + "5min_" + "ema",
        "price_" + "5min_" + "perc90",
        "vwap_" + "15min_" + "mean",
        "price_" + "5min_" + "stddev",
        "price_" + "5min_" + "min",
        "price_" + "5min_" + "bollingerupper"
    ]
    df_test = dm[dm['_time'] > dt][col_y+col_x]
    df_train = dm[dm['_time'] < dt][col_y+col_x]
    X = df_train[col_x]
    Y = df_train[col_y].values.ravel()

    return X, Y


def train(X: pd.DataFrame, Y: pd.DataFrame):
    print(X.shape)
    print(X.dtypes)

    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    param_xgboost = {
        'learning_rate': [0.01, 0.05],  # Fewer learning rates
        'n_estimators': [70, 100],  # Essential range for estimators
        'subsample': [0.8, 1.0],  # Reduced subsample ratios
        'max_depth': [7, 8],  # Simplified depth range
        'gamma': [0, 0.1],  # Reduced loss reduction options
        'min_child_weight': [1, 3],  # Reduced instance weight sum values
        'random_state': [124],  # Fixed for reproducibility
    }
    model = XGBRegressor(eval_metric='rmse')
    grid_search = GridSearchCV(estimator=model,
                               param_grid=param_xgboost,
                               n_jobs=-1,
                               cv=cv, scoring='neg_mean_squared_error', error_score=0)
    grid_search.fit(X, Y)

    # Get the best model from grid search
    best_model = grid_search.best_estimator_
    model_filename = os.path.join(f"v11-model_xgb_{col_y_title}.joblib")
    joblib.dump(best_model, model_filename)

    return True










