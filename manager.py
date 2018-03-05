from crypto_data import CryptoLoader
from celery_worker import predict_task
from utils import dump, load

class CryptoManager:

    def __init__(self, crypto_loader=CryptoLoader):
        self._cl = CryptoLoader()

    def send_tasks(self):
        results = {}
        for name in self._cl.get_crypto_names():
            prices = self._cl.get_prices(name)
            task = predict_task.delay('prophet', dump(prices))
            results[name] = prices

        for k,v in results.items():
            print(k, v)
            r = v.get()
            print(k, r)




# print('Pulling tick data...',)
# tickers = 'XOM CVX COP VLO MSFT IBM YHOO AMZN GOOG'.split()
# start_dt = datetime(2010, 1, 1)
# end_dt = datetime(2013, 1, 1)
# quotes = [yf.download(sym, start=start_dt, end=end_dt) for sym in tickers]
# #quotes = [DataReader(sym, "yahoo", start_dt, end_dt) for sym in tickers]
# closes = dict(zip(tickers, [array([q['Adj Close'].tolist()]).transpose() for q in quotes 
#                                                                 if "Adj Close" in q]))
# print('done')
# 
# print('Mapping work to nodes...',)
# coeffs = []
# for stk1, stk2 in itertools.combinations(tickers, 2):
#         pair_name = '%s:%s'%(stk1, stk2)
#         if stk1 in closes and stk2 in closes:
#             coeffs.append((pair_name, reg.delay(
#                         dump(linear_model.LinearRegression()), 
#                         dump(closes[stk1]), 
#                         dump(closes[stk2]))))
# print('done')
# 
# print('Getting results...')
# for pair, result in coeffs:
#     r = result.get()
#     coef = load(r[0])
#     start = r[1]
#     end = r[2]
#     print(pair, coef, start, end)


