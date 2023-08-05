import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

start = '2016-01-01'


start = '2019-01-05'
 
#precios_yahoo y precios_rava son las dos bases de datos 

def descargar_datos_db(db_name:str,start=None,end=None) :
    path_to_db = f'db/base_de_datos.db'
    if start is None:
        start = '2019-01-05'
    if end is None:
        end = '2030-01-01'
    conn = sqlite3.connect(path_to_db)
    query = f"SELECT * FROM {db_name} WHERE Date >= '{start}' AND Date <= '{end}'"
    df_query = pd.read_sql_query(query, conn,index_col='Date')
    conn.close()
    return df_query

# Mostrar los datos obtenidos de la consulta

precios_rava = descargar_datos_db('precios_rava')

precios_yf = descargar_datos_db('precios_yahoo')

valo = pd.DataFrame(precios_yf['VALO.BA']).set_axis(['VALO'],axis=1)
valo.index = pd.to_datetime(valo.index)
valo.index = valo.index.strftime('%Y-%m-%d') + ' 00:00:00'
valo.index = pd.to_datetime(valo.index)
precios_rava.index = pd.to_datetime(precios_rava.index)
precios_rava.index = precios_rava.index.strftime('%Y-%m-%d') + ' 00:00:00'
precios_rava.index = pd.to_datetime(precios_rava.index)
definitivo_panel_lider = pd.concat([precios_rava,valo],axis=1)
definitivo_panel_lider.head()
definitivo_panel_lider.to_csv('definitivo_panel_lider_now.csv',index=True)
definitivo_panel_lider.iloc[-2]

valo.head()
precios_rava.head()