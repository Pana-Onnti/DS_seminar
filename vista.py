import streamlit as st
import pandas as pd
import plost
import numpy as np
import matplotlib.pylab as plt



activos_now = pd.read_csv('definitivo_panel_lider_now.csv')
activos_now['Date'] = pd.to_datetime(activos_now['Date'])
activos_now = activos_now.set_index(activos_now['Date'])
activos_now= activos_now.drop(columns=(['Date']))
precios = activos_now
asset_names = ['ALUA', 'BBAR', 'BMA', 'CEPU', 'COME', 'CRES', 'CVH', 'EDN', 'GGAL', 'LOMA', 'MIRG', 'PAMP', 'SUPV', 'TECO2', 'TGNO4', 'TGSU2', 'TRAN', 'TXAR', 'YPFD', 'VALO.BA']
weights = [0.078182, 0.043547, 0.052573, 0.048691, 0.049757, 0.039227, 0.032345, 0.059888, 0.027772, 0.021094, 0.052213, 0.08018, 0.01284, 0.058932, 0.049437, 0.055613, 0.030349, 0.076932, 0.094556, 0.035871]
returns = precios.pct_change()
log_returns = np.log(1 + precios.pct_change()[1:])
cummulative_r = (1+returns).cumprod() - 1
cummulative_r.fillna(0, inplace = True)
returns_w = returns.dot(weights)
cummulative_cartera = (1+returns_w).cumprod() - 1
cummulative_cartera.fillna(0, inplace = True)


merval_historico = pd.read_csv('Merval_Historico.csv', index_col='Date')
merval_historico = merval_historico['2019-01-07':'2023-06-01']
merval_historico['2020-07-15':'2020-07-19'] = 45475.23828
merval_returns = merval_historico.pct_change()
merval_returns.fillna(0, inplace = True)
merval_acumulado = (1+merval_returns).cumprod() -1
merval_acumulado.fillna(0, inplace = True)
serie1 = merval_acumulado
serie2 = pd.DataFrame(cummulative_cartera['2019-01-01':'2023-06-01'])
serie1.index = pd.to_datetime(serie1.index).date
serie2.index = pd.to_datetime(serie2.index).date
merged_df = pd.concat([serie1, serie2], axis=1)
####################
#returns_w , merval_returns
###################


#st.title('Cartera VS Merval :heavy_dollar_sign: ')
#st.write('Titulo')
#st.line_chart(chart_data)
#st.line_chart(returns_w)
#st.line_chart(cummulative_cartera)
#st.line_chart(merval_acumulado)
#st.line_chart(merged_df)
#


pd.concat([serie1, serie2], axis=1)
df_nota = pd.concat([pd.DataFrame(asset_names),pd.DataFrame(weights)],axis=1)
df_nota.columns = ['company','weigths']

# Crear el gráfico de donut con plost
plost.donut_chart(df_nota,theta='weigths',  color='company', title='Distribución de Activos en la Cartera', legend='right')

##



df = pd.concat([cummulative_r.iloc[-1].reset_index(),(df_nota['weigths'])],axis=1)
df['weigths'] = (df['weigths']* 100).round(2).map('{:.2f}%'.format)

dff = df 

items = []
for i in cummulative_r:
    items.append(cummulative_r[i].values)

df['views_history'] = items


#####


annualized_cummulative = cummulative_r[1:]**(252/len(cummulative_r))-1


Vol_annual = returns.std() * np.sqrt(252)
rf = 38.57 /100

dfx = pd.DataFrame(index=returns.columns)
dfx['CAGR'] = annualized_cummulative.iloc[-1].round(3)
dfx['Vol_annual'] = Vol_annual.round(3)
dfx['Sharpe'] = ((dfx['CAGR'] - rf)/ dfx['Vol_annual'])

#dfx

#df
df_final = pd.concat([dfx.reset_index(),df],axis=1)

df_final.columns = ['Nombre','CAGR','Vol_annual','Sharpe','asd','CumRetUltimo','Pesos','Ret Acum']
df_final = df_final.drop(columns=['asd'])

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


