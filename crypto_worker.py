from celery import Celery
from crypto_utils import dump, load
from crypto_models import ModelLibrary
from crypto_logger import worker_logger as log

app = Celery('crypto_celery', backend='amqp://guest@localhost//', broker='amqp://guest@localhost//')

@app.task
def predict_task(model, p_x):
        log.debug("Predict task start on " + model)
        try:
            ml = ModelLibrary(model)
            ml.__init__(model)
            x = load(p_x)
            result = ml.predict(x)
            log.debug("Successfully predicted task on " + model)
            return dump(result)
        except Exception:
            log.exception("Error on task predicting with " + model)

