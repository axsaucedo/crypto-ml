from crypto_ml.utils import dump, load, worker_logger as log
from crypto_ml.ml import ModelLibrary
from celery import Celery
import os

CELERY_URL = os.getenv("RABBITMQ_SERVICE_SERVICE_HOST", "localhost")
CELERY_USER = os.getenv("CRYPTO_RABBITMQ_USER", "user")
CELERY_PASS = os.getenv("CRYPTO_RABBITMQ_PASS", "1234")
CELERY_VHOST = os.getenv("CRYPTO_RABBITMQ_VHOST", "")

app = Celery('crypto_ml',
    backend=f'amqp://{CELERY_USER}:{CELERY_PASS}@{CELERY_URL}/{CELERY_VHOST}',    
    broker=f'amqp://{CELERY_USER}:{CELERY_PASS}@{CELERY_URL}/{CELERY_VHOST}')

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

