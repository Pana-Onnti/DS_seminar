import sqlite3
from etl.extract.p_yahoo import DescargarDataYahoo
from etl.extract.p_rava import DescargarDataRava
from variables import assets, asset_rava

path_to_db_dt = 'db\data_lake\simu.datalake.db'


class Precios:
    def __init__(self, db_path=path_to_db_dt):
        self.db_path = db_path
    def _cargar_datos(self, datos, nombre_tabla):
        with sqlite3.connect(self.db_path) as conn:
            try:
                precios = datos
                precios.to_sql(nombre_tabla, conn, if_exists='replace', index=True)
            except Exception as e:
                raise RuntimeError(f'Error al cargar los datos en {nombre_tabla}: {e}')
    def _ejecucion_descargar_rava(self):
        descargar_rava = DescargarDataRava()
        descargar_rava.obtener_token()
        datos_respuesta = descargar_rava.precios_lista(asset_rava)
        datos_respuesta.info()
        return datos_respuesta
    def cargar_datos_yahoo(self):
        try:
            datos = DescargarDataYahoo(assets=assets)
            datos = datos.data
            datos.info()
            self._cargar_datos(datos, 'precios_yahoo')
        except Exception as e:
            raise RuntimeError(f'No se pudieron descargar o cargar los datos de Yahoo: {e}')
        return 'Datos de Yahoo cargados correctamente.'
    def cargar_datos_rava(self):
        try:
            datos = self._ejecucion_descargar_rava()
            self._cargar_datos(datos, 'precios_rava')
        except Exception as e:
            raise RuntimeError(f'No se pudieron descargar o cargar los datos de Rava: {e}')
        return 'Datos de Rava cargados correctamente.'
    def descargar_precios(self):
        resultados = []
        resultados.append(self.cargar_datos_rava())
        resultados.append(self.cargar_datos_yahoo())
        return f'Datos de {", ".join(resultados)} fueron descargados y cargados correctamente.'

if __name__ == "__main__":
    # Crear una instancia de la clase Precios
    precios = Precios()

    # Llamar al método descargar_precios
    resultado = precios.descargar_precios()

    print(resultado)


