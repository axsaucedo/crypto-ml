import os
import pandas as pd
from crypto_logger import manager_logger as log

class CryptoLoader:

    def __init__(self, data_path="data/crypto", max_points=None):
        self._crypto_data = {}
        self._max_points = max_points
        self._load_data(data_path=data_path)

    def _load_data(self, data_path=None):
        if data_path:
            self._load_from_path(data_path)

    def _load_from_path(self, data_path):
        for _,_,files in os.walk(data_path):
            for file in files:
                # Skipping file that describes all columns
                if "100" in file:
                    continue
                cols = ["Date", "Open", "High", "Low", "Close", "Volume", "Market Cap"]
                log.debug("Loading: " + file)
                try:
                    df = pd.read_csv(os.path.join(data_path, file) 
                                        , parse_dates=['Date']
                                        , usecols=cols)
                    if self._max_points:
                        df = df.truncate(0, self._max_points)
                    # flip to ensure that latest date is at bottom (for ml models)
                    df = df.iloc[::-1]
                    # Remove extension, caps, and whitespace
                    crypto_name = file[:-4].lower().replace(' ', '_')
                    self._crypto_data[crypto_name] = df
                    log.debug("Loaded as " + crypto_name)
                except Exception:
                    log.exception("Error loading" + file)
                    continue
            
    def get_crypto_names(self):
        return list(self._crypto_data.keys())

    def get_df(self, crypto_name):
        return self._crypto_data.get(crypto_name, None)

    def get_prices(self, crypto_name):
        df = self.get_df(crypto_name)
        if df is None:
            return
        try:
            prices = df[['Close']].values.ravel()
            return prices
        except Exception:
            log.exception("Error returning close price for ", crypto_name)
            return


