import numpy as np
import pandas as pd
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")
# Date range

from variables import end,assets,start


# Downloading data
data = yf.download(assets, start = start, end = end)
data = data.loc[:,('Adj Close', slice(None))]
data.columns = assets
# Calculating returns
Y = data[assets].pct_change().dropna()
Y.head()

def descargar_precios_yahoo (activos:list,start,end):
    precios_activos = yf.download(activos,start = start, end = end)
    precios_activos = precios_activos.loc[:,('Adj Close', slice(None))]
    precios_activos.columns = assets
    return precios_activos

def calcular_retornos (precios):
    retornos = precios[assets].pct_change().dropna()
    return retornos
   

precios = descargar_precios_yahoo(assets, start = start, end = end)

retornos = calcular_retornos(precios)

retornos.head()