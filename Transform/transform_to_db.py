import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Transformar los datos brutos a los datos finales #
path_to_db = 'base_de_datos.db'

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

def transformar():
    precios_rava = descargar_datos_db('precios_rava',path_to_db)
    precios_yf = descargar_datos_db('precios_yahoo',path_to_db)
    valo = pd.DataFrame(precios_yf['VALO.BA']).set_axis(['VALO'],axis=1)
    valo.index = pd.to_datetime(valo.index)
    valo.index = valo.index.strftime('%Y-%m-%d') + ' 00:00:00'
    valo.index = pd.to_datetime(valo.index)
    precios_rava.index = pd.to_datetime(precios_rava.index)
    precios_rava.index = precios_rava.index.strftime('%Y-%m-%d') + ' 00:00:00'
    precios_rava.index = pd.to_datetime(precios_rava.index)
    definitivo_panel_lider = pd.concat([precios_rava,valo],axis=1)
    datos = definitivo_panel_lider
    return datos
def cargar(datos):
    conn = sqlite3.connect(path_to_db)
    datos.to_sql('Definitivo_v1', conn, if_exists='replace', index=True)
    conn.commit()
    conn.close()

datos = transformar()
cargar(datos)




##from sqlalchemy import create_engine, text
##cambiada la db/base_de_datos.db
##precios_yahoo y precios_rava son las dos bases de datos 
##engine = create_engine("sqlite:///base_de_datos.db", echo=True)
##query = text('SELECT * FROM "precios_rava"')
##df = pd.read_sql_query(query, engine)
##print(df)
