import numpy as np
import pandas as pd
import riskfolio as rp

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


activos = pd.read_csv('definitivo_panel_lider.csv', index_col='Date')
retornos_train = activos.pct_change().dropna()

# Building the portfolio object
port = rp.HCPortfolio(returns=retornos_train)

# Estimate optimal portfolio:

model='HRP'
codependence = 'abs_spearman'
rm =  'DaR' # Risk measure used, this time will be variance
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

#display(w.T)
#normalizacion ponderada 
nueva_serie = w[w['weights'] > 0.02]  # Filtrar los pesos mayores a 0.02

total_weights = nueva_serie['weights'].sum()  # Sumar los pesos filtrados

nota = 1 - total_weights  # Calcular el valor que falta para llegar a 1

weights_sum = nueva_serie['weights'].sum()  # Suma de los pesos existentes
nueva_serie['weights'] += nota * (nueva_serie['weights'] / weights_sum)

nueva_serie['weights'] = nueva_serie['weights'] / nueva_serie['weights'].sum()  # Normalizar los pesos

nueva_serie['weights'].sum()  # Verificar que la suma de los pesos sea 1

# Ajustar el último peso para que la suma sea igual a 1
diff = 1 - nueva_serie['weights'].sum()
nueva_serie.iloc[-1, nueva_serie.columns.get_loc('weights')] += diff
nueva_serie['weights'].sum()  # Verificar que la suma de los pesos sea 1
# preparo para la funcion 
weights = nueva_serie
pesos = weights.transpose()


activos_now = pd.read_csv('definitivo_panel_lider_now.csv', index_col='Date')
activos_now = activos_now.fillna(method='ffill')
retornos_testeo = activos_now.pct_change().dropna()

retornos_testeo = retornos_testeo.drop(columns=['SUPV'])
rendimiento = calcular_rendimientos_cartera(pesos=pesos, rendimientos_diarios=retornos_testeo)

print (rendimiento['Rendimiento Acumulado'][-1])