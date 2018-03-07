from crypto_ml.utils import dump, load, worker_logger as log
from crypto_ml.ml import ModelLibrary
from celery import Celery
import os

CELERY_URL = os.getenv("CRYPTO_CELERY_URL", "rabbitmq")
CELERY_USER = os.getenv("CRYPTO_CELERY_USER", "user")
CELERY_PASS = os.getenv("CRYPTO_CELERY_PASS", "1234")

app = Celery('crypto_celery',
    backend=f'amqp://{CELERY_USER}:{CELERY_PASS}@{CELERY_URL}/',    
    broker=f'amqp://{CELERY_USER}:{CELERY_PASS}@{CELERY_URL}/')

@app.task
def predict_task(model, p_x):
        log.debug("Predict task start on " + model)
        try:
            ml = ModelLibrary(model)
            x = load(p_x)
            result = ml.predict(x)
            log.debug("Successfully predicted task on " + model)
            return dump(result)
        except Exception:
            log.exception("Error on task predicting with " + model)

