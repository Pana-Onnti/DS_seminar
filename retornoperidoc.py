import numpy as np
import pandas as pd
import riskfolio as rp
import matplotlib.pyplot as plt
import sqlite3

path_to_db_dt = 'db\data_lake\simu.datalake.db'
path_to_db_wh = 'db\data_w\simu.datawarehouse.db'


def cargar_datos_db(db_name:str,path_to_db,start=None,end=None) :
    path_to_db = path_to_db
    if start is None:
        start = '1900-01-05'
    if end is None:
        end = '2030-01-01'
    conn = sqlite3.connect(path_to_db)
    query = f"SELECT * FROM {db_name}"
    #query = f"SELECT * FROM {db_name} WHERE Date >= '{start}' AND Date <= '{end}'"
    df_query = pd.read_sql_query(query, conn,index_col='Date')
    conn.close()
    return df_query

class Datos():
    retornos_train : None
    retornos_test : None
    start = None
    end = None
    def __init__(self) -> None:
        self._precios_brutos = None
    def pedir_datos(self):
        path_to_db = path_to_db_wh
        precios_brutos = cargar_datos_db('Definitivo_v1',start=self.start,end=self.end,path_to_db=path_to_db)
        return precios_brutos
    def pedir_datos_csv(self,path:str):
        precios_brutos = pd.read_csv(path)
        precios_brutos = precios_brutos.set_index(['Date'])
        self._precios_brutos = precios_brutos
        return {'Bien':'Echo'}
    def cal_retornos(self):
        if self._precios_brutos is not None:
            precios = self._precios_brutos 
            retornos_simples = precios.pct_change().fillna(0)
            return retornos_simples
        else:
            precios = self.pedir_datos()
            retornos_simples = retornos_simples = precios.pct_change().fillna(0)
            return retornos_simples
 


class Portfolio:
    def __init__(self) -> None:
        pass
    def cal_pesos(self,retornos_train):
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


def def_cartera(retornos,pesos,retornos_simple=None):
    retornos = retornos.dot(pesos)
    retornos_acumulados = (1+retornos).cumprod() - 1
    retornos_acumulados.fillna(0, inplace = True)
    retornos_acumulados.columns = ['Ret Acum. Cartera']
    retornos_acumulados.index = pd.to_datetime(retornos_acumulados.index).date
    if retornos_simple == True:
        return retornos 
    else:
        return retornos_acumulados

def all(start,end,pathcsv=None,retornos_simple=None):
    precios = Datos()
    retornos = precios.cal_retornos()
    retornos_train = retornos[start : end]
    portfolio = Portfolio()
    port_w = portfolio.cal_pesos(retornos_train)
    retornos_test = retornos['2019-00-00':'2023-06-00']
    retornos_totales =  def_cartera(retornos_test,port_w,retornos_simple=retornos_simple)
    return retornos_totales

w  = all('2016-00-00','2019-00-00')


def retornos_periodicos():
    retorno_prueba = []
    fecha = []
    start_date = pd.Period('2019-01', freq='M')  
    end_date = pd.Period('2023-6', freq='M')
    current_date = start_date
    while current_date <= end_date:
        print(current_date)
        current_date += 1    
        w  = all('2016-00-00',str(current_date))
        retorno_prueba.append(w.iloc[-1].values)
        fecha.append(current_date)
    df = pd.concat([pd.DataFrame(retorno_prueba),pd.DataFrame(fecha)],axis=1)
    df.columns = ['rt','Date']
    df = df.set_index(['Date'],drop=True)
    return df

retornos_peri = retornos_periodicos()

def dib_plot_regr(df):
    df_reset = df.reset_index()
    df_reset['Date'] = df_reset['Date'].astype(str)
    df_reset.plot.scatter(x='Date', y='rt', title='Serie de tiempo "rt"')
    # Calcular la regresión lineal utilizando numpy
    x = np.arange(len(df_reset))  # Crear un array con valores numéricos para el eje x
    y = df_reset['rt']  # Valores de la columna 'rt' para el eje y
    coefficients = np.polyfit(x, y, 1)  # Calcular los coeficientes de la regresión lineal (orden 1)
    line = np.polyval(coefficients, x)
    # Trazar la línea de regresión lineal
    plt.plot(df_reset['Date'], line, color='red', label='Regresión lineal')
    plt.xlabel('Fecha')
    plt.ylabel('Valor rt')
    plt.xticks(rotation=90)  # Rotar las etiquetas del eje x para una mejor visualización

    plt.show()

dib_plot_regr(retornos_peri)
retornos_peri

def cartera_rebalanceada(freq:str):
    """
        Args: (freq) --> 'M' : 'A' : Mensual y AA
 
    """
    start_date = pd.Period('2019-01', freq=freq)  
    end_date = pd.Period('2023-07',freq=freq)
    current_date = start_date
    df = pd.DataFrame()
    while current_date <= end_date:
        wa  = all('2016-00-00',str(current_date),retornos_simple=True)
        next_month = current_date + 1 
        waa = wa[str(current_date)+'-00':str(next_month)+'-00']
        df = pd.concat([df,waa],axis=0)
        print(current_date)
        current_date += 1 
    return df

cartera_df = cartera_rebalanceada('M')
cartera_df.head()

def reto(retornos):
    retornos_acumulados = (1+retornos).cumprod() - 1
    retornos_acumulados.fillna(0, inplace = True)
    return retornos_acumulados

w  = all('2016-00-00','2019-00-00',retornos_simple=True)
w.sum()


