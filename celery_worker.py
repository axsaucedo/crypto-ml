from celery import Celery
import datetime, time
import pickle
from fbprophet import Prophet
from sklearn import linear_model

models = {}

def linear(dates, prices):
    dates = np.reshape(dates, (len(dates),1))
    prices = np.reshape(prices, (len(prices),1))
    linear_mod = linear_model.LinearRegression()
    linear_mod.fit(dates, prices)

def svr(dates, prices):

def prophet(prices):
    m = Prophet()
    s = 10
    m.fit(prices)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']][-s:]

def dump(o):
    return pickle.dumps(o).hex()

def load(o):
    return pickle.loads(bytearray.fromhex(o))

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

if __name__ == '__main__':
    df = pd.read_csv("data/crypto/Bitcoin.csv", 
                        parse_dates=['Date']
                        , usecols=["Date", "Close"])
    prices = df[['Close']].values
    

