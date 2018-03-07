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

