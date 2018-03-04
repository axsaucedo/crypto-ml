from celery import Celery
import datetime, time
import pickle

def dump(o):
    return pickle.dumps(o).hex()

def load(o):
    return pickle.loads(bytearray.fromhex(o))

app = Celery('tasks', backend='amqp://guest@localhost//', broker='amqp://guest@localhost//')

@app.task
def reg(p_model, p_x, p_y):
        x = load(p_x)
        y = load(p_y)
        model = load(p_model)
        start_tme = datetime.datetime.now()
        model.fit(x, y)
        coef = model.coef_
        time.sleep(5) # (added this to show that work is being distributed)
        end_tme = datetime.datetime.now()
        return (dump(coef), start_tme, end_tme)

