from celery import Celery
from utils import dump, load
from models import models

app = Celery('tasks', backend='amqp://guest@localhost//', broker='amqp://guest@localhost//')

@app.task
def reg(model, p_x):
        x = load(p_x)
        y = load(p_y)
        model = load(p_model)
        start_tme = datetime.datetime.now()
        model.fit(x, y)
        coef = model.coef_
        time.sleep(5) # (added this to show that work is being distributed)
        end_tme = datetime.datetime.now()
        return (dump(coef), start_tme, end_tme)

df = pd.read_csv("data/crypto/Bitcoin.csv", 
                    parse_dates=['Date']
                    , usecols=["Date", "Close"])

prices = df[['Close']].values.ravel()[::-1]



