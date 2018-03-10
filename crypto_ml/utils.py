import pickle
import logging
import os

file_path = os.path.dirname(os.path.abspath(__file__)) 

def dump(o):
    return pickle.dumps(o).hex()

def load(o):
    return pickle.loads(bytearray.fromhex(o))

def _setup_logger(name
        , file
        , dir=os.path.join(file_path, "logs/")
        , level=logging.DEBUG):
    """Function setup as many loggers as you want"""

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    if not os.path.exists(dir):
        os.makedirs(dir)

    handler = logging.FileHandler(os.path.join(dir, file))
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

manager_logger = _setup_logger("manager", "manager.log")
worker_logger = _setup_logger("worker", "worker.log")


from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential

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

