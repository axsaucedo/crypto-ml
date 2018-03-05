from celery import Celery
from utils import dump, load
from ml_models import ModelLibrary
from crypto_logger import worker_logger as log

app = Celery('celery_worker', backend='amqp://guest@localhost//', broker='amqp://guest@localhost//')

@app.task
def predict_task(model, p_x):
        log.info("Predict task start on " + model)
        try:
            ml = ModelLibrary(model)
            x = load(p_x)
            result = ml.predict(x)
            return dump(result)
        except Exception:
            log.exception("Error on task predicting with " + model)



