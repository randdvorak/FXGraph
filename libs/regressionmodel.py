from typing import Any
from datetime import datetime


from sklearn.linear_model import LinearRegression
import numpy as np

from .config import *

def str_to_datetime(date: str):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')

def str_to_unix_time(date: str):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z').timestamp()

class FXRegression:
    def __init__(self) -> None:
        self._regr = LinearRegression()

    def get_regression_data(self, fxdata, basecur) -> Any:
        x_train = []
        for d in fxdata[FXRatesKey].keys():
            x_train.extend((str_to_unix_time(d), str_to_unix_time(d)**2, str_to_unix_time(d)**3))
        y_train = list(v[basecur[CurrencyCodeKey]] for _, v in fxdata[FXRatesKey].items())
        x_train = np.array(x_train).reshape(-1, 3)
        self._regr.fit(x_train, np.array(y_train))
        x_regressed = list(str_to_datetime(d) for d in fxdata[FXRatesKey].keys())
        y_regressed = []
        for x in x_train:
            y_regressed.append(self._regr.predict([x]))
        return (x_regressed, y_regressed)