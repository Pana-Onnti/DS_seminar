import numpy as np
import pandas as pd
import riskfolio as rp

activos = pd.read_csv('definitivo_panel_lider.csv', index_col='Date')
retornos_train = activos.pct_change().dropna()

class Portfolio:
    def __init__(self) -> None:
        pass
    def devolver(self,retornos_train):
        port = rp.HCPortfolio(returns=retornos_train)
        model='HRP'
        codependence = 'abs_spearman'
        rm =  'DaR' 
        rf = 0.6 #?
        linkage = 'DBHT'
        max_k = 10
        leaf_order = True
        w = port.optimization(model=model,
                            codependence=codependence,
                            rm=rm,
                            rf=rf,
                            linkage=linkage,
                            max_k=max_k,
                                leaf_order=leaf_order)
        return w

port = Portfolio()
port.devolver(retornos_train)

