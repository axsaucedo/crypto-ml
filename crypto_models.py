from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn import linear_model
from sklearn.svm import SVR
import pandas as pd
import numpy as np
from crypto_logger import worker_logger as log

def _svr_compute(model, prices):
    times = np.arange(prices.size).reshape(-1, 1)
    model.fit(times, prices)
    p_arr = np.arange(prices.size).reshape(-1, 1)
    return model.predict(p_arr)[-10:]

def svr_poly(prices):
    model = SVR(kernel='poly', C=1e3, degree=2)
    return _svr_compute(model, prices)

def svr_rbf(prices):
    model = SVR(kernel='rbf', C=1e3, gamma=0.1)
    return _svr_compute(model, prices)

def svr_linear(prices):
    model = SVR(kernel='linear', C=1e3)
    return _svr_compute(model, prices)

def linear(prices):
    model = linear_model.LinearRegression()
    return _svr_compute(model, prices)

def prophet(prices):
    m = Prophet()
    s = 10
    times = datetime(1995,7,1) + np.arange(prices.size) * timedelta(hours=1)
    df = pd.DataFrame({"ds": times, "y": prices})
    m.fit(df)
    future = m.make_future_dataframe(periods=s)
    forecast = m.predict(future)
    return forecast[['yhat']][-s:].values.reshape(1,-1)

def get_models():
    _models = {}
    _models["svr_poly"] = svr_poly
    _models["svr_rbf"] = svr_rbf
    _models["svr_linear"] = svr_linear
    _models["prophet"] = prophet
    _models["linear"] = linear
    _models["default"] = linear
    return _models

class ModelLibrary:

    def __init__(self, name, models=get_models()):
        self._models = models
        self._model_func = self._get_model_or_default(name)

    def predict(self, x):
        result = self._model_func(x)
        return result

    def _get_model_or_default(self, name):
        return self._models.get(name, self._get_default_model())

    def _get_default_model(self):
        return self._models["default"]


