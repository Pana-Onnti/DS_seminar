import numpy as np
import pandas as pd
import riskfolio as rp
import sqlite3
from typing import NewType
import matplotlib.pyplot as plt
from scipy.stats import beta

Rendimiento = NewType('Rendimiento Acumulado', float)

'2019-01-01':'2023-06-01'

path_to_db_dt = 'db\data_lake\simu.datalake.db'
path_to_db_wh = 'db\data_w\simu.datawarehouse.db'

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

retornos_Test = retornos_test()


datos = descargar_datos_db('Definitivo_v1',path_to_db_wh,'2017-01-01','2019-01-01')


class Port_Optim:
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



def cartera_tipo_a() -> Rendimiento:
    '''''
    Se utiliza el metodo dropNa : Sugerido por la documentacion oficial 

    retornos_train.info()

    Index: 297 entries, 2017-11-02 00:00:00 to 2018-12-31 00:00:00
    Data columns (total 20 columns):
    '''''
    retornos_train = datos.pct_change().dropna()
    port = Port_Optim()
    w = port.devolver(retornos_train)
    cartera_2 = calcular_rendimientos_cartera(retornos_Test,w.T)
    return {'Rendimiento':cartera_2['Rendimiento Acumulado'].iloc[-1],
            'Pesos':w}


def cartera_tipo_b() -> Rendimiento :
    '''''
    Se utiliza el metodo Fillna -> 0 

    retornos_train.info()

    Index: 505 entries, 2017-01-02 00:00:00 to 2018-12-31 00:00:00
    Data columns (total 20 columns):
    '''''
    retornos_train = datos.pct_change().fillna(0)
    port = Port_Optim()
    w = port.devolver(retornos_train)
    cartera_1 = calcular_rendimientos_cartera(retornos_Test,w.T)
    return {'Rendimiento':cartera_1['Rendimiento Acumulado'].iloc[-1],
            'Pesos':w}



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

def normalizacion_ponderada(w):
    nueva_serie = w[w['weights'] > 0.02]  # Filtrar los pesos mayores a 0.02
    total_weights = nueva_serie['weights'].sum()  # Sumar los pesos filtrados
    nota = 1 - total_weights  # Calcular el valor que falta para llegar a 1
    weights_sum = nueva_serie['weights'].sum()  # Suma de los pesos existentes
    nueva_serie['weights'] += nota * (nueva_serie['weights'] / weights_sum)
    nueva_serie['weights'] = nueva_serie['weights'] / nueva_serie['weights'].sum()  # Normalizar los pesos
    return nueva_serie

def cartera_tipo_b_ponderada():
    '''''
    Retorno Acumulado -> 11.682280
    Elimina a :
               'VALO','CVH','LOMA','MIRG'
    '''''
    nueva_serie = normalizacion_ponderada(cartera_tipo_b()['Pesos'])
    rt = retornos_Test.drop(columns=['VALO','CVH','LOMA','MIRG'])
    cartera_tipo_b_ponderada = calcular_rendimientos_cartera(rt,nueva_serie.T)
    return cartera_tipo_b_ponderada['Rendimiento Acumulado'].iloc[-1]

def cartera_tipo_a_ponderada():
    '''''
    Retorno Acumulado -> 13.094770705307141
     Elimina a :
                'CVH','MIRG'
    '''''
    nueva_serie = normalizacion_ponderada(cartera_tipo_a()['Pesos'])
    rt = retornos_Test.drop(columns=['CVH','MIRG'])
    cartera_tipo_a_ponderada = calcular_rendimientos_cartera(rt,nueva_serie.T)
    return cartera_tipo_a_ponderada['Rendimiento Acumulado'].iloc[-1]



###############################################################################################################################################
# no hace falta ejecutar esta parte del codigo
class OptimizarParametros():
    '''
    rms Y codependence = 220 Combinaciones 
             Valores     Nombres
        126  13.222554   DaR  abs_kendall
        125  13.182411   DaR  abs_spearman
        135  13.137579   CDaR abs_spearman
        145  13.131436   EDaR abs_spearman
        136  13.100266   CDaR abs_kendall
    '''
    mode = ['HRP','HERC','HERC2']
    links = ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward','DBHT']
    rms = ['vol', 'MV', 'MAD', 'MSV', 'FLPM', 'SLPM',
                'VaR','CVaR', 'EVaR', 'WR', 'MDD', 'ADD',
                'DaR', 'CDaR', 'EDaR', 'UCI', 'MDD_Rel', 'ADD_Rel',
                'DaR_Rel', 'CDaR_Rel', 'EDaR_Rel', 'UCI_Rel']
    
    codependence = ['pearson','spearman','kendall','gerber1','abs_pearson','abs_spearman','abs_kendall','distance','mutual_info','tail']

    retornos_train = datos.pct_change().dropna()


    def funcion (x,y):
        port = rp.HCPortfolio(returns=retornos_train)
        pd.options.mode.chained_assignment = None  
        model='HRP'
        codependence = y
        rm =  x 
        rf = 0.6
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
        pesos = w.transpose()
        rendimiento = calcular_rendimientos_cartera(pesos=pesos, rendimientos_diarios=retornos_Test)
        total = rendimiento['Rendimiento Acumulado'][-1]
        return total
    
    nombres,lista = [],[]
    for x in rms :
        print (x)
        for y in codependence:
                nombre = x+y
                resultado = funcion(x,y)
                lista.append(resultado)
                nombres.append(nombre)
        print('LISTO')
    lista_final = pd.concat([pd.DataFrame(lista),pd.DataFrame(nombres)],axis=1)
    lista_final
    lista_final.columns = ['Valores','Nombres']
    lista_final.sort_values(by='Valores',ascending=False)


