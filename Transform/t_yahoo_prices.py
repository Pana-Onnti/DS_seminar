import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

start = '2016-01-01'
end = '2019-01-05'

def descargar_datos_db(start=None,end=None) :
    nombre_tabla = 'precios_yahoo'
    path_to_db = 'db/base_de_datos.db'
    if start is None:
        start = '2000-01-01'
    if end is None:
        end = '2030-01-01'
    conn = sqlite3.connect(path_to_db)
    query = f"SELECT * FROM {nombre_tabla} WHERE Date >= '{start}' AND Date <= '{end}'"
    df_query = pd.read_sql_query(query, conn,index_col='Date')
    conn.close()
    return df_query

# Mostrar los datos obtenidos de la consulta

datos = descargar_datos_db(start=start,end=end)

datos.to_csv('archivo.csv', index=True)

datos.head()

datos['ALUA.BA'].plot()

plt.plot(datos['ALUA.BA'])
plt.show()