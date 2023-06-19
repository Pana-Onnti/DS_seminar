import numpy as np
import pandas as pd
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")
# Date range

from variables import end,assets,start
import yfinance as yf
import pandas as pd

class DescargarDataYahoo:
    def __init__(self, assets, start, end):
        self.assets = assets
        self.start = start
        self.end = end
        self.data = self.descargar_data()
    
    def descargar_data(self):
        # Descargar datos
        data = yf.download(self.assets, start=self.start, end=self.end)
        data = data.loc[:, ('Adj Close', slice(None))]
        data.columns = self.assets
        return data
    
   
    def calcular_retornos(self, precios):
        # Calcular retornos
        retornos = precios[self.assets].pct_change().dropna()
        return retornos


datos = DescargarDataYahoo(assets=["AAPL", "MSFT"], start="2023-01-01", end="2023-06-01")
data = datos.descargar_precios_yahoo()
print(data)