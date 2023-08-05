import streamlit as st
import pandas as pd
import plost
import numpy as np
import matplotlib.pylab as plt

ticker = ['ALUA', 'BBAR', 'BMA', 'CEPU', 'COME', 'CRES', 'CVH', 'EDN', 'GGAL', 'LOMA', 'MIRG', 'PAMP', 'SUPV', 'TECO2', 'TGNO4', 'TGSU2', 'TRAN', 'TXAR', 'YPFD', 'VALO.BA']
pesos = [0.078182, 0.043547, 0.052573, 0.048691, 0.049757, 0.039227, 0.032345, 0.059888, 0.027772, 0.021094, 0.052213, 0.08018, 0.01284, 0.058932, 0.049437, 0.055613, 0.030349, 0.076932, 0.094556, 0.035871]
def def_precios():
    activos_now = pd.read_csv('definitivo_panel_lider_now.csv')
    activos_now['Date'] = pd.to_datetime(activos_now['Date'])
    activos_now = activos_now.set_index(activos_now['Date'])
    activos_now= activos_now.drop(columns=(['Date']))
    precios = activos_now
    return precios

def retornos_activos(precios, opcion_retorno='retorno_acumulado'):
    returns = precios.pct_change()
    log_returns = np.log(1 + precios.pct_change()[1:])
    cummulative_r = (1 + returns).cumprod() - 1
    cummulative_r.fillna(0, inplace=True)
    if opcion_retorno == 'retorno_simple':
        return returns
    elif opcion_retorno == 'retorno_log':
        return log_returns
    elif opcion_retorno == 'retorno_acumulado':
        return cummulative_r
    else:
        raise ValueError("La opción de retorno especificada no es válida. Opciones válidas: 'returns', 'log_returns', 'cummulative_r'")

def def_cartera(retornos,pesos,retornos_simple=None):
    retornos = retornos.dot(pesos)
    retornos_acumulados = (1+retornos).cumprod() - 1
    retornos_acumulados.fillna(0, inplace = True)
    retornos_acumulados = pd.DataFrame(retornos_acumulados['2019-01-01':'2023-06-01'])
    retornos_acumulados.columns = ['Ret Acum. Cartera']
    retornos_acumulados.index = pd.to_datetime(retornos_acumulados.index).date
    if retornos_simple == True:
        return retornos 
    else:
        return retornos_acumulados

def def_merval(retornos_simple=None):
    precios_merval_historico = pd.read_csv('Merval_Historico.csv', index_col='Date')
    precios_merval_historico = precios_merval_historico['2019-01-07':'2023-06-01']
    precios_merval_historico['2020-07-15':'2020-07-19'] = 45475.23828
    retornos_merval = precios_merval_historico.pct_change()
    log_returns = np.log(1 + precios_merval_historico.pct_change()[1:])
    retornos_merval.fillna(0, inplace = True)
    merval_retorno_acumulado = (1+retornos_merval).cumprod() -1
    merval_retorno_acumulado.fillna(0, inplace = True)
    merval_retorno_acumulado.columns = ['Ret Acum. Merval']
    merval_retorno_acumulado.index = pd.to_datetime(merval_retorno_acumulado.index).date
    if retornos_simple == True:
        return retornos_merval
    else:
        return merval_retorno_acumulado

def unir_series(primera,segunda):
    merged_df = pd.concat([primera, segunda], axis=1)
    return merged_df

precios = def_precios()
retornos = retornos_activos(precios=precios,opcion_retorno='retorno_simple')
retornos_acumulados = retornos_activos(precios=precios,opcion_retorno='retorno_acumulado')
cartera = def_cartera(retornos_activos(precios=precios,opcion_retorno='retorno_simple'),pesos)
merval = def_merval(retornos_simple=False)
merged_df=unir_series(cartera,merval)

distribucion_pesos = pd.concat([(pd.DataFrame(ticker).set_axis(['Ticker'],axis=1)),(pd.DataFrame(pesos)).set_axis(['Pesos'],axis=1)],axis=1)
df = pd.concat([(retornos_acumulados.iloc[-1].reset_index()).set_axis(['Ticker', 'Ret Acum '], axis=1),
                 (distribucion_pesos['Pesos'])], axis=1).assign(Pesos=lambda x: (x['Pesos'] * 100).round(2).map('{:.2f}%'.format))

df['Retornos Acum T'] = retornos_acumulados.to_dict(orient='list').values()
###
annualized_cummulative = retornos_acumulados[1:]**(252/len(retornos_acumulados))-1
Vol_annual = retornos.std() * np.sqrt(252)
rf = 38.57 /100
dfx = pd.DataFrame(index=retornos.columns)
dfx['CAGR'] = annualized_cummulative.iloc[-1].round(3)
dfx['Vol_annual'] = Vol_annual.round(3)
dfx['Sharpe'] = ((dfx['CAGR'] - rf)/ dfx['Vol_annual'])
df_final = pd.concat([dfx.reset_index(names=['Nombre Ticker']),df.drop(columns=['Ticker'])],axis=1)

col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

st.title('Cartera VS Merval :heavy_dollar_sign: ')
st.write('Titulo')

st.line_chart(retornos_acumulados)

st.line_chart(cartera)

st.line_chart(merval)
st.line_chart(merged_df)
plost.donut_chart(distribucion_pesos,theta='Pesos',  color='Ticker', title='Distribución de Activos en la Cartera', legend='right')

st.dataframe(
    df_final,
    column_config={
    "Ret Acum": st.column_config.LineChartColumn(
            "Retornos Acumulados", y_min=0, y_max=5000
        )
    },
    hide_index=True,
    use_container_width=True,
    )

def maximas_caidas(retornos_simple):
 returns = retornos_simple.fillna(0)
 cummulative_r = (1+returns).cumprod()
 cummulative_r.fillna(1, inplace = True)
 peaks = cummulative_r.cummax()
 dd = ((cummulative_r - peaks) / peaks)
 mdd = dd.min()
 print(mdd)
 return dd

cartera_retornos = def_cartera(retornos_activos(precios=precios,opcion_retorno='retorno_simple'),pesos,retornos_simple=True)
merval = def_merval(retornos_simple=True)
caidas_merval = maximas_caidas(merval)
caidas_cartera = maximas_caidas(cartera_retornos)

st.area_chart(caidas_merval)
st.area_chart(caidas_cartera)

merval.plot()

plt.show()

