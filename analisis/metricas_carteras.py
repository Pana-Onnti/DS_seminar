import numpy as np
import pandas as pd
import sqlite3
from typing import NewType
import matplotlib.pyplot as plt
from scipy.stats import beta
from scipy.stats import norm



Rendimiento = NewType('Rendimiento Acumulado', float)
data  = {'2019-01-01':'2023-06-01'}

path_to_db_dt = 'db\data_lake\simu.datalake.db'
path_to_db_wh = 'db\data_w\simu.datawarehouse.db'
# Funciones


def calcular_rendimientos_cartera(rendimientos_diarios, pesos):
    # Calcular los rendimientos ponderados por pesos
    rendimientos_ponderados = rendimientos_diarios * pesos.values

    # Calcular el rendimiento diario de la cartera
    rendimiento_cartera = rendimientos_ponderados.sum(axis=1)

    # Calcular el rendimiento acumulado de la cartera
    rendimiento_acumulado = (1 + rendimiento_cartera).cumprod() - 1

    # Crear un DataFrame con los rendimientos diarios y acumulados de la cartera
    df_rendimientos = pd.DataFrame({
        'Rendimiento Diario': rendimiento_cartera,
        'Rendimiento Acumulado': rendimiento_acumulado
    })

    return df_rendimientos


def descargar_datos_db(db_name:str,path_to_db,start=None,end=None) :
    path_to_db = path_to_db
    if start is None:
        start = '1900-01-05'
    if end is None:
        end = '2030-01-01'
    conn = sqlite3.connect(path_to_db)
    query = f"SELECT * FROM {db_name} WHERE Date >= '{start}' AND Date <= '{end}'"
    df_query = pd.read_sql_query(query, conn,index_col='Date')
    conn.close()
    return df_query

def retornos_test():
    datos = descargar_datos_db('Definitivo_v1',path_to_db_wh,'2019-01-01','2023-06-01')
    retornos_test = datos.pct_change().fillna(0)
    datos.head()
    return retornos_test

#Datos 
datos = descargar_datos_db('Definitivo_v1',path_to_db_wh,'2017-01-01','2019-01-01')
retornos_Test = retornos_test()
retornos_train = datos.pct_change().dropna()



class Cartera():
    _pesos : None
    _retornos_simples: None
    _rf = 0
    #_rf = 38.57 /100

    def __init__(self,pesos,retornos_simples) :
        if not isinstance(pesos, pd.DataFrame):
              raise TypeError('Los pesos deben ser un DataFrame :-> Vector de pesos')
        if pesos.__len__() == 1 : 
            self._pesos = pesos
        else :
            self._pesos = pesos.T
        self._retornos_simples  = retornos_simples
        pass

    def calcular_rendimiento(self):
        df_rendimientos = calcular_rendimientos_cartera(self._retornos_simples,self._pesos) 
        return  df_rendimientos
    def ultimo_rend_acumulado(self):
        ult_rend = self.calcular_rendimiento()
        ult_rend_acumulado = ult_rend['Rendimiento Acumulado'].iloc[-1]
        return {'El Ultimo Rendimiento Acumulado es ': ult_rend_acumulado}
    def rendimientos_acumulados(self):
        r_acumulados = self.calcular_rendimiento()
        r_acumulados = r_acumulados['Rendimiento Acumulado']
        return r_acumulados
    def rendimientos_diario(self):
        r_diario = self.calcular_rendimiento()
        r_diario = r_diario['Rendimiento Diario']
        return r_diario
    def log_returns(self):
        log_returns = np.log(1 + self._retornos_simples[1:])
        return log_returns
    def log_rendimientos_acumulado(self):
        pesos = self._pesos
        log_returns_acumulado = calcular_rendimientos_cartera(self.log_returns(),pesos)
        log_returns_acumulado['Log Rendimiento Acumulado'] = log_returns_acumulado['Rendimiento Acumulado']
        return log_returns_acumulado['Log Rendimiento Acumulado'] 
    def ultimo_log_acumulado(self):
        log_r_acum = self.log_rendimientos_acumulado()
        log_r_acum = log_r_acum.iloc[-1]
        return log_r_acum
    def calcular_caidas(self):
        r_acumulado_plus = self.rendimientos_acumulados()+1
        picos = r_acumulado_plus.cummax()
        caidas = ((r_acumulado_plus - picos)/picos)
        return caidas
    def caida_maxima(self):
        max_caida = self.calcular_caidas().min()
        return max_caida
    def metricas_extras(self):
        retornos_acumulados = self.rendimientos_acumulados()
        rend_acum_anual = retornos_acumulados[1:]**(252/len(retornos_acumulados))-1
        vol_anual = (self.rendimientos_diario()).std() * np.sqrt(252)
        cagr = rend_acum_anual.iloc[-1]
        sharpe = (cagr-self._rf) / vol_anual
        return {'Sharpe':sharpe.round(3),'CAGR':cagr,'Volatilidad Anual':vol_anual.round(3)}

