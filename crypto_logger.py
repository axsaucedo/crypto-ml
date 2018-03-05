import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def _setup_logger(name, log_file, level=logging.DEBUG):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# first file logger
manager_logger = _setup_logger("manager", "logs/manager.log")
worker_logger = _setup_logger("worker", 'logs/worker.log')

