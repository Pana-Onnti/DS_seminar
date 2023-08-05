import numpy as np
import pandas as pd
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")
from configs.variables import assets
import yfinance as yf
import pandas as pd

class DescargarDataYahoo:
    def __init__(self, assets, start=None, end=None):
        self.assets = assets
        self.start = start or '1900-01-01'  
        self.end = end or '2030-01-01'  
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


#datos = DescargarDataYahoo(assets=assets)
#print(datos.data)