###############################################################################################################################################



class EvaluacionRetornosSinteticos():
    '''
    'Parámetro a': 101.04419639660203,
    'Parámetro b': 12632979.910999998,
    'Parámetro loc': 0.7936416386121465,
    'Parámetro scale': 1325577.55747351,
    'Quantiles': array([10.66692986, 12.08720577]),
    'Intervalo de confianza (95%)': (9.429945679452967,13.560909318556112),
    'Media': 11.396116168088403,
    'Probabilidad acumulada hasta': '13.2, ":", 95.09965015786422'}
    '''
    datos = []
    n = 100000#00
    rendimientos_diarios = retornos_Test

    rendimientos_diarios = np.array(rendimientos_diarios)
    for i in range(n) :
        numbers = np.random.rand(20)
        total = numbers.sum()
        array = np.reshape(numbers / total, (20, 1))
        rendimientos_ponderados = np.matmul(rendimientos_diarios,array)
        rendimiento_cartera = rendimientos_ponderados.sum(axis=1)
        rendimiento_acumulado = (1+rendimiento_cartera).cumprod() - 1
        datos.append(rendimiento_acumulado[-1])

    datos = pd.DataFrame(datos)
    datos = np.array(datos)
    datos.mean() , datos.max() , datos.min() ,  np.count_nonzero(datos > 13.182411)
    a,b,c,d = beta.fit(datos)
    a, b,loc,scale = a,b,c,d
    datos = np.array(datos)
    x = np.linspace(np.array(datos).min(), np.array(datos).max(), 100)
    pdf = beta.pdf(x, a, b,loc,scale)
    # Calcular los quantiles
    quantiles = beta.ppf([0.25, 0.75], a, b, loc=loc, scale=scale)
    # Calcular el intervalo de confianza del 95%
    confianza = beta.interval(0.95, a, b, loc=loc, scale=scale)
    # Calcular la media
    media = beta.mean(a, b, loc=loc, scale=scale)
    plt.plot(x, pdf, label='PDF')
    plt.hist(datos.round(decimals=3), density=True, bins=100, alpha=0.7, label='Datos')
    # Agregar los quantiles al gráfico
    plt.axvline(quantiles[0], color='r', linestyle='--', linewidth=1.5)
    plt.axvline(quantiles[1], color='r', linestyle='--', linewidth=1.5)
    plt.text(quantiles[0]-3, 0.32, f'Quantile: {quantiles[0]:.2f}', va='bottom')
    plt.text(quantiles[1]+1, 0.32, f'Quantile: {quantiles[1]:.2f}', va='bottom')
    # Agregar la media al gráfico
    plt.axvline(media, color='b', linestyle='--', linewidth=1.5)
    plt.text(media+1, 0.4, f'Mean: {media:.2f}', va='bottom')
    plt.xlabel('Valores')
    plt.ylabel('Probabilidad')
    plt.legend()
    plt.show()
    print("Parámetro a:", a)
    print("Parámetro b:", b)
    print("Parámetro loc:", loc)
    print("Parámetro scale:", scale)
    print("Quantiles:", quantiles)
    print("Intervalo de confianza (95%):", confianza)
    print("Media:", media)
    valor =  11.38
    prob_acumulada = beta.cdf(valor, a, b, loc=loc, scale=scale)
    print("Probabilidad acumulada para EW ", valor, ":", (1-prob_acumulada)*100)
    valor = 13.2
    prob_acumulada = beta.cdf(valor, a, b, loc=loc, scale=scale)
    print("Probabilidad acumulada hasta", valor, ":", (1-prob_acumulada)*100)
    resultados_simulacion_beta = {
        "Parámetro a": a,
        "Parámetro b": b,
        "Parámetro loc": loc,
        "Parámetro scale": scale,
        "Quantiles": quantiles,
        "Intervalo de confianza (95%)": confianza,
        "Media": media,
        "Probabilidad acumulada hasta" : f'{valor}, ":", {(prob_acumulada)*100}',
    }

