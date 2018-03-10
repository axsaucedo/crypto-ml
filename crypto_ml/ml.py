from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn import linear_model
from sklearn.svm import SVR
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import pandas as pd
import numpy as np
from crypto_ml.utils import get_rnn_model, worker_logger as log


def get_rnn_model():
    model = Sequential()
    model.add(LSTM(input_dim=1, output_dim=50, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(100, return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(output_dim=1))
    model.add(Activation('linear'))

    model.compile(loss="mse", optimizer="rmsprop")

    return model

def rnn_predict(model, data, original, prediction_len=10):

    predictions = []
    d_predictions = []

    window = data.shape[1]

    # Start with the latest set of data
    base_frame = data[-1].copy()
    base_original = original[-window:].copy()

    for i in range(prediction_len):
        prediction = model.predict(base_frame[np.newaxis,:,:])[0,0]
        denormalised = base_original[i] * (prediction + 1)
        base_frame = base_frame[1:]

        np.append(base_frame, prediction)
        np.append(base_original, denormalised)
        predictions.append(prediction)
        d_predictions.append(denormalised)

    return d_predictions, predictions


def build_lstm_data(data, seq_len=50):

    sequence_length = seq_len + 1
    result = []

    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])

    n_result = normalise_windows(result)

    n_result = np.array(n_result)

    x = n_result[:, :-1]
    y = n_result[:, -1]

    x = np.reshape(x, (x.shape[0], x.shape[1], 1))

    return x, y

def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:
        normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalised_data.append(normalised_window)
    return normalised_data


def _svr_compute(model, prices):
    p = 10
    s = prices.size

    # Create a t time axis
    times = np.arange(s).reshape(-1, 1)

    model.fit(times, prices)

    # Create a list of the following p predictions
    p_arr = np.arange(s+1, s+p+1).reshape(-1, 1)

    return model.predict(p_arr)

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

def deep_predict(prices):
    p = 10

    model = get_rnn_model()

    x, y = build_lstm_data(prices, 50)

    model.fit(x, y, batch_size=512, nb_epoch=1, validation_split=0.05)

    predict_times = rnn_predict(model, x, prices)

    return predict_times

def get_models():
    _models = {}
    _models["svr_poly"] = svr_poly
    _models["svr_rbf"] = svr_rbf
    _models["svr_linear"] = svr_linear
    _models["prophet"] = prophet
    _models["linear"] = linear
    _models["deep_predict"] = deep_predict
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


