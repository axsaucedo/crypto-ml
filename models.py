from fbprophet import Prophet
from sklearn import linear_model
from sklearn.svm import SVR
import pandas as pd
import numpy as np


models = {}

def _svr_compute(model, prices):
    times = np.arange(prices.size).reshape(-1, 1)
    svr_poly.fit(times, prices)
    p_arr = np.arange(prices.size).reshape(-1, 1)
    return model.predict(p_arr)

def svr_poly(prices):
    model = SVR(kernel='poly', C=1e3, degree=2)
    return _svr_compute(model, prices)

models["svr_poly"] = svr_poly

def svr_rbf(prices):
    model = SVR(kernel='rbf', C=1e3, gamma=0.1)
    return _svr_compute(model, prices)

models["svr_rbf"] = svr_rbf

def svr_linear(prices):
    model = SVR(kernel='linear', C=1e3)
    return _svr_compute(model, prices)

models["svr_linear"] = svr_linear

def linear(prices):
    model = linear_model.LinearRegression()
    return _svr_compute(model, prices)

models["linear"] = linear

def prophet(prices):
    m = Prophet()
    s = 10
    m.fit(prices)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    return forecast[['yhat']][-s:]

models["prophet"] = prophet

models["default"] = linear