####################################


'''
Aca termina el codigo donde el primer lugar se definen los datos a utilizar los periodos de entrenamiento y de testeo para el algoritmo,
periodo entramiento 2017/2019 - periodo de testeo 2019/2023-06

Se optimizan los pesos con el algoritmo de la libreria Risk-folio, apartir de ahora definido como <HRP>, donde espera como argumento los retornos
de los activos en cuestion y devuelve los pesos que deben ser asignados a cada uno de ellos.
En una comprobacion extra y por cuestiones mas practicas que de teoria se busca reducir los pesos que son menores a 0.02 y redistribuirlos
uniformemente en los restantes, arrojando como resultado la eliminacion de varios dependiendo el caso desde (2 a 4) activos
al analizar sus retornos vemos que dan resultados inferiores en terminos de retorno acumulado total que sera nuestro objetivo a optmizar,
por lo cual queda descartado la aplicacion de una normalizacion ponderada de pesos.

Enfoque Metodológico Basado en la Simulación y Análisis de Resultados:
El enfoque metodológico adoptado se fundamenta en un proceso de simulación exhaustiva.
Primero, se aplican técnicas de simulación para obtener resultados cuantitativos,
en este caso, relacionados con el Retorno Total Acumulado (RTA). En lugar de explorar factores individualmente 
uno por uno, el énfasis se pone en obtener un conjunto completo de resultados a través de la simulación.
Una vez que los resultados de la simulación están disponibles, el análisis se despliega en esta dirección.
El enfoque no se centra únicamente en examinar los posibles factores uno por uno, sino en estudiar minuciosamente
los resultados obtenidos. Cada resultado es sometido a un análisis detallado para lograr una comprensión más profunda y holística.
En esencia, el proceso implica una doble capa de análisis: la primera se concentra en la generación de resultados 
mediante la simulación, y la segunda se enfoca en el estudio pormenorizado de los resultados para una comprensión 
enriquecedora. Esta metodología proporciona una visión más completa y rica de cómo los diferentes elementos interactúan
y afectan el objetivo principal, el Retorno Total Acumulado.

podemos decir que, este enfoque permite una exploración exhaustiva y una apreciación profunda de los resultados generados
por la simulación, lo que conduce a una comprensión más sólida de las dinámicas en juego y contribuye a tomar decisiones
informadas y optimizadas en la gestión del portafolio.

Luego a traves de simulaciones buscar cuales son los mejores parametros de la funcion HRP que maximiza el RTA(Retorno Total Acumulado)
Tenemos.
    1) RM: Es la medida de riesgo que se va utilizar para optimizar el portfolio.
               Parametro seleccionado : 'DaR'
    2) Codependce: La codependencia (o matriz de similitud) se utiliza para medir la relación entre diferentes variables o elementos en el análisis.
       Los diferentes métodos de correlación y cálculo de distancia determinan cómo se mide esta relación
               Parametro seleccionado : 'abs_kendall'
    3) Linkage: Este parametro hace referencia a un tipo de 'Conexion' determinado, la cual se utiliza para el hierarchical clustering
                Parametro seleccionado : 'DBHT'

Luego de simular el RTA para cada RMS:CODEPENDENCE y evaluar 220 posibles combinaciones esos fueron los mejores resultados.
El parametro Linkage se evaluo con parametros estaticos para evitar hacer 1,760 simulaciones se evaluó con valores estáticos
debido a consideraciones de eficiencia, evitando así un gran número de simulaciones(1,760), hay razones para pensar que es innecesario
Aun que es un topico muy abordado en la bibliografia siempre aclaran que los metodos mas optimos suelen ser el Single. Ward , no encontrando
mucha menciones sobre el metodo DBHT que es el utilizado en este analisis, podemos estimar que por novedoso o experimental.

'''

