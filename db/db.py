import pandas as pd
import sqlite3
from precios_yahoo import DescargarDataYahoo
from variables import assets

# Crear una conexión a la base de datos MiniSQL
conn = sqlite3.connect('minisql.db')
datos = DescargarDataYahoo(assets=assets, start="2023-01-01", end="2023-06-01")
df =datos
# Cargar DataFrame en una tabla de la base de datos
df.to_sql('nombre_tabla', conn, if_exists='replace', index=False)

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()
