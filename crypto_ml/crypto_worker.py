from celery import Celery
from crypto_utils import dump, load
from crypto_models import ModelLibrary
from crypto_logger import worker_logger as log
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

