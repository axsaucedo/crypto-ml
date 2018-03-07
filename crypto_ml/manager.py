from crypto_ml.data_loader import CryptoLoader
from crypto_ml.worker import predict_task
from crypto_ml.utils import dump, load, manager_logger as log

class CryptoManager:

    def __init__(self, crypto_loader=CryptoLoader):
        self._cl = CryptoLoader(max_points=200)

    def send_tasks(self, model="prophet"):
        results = {}
        log.debug(self._cl.get_crypto_names())
        for name in self._cl.get_crypto_names():
            log.debug("Logger sending " + name)
            prices = self._cl.get_prices(name)
            task = predict_task.delay(model, dump(prices))
            results[name] = task

        for k,v in results.items():
            result = v.get()
            if result:
                print(k, load(result))


