import pickle
import logging
import os

def dump(o):
    return pickle.dumps(o).hex()

def load(o):
    return pickle.loads(bytearray.fromhex(o))

def _setup_logger(name, file, dir="logs/", level=logging.DEBUG):
    """Function setup as many loggers as you want"""

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    if not os.path.exists(log_filedir):
        os.makedirs(log_filedir)

    handler = logging.FileHandler(log_filedir)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

manager_logger = _setup_logger("manager", "manager.log")
worker_logger = _setup_logger("worker", "worker.log")

