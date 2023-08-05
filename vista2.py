import streamlit as st
import pandas as pd
import numpy as np
import plost

class Cartera:
    def __init__(self, activos, weights):
        self.activos = activos
        self.weights = weights
        self.precios = self._cargar_precios()
        self.returns = self.precios.pct_change()
        self.cummulative_r = (1 + self.returns).cumprod() - 1
        self.cummulative_r.fillna(0, inplace=True)
        self.returns_w = self.returns.dot(self.weights)
        self.cummulative_cartera = (1 + self.returns_w).cumprod() - 1
        self.cummulative_cartera.fillna(0, inplace=True)

    def _cargar_precios(self):
        activos_now = pd.read_csv('definitivo_panel_lider_now.csv')
        activos_now['Date'] = pd.to_datetime(activos_now['Date'])
        activos_now = activos_now.set_index('Date')
        #activos_now = activos_now.drop(columns=['Date'])
        return activos_now

    #def mostrar_graficos(self):
    #    plost.line_chart(self.cummulative_cartera)
    #    plost.line_chart(self.merval_acumulado)

class Datos:
    def __init__(self):
        self.merval_historico = self._cargar_merval_historico()

    def _cargar_merval_historico(self):
        merval_historico = pd.read_csv('Merval_Historico.csv', index_col='Date')
        merval_historico = merval_historico['2019-01-07':'2023-06-01']
        merval_historico['2020-07-15':'2020-07-19'] = 45475.23828
        merval_returns = merval_historico.pct_change()
        merval_returns.fillna(0, inplace=True)
        merval_acumulado = (1 + merval_returns).cumprod() - 1
        merval_acumulado.fillna(0, inplace=True)
        return merval_acumulado

def mostrar_resultados(cartera, datos):
    #cartera.mostrar_graficos()

    df_nota = pd.DataFrame({'company': cartera.activos, 'weights': cartera.weights})
    df_nota['weights'] = (df_nota['weights'] * 100).round(2).astype(str) + '%'
    plost.donut_chart(df_nota, theta='weights', color='company', title='Distribución de Activos en la Cartera', legend='right')

    df = pd.DataFrame({'Nombre': cartera.activos, 'Ret Acum': cartera.cummulative_r.iloc[-1], 'Pesos': cartera.weights})
    df['Pesos'] = (df['Pesos'] * 100).round(2).astype(str) + '%'

    dfx = pd.DataFrame(index=cartera.returns.columns)
    dfx['CAGR'] = cartera.cummulative_r.iloc[-1].round(3)
    dfx['Vol_annual'] = cartera.returns.std() * np.sqrt(252).round(3)
    rf = 38.57 / 100
    dfx['Sharpe'] = ((dfx['CAGR'] - rf) / dfx['Vol_annual']).round(3)

    df_final = pd.merge(dfx.reset_index(), df, on='Nombre')
    df_final = df_final.drop(columns=['Ret Acum'])
    df_final.columns = ['Nombre', 'CAGR', 'Vol_annual', 'Sharpe', 'Pesos']

    st.dataframe(df_final, use_container_width=True)

def main():
    asset_names = ['ALUA', 'BBAR', 'BMA', 'CEPU', 'COME', 'CRES', 'CVH', 'EDN', 'GGAL', 'LOMA', 'MIRG', 'PAMP', 'SUPV', 'TECO2', 'TGNO4', 'TGSU2', 'TRAN', 'TXAR', 'YPFD', 'VALO.BA']
    weights = [0.078182, 0.043547, 0.052573, 0.048691, 0.049757, 0.039227, 0.032345, 0.059888, 0.027772, 0.021094, 0.052213, 0.08018, 0.01284, 0.058932, 0.049437, 0.055613, 0.030349, 0.076932, 0.094556, 0.035871]

    cartera = Cartera(asset_names, weights)
    datos = Datos()

    st.title('Cartera VS Merval :heavy_dollar_sign:')
    mostrar_resultados(cartera, datos)

if __name__ == "__main__":
    main()
