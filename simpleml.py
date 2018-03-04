from celery import Celery
import datetime, time
import pickle
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
    return svr_poly.predict(p_arr)

def _svr_poly(prices):
    model = SVR(kernel='poly', C=1e3, degree=2)
    return _svr_compute(model, prices)

def _svr_rbf(prices):
    model = SVR(kernel='rbf', C=1e3, gamma=0.1)
    return _svr_compute(model, prices)

def _svr_linear(prices):
    model = SVR(kernel='linear', C=1e3)
    return _svr_compute(model, prices)

def linear(dates, prices):
    dates = np.reshape(dates, (len(dates),1))
    prices = np.reshape(prices, (len(prices),1))
    linear_mod = linear_model.LinearRegression()
    linear_mod.fit(dates, prices)

def prophet(prices):
    m = Prophet()
    s = 10
    m.fit(prices)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    return forecast[['yhat']][-s:]

def dump(o):
    return pickle.dumps(o).hex()

def load(o):
    return pickle.loads(bytearray.fromhex(o))

app = Celery('tasks', backend='amqp://guest@localhost//', broker='amqp://guest@localhost//')

@app.task
def reg(model, p_x):
        x = load(p_x)
        y = load(p_y)
        model = load(p_model)
        start_tme = datetime.datetime.now()
        model.fit(x, y)
        coef = model.coef_
        time.sleep(5) # (added this to show that work is being distributed)
        end_tme = datetime.datetime.now()
        return (dump(coef), start_tme, end_tme)

df = pd.read_csv("data/crypto/Bitcoin.csv", 
                    parse_dates=['Date']
                    , usecols=["Date", "Close"])

prices = df[['Close']].values.ravel()[::-1]



