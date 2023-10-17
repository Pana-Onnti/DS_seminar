import pandas as pd
import sqlite3

# Transformar los datos brutos a los datos finales #
path_to_db_dt = 'db\data_lake\simu.datalake.db'
path_to_db_wh = 'db\data_w\simu.datawarehouse.db'

def descargar_datos_db(db_name:str,path_to_db,start=None,end=None) :
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
def transformar():
    precios_rava = descargar_datos_db('precios_rava',path_to_db_dt)
    precios_yf = descargar_datos_db('precios_yahoo',path_to_db_dt)
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
def cargar(datos,nombre):
    conn = sqlite3.connect(path_to_db_wh)
    datos.to_sql(nombre, conn, if_exists='replace', index=True)
    conn.commit()
    conn.close()

def cargar_datos_merval():
    precios_merval_historico = pd.read_csv('aux_datos\Merval_Historico.csv', index_col='Date')
    cargar(precios_merval_historico,'merval_index')
    print( f'Datos cargados correctamente')



if __name__ == "__main__":    

    cargar_datos_merval()
    datos = transformar()
    cargar(datos,'Definitivo_v1')
    print('Datos Cargados')