#Cargo los pesos 
weights = [0.078182, 0.043547, 0.052573, 0.048691, 0.049757, 0.039227, 0.032345, 0.059888, 0.027772, 0.021094, 0.052213, 0.08018, 0.01284, 0.058932, 0.049437, 0.055613, 0.030349, 0.076932, 0.094556, 0.035871]

from simulaciones import w_nco_minrisk_ward
peso = w_nco_minrisk_ward 
cartera_nco = Cartera(peso,retornos_Test)
cartera_nco.ultimo_rend_acumulado()


weights = pd.DataFrame(weights)
m_pesos_ew = np.full((1,20), 0.05)
m_pesos_ew
m_pesos_ew = pd.DataFrame(m_pesos_ew)
cartera = Cartera(m_pesos_ew,retornos_Test)  
cartera = Cartera(weights,retornos_Test)  
cartera.metricas_extras()

cartera.ultimo_rend_acumulado() # Rendimiento



# Datos de los retornos de la cartera (reemplaza con tus propios datos)

retornos_cartera = cartera.rendimientos_diario()
retornos = np.array(retornos_cartera)
retornos


def calcular_var():
    retornos_cartera = cartera.rendimientos_diario()
    retornos = np.array(retornos_cartera)
    retornos

    # Nivel de confianza para el cálculo del VAR (por ejemplo, 95%)
    confianza = 0.95

    # Cálculo del VAR histórico
    var_historico = np.percentile(retornos, (1 - confianza) * 100)

    # Cálculo del VAR paramétrico (asumiendo una distribución normal)
    media = np.mean(retornos)
    desviacion_estandar = np.std(retornos)
    var_parametrico = norm.ppf(1 - confianza, media, desviacion_estandar)

    # Método de Monte Carlo
    num_simulaciones = 100000

    # Generar simulaciones de los retornos utilizando una distribución normal
    simulaciones = np.random.normal(media, desviacion_estandar, (num_simulaciones, len(retornos)))

    # Calcular los valores finales de la cartera para cada simulación
    valores_finales = np.sum(simulaciones, axis=1)

    # Ordenar los valores finales
    valores_finales_ordenados = np.sort(valores_finales)

    # Encontrar el índice correspondiente al nivel de confianza deseado
    indice_confianza = int(num_simulaciones * confianza)

    # Calcular el VAR utilizando el índice de confianza
    var_monte_carlo = -valores_finales_ordenados[indice_confianza]

    print("VAR Histórico:", var_historico)
    print("VAR Paramétrico:", var_parametrico)
    print("VAR Monte Carlo:", var_monte_carlo)

def cartera_merval():
    datos = descargar_datos_db('merval_index',path_to_db_wh,'2019-01-01','2023-06-01')
    retornos_merval = datos.pct_change().fillna(0)
    peso_merval = pd.DataFrame([1])
    cartera = Cartera(peso_merval,retornos_merval)
    return cartera

cartera_merv = cartera_merval()
cartera_merv.ultimo_rend_acumulado()
cartera_merv.metricas_extras()


#
#retornos_cartera.to_csv('Retorno_cartera.csv',index=True)


cartera_merv = cartera_merv.rendimientos_diario()
#cartera_merv.to_csv('cartera_merv.csv',index=True)

rendimientos_acumulados = cartera.rendimientos_acumulados()
rendimientos_diario = cartera.rendimientos_diario()

volatilidad = np.std(rendimientos_diario)  * np.sqrt(252)
volatilidad
rendimiento_promedio = np.mean(rendimientos_diario)

sharpe_ratio = (rendimiento_promedio ) / volatilidad
print("Sharpe Ratio:", sharpe_ratio)


1.865 - 1.58