'''
Evaluacion de retornos sinteticos 

En la fase posterior a la optimización del Retorno Total Acumulado (RTA), se lleva a cabo un análisis exhaustivo para evaluar la validez y robustez de
 los resultados obtenidos. Este análisis se enfoca en la generación y evaluación de carteras sintéticas, diseñadas para poner a prueba la solidez de la
   optimización y comprender mejor la variabilidad inherente en los resultados.

Generación de Carteras Sintéticas:

En esta etapa, se implementa una estrategia de simulación rigurosa para generar un conjunto diverso de carteras. Cada cartera se compone de activos
 financieros con ponderaciones ponderadas aleatorias. Estas ponderaciones son cuidadosamente normalizadas para asegurarse de que representen una
   distribución válida de la inversión en la cartera. A través de este proceso iterativo, se generan múltiples carteras, cada una de las cuales
     refleja una combinación única de activos y ponderaciones.

Análisis Estadístico con Distribución Beta:

Una vez obtenidas las carteras sintéticas, se someten a un análisis profundo utilizando la teoría de distribuciones estadísticas,
 específicamente la distribución beta. Esta distribución se ajusta a los datos generados por las carteras sintéticas para modelar la
   distribución potencial de los retornos acumulados. Los parámetros clave de la distribución beta (a, b, loc, scale) se estiman a partir
     de los datos obtenidos en las simulaciones. Esto permite capturar la forma y características de la distribución de los retornos.

Visualización y Caracterización de Resultados:

El análisis se materializa en visualizaciones gráficas significativas. Se construye una función de densidad de probabilidad (PDF) basada en 
la distribución beta y se superpone con un histograma de los retornos acumulados simulados. Esta visualización revela cómo se distribuyen los
 retornos y proporciona una representación visual de la variabilidad y los posibles resultados.

En el gráfico, se destacan los cuantiles y la media de la distribución para mostrar los niveles de retorno que podrían alcanzarse y ofrecer 
una perspectiva visual del rendimiento potencial. Además, se calculan valores cruciales, como los intervalos de confianza y las probabilidades
acumuladas hasta puntos de referencia específicos. Estos valores permiten evaluar la incertidumbre y el riesgo asociados con los resultados y
ayudan a tomar decisiones informadas.

Funcion Beta
Al ajustar la función beta a los datos de simulación, se logra una caracterización precisa de la variabilidad asociados con los resultados.
Su capacidad para calcular probabilidades acumuladas, cuantiles e intervalos de confianza permite evaluar la probabilidad de alcanzar ciertos niveles de rendimiento.

la probabilidad acumulada hasta un valor de 13.2 es del 95.10%, esto significa que hay un 95.10% de probabilidad de que el retorno acumulado de la cartera sea igual o menor
a 13.2. 
En términos prácticos, esto sugiere que en el 95.10% de los casos simulados, la cartera podría obtener un retorno acumulado de 13.2 o menos.

'''

# Otras carteras para comparar 
retornos_train = datos.pct_change().dropna()



# Building the portfolio object
port = rp.Portfolio(returns=retornos_train)

# Calculating optimal portfolio

# Select method and estimate input parameters:

method_mu='hist' # Method to estimate expected returns based on historical data.
method_cov='hist' # Method to estimate covariance matrix based on historical data.

port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

# Estimate optimal portfolio:

model='Classic' # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
rm = 'MV' # Risk measure used, this time will be variance
obj = 'Sharpe' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
hist = True # Use historical scenarios for risk measures that depend on scenarios
rf = 0 # Risk free rate
l = 0 # Risk aversion factor, only useful when obj is 'Utility'

w_classic_mv_sharpe = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)

print(w_classic_mv_sharpe)


#2. Estimating NCO Portfolio
#This is the original model proposed by López de Prado (2019). Riskfolio-Lib expand this model to 13 risk measures 
#and for objective functions: "Minimize Risk", "Maximize Utility Function", "Maximize Return/Risk Ratio" and "Equal Risk Contribution".

# Building the portfolio object
port = rp.HCPortfolio(returns=retornos_train)

# Estimate optimal portfolio:

model='NCO' # Could be HRP, HERC or NCO
codependence = 'pearson' # Correlation matrix used to group assets in clusters
covariance = 'hist' # Covariance estimation technique
obj = "MinRisk" # Posible values are "MinRisk", "Utility", "Sharpe" and "ERC"
rm = 'MV' # Risk measure used, this time will be variance
rf = 0 # Risk free rate
l = 2 # Risk aversion factor, only usefull with "Utility" objective
linkage = 'ward' # Linkage method used to build clusters
max_k = 10 # Max number of clusters used in two difference gap statistic
leaf_order = True # Consider optimal order of leafs in dendrogram

w_nco_minrisk_ward = port.optimization(model=model,
                      codependence=codependence,
                      covariance=covariance,
                      obj=obj,
                      rm=rm,
                      rf=rf,
                      l=l,
                      linkage=linkage,
                      max_k=max_k,
                      leaf_order=leaf_order)

print(w_nco_minrisk_ward.T)


# portafolio 3 

port = rp.Portfolio(returns=retornos_train)

# Calculating optimal portfolio

# Select method and estimate input parameters:

method_mu='hist' # Method to estimate expected returns based on historical data.
method_cov='hist' # Method to estimate covariance matrix based on historical data.

port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

# Estimate optimal portfolio:

model='Classic' # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
rm = 'MV' # Risk measure used, this time will be variance
obj = 'MinRisk' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
hist = True # Use historical scenarios for risk measures that depend on scenarios
rf = 0 # Risk free rate
l = 0 # Risk aversion factor, only useful when obj is 'Utility'

w_classic_mv_minrisk = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)

print(w_classic_mv_minrisk)