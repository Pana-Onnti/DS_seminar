import re
import json
import pandas as pd
import requests

class DescargarDataRava :

    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end
        self.token :  None
        self.sesion : None

    def obtener_token(self):
      sesion= requests.Session()
      self.sesion = sesion
      def strbetw(text, left, right):
        match = re.search( left + '(.*?)' + right, text)
        if match:
          return match.group(1)
        return ''
      url = "https://www.rava.com"
      headers = {
      "Host" : "www.rava.com",
      "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
      "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      "Accept-Language" : "en-US,en;q=0.5",
      "Accept-Encoding" : "gzip, deflate, br",
      "DNT" : "1",
      "Connection" : "keep-alive",
      "Upgrade-Insecure-Requests" : "1",
      "Sec-Fetch-Dest" : "document",
      "Sec-Fetch-Mode" : "navigate",
      "Sec-Fetch-Site" : "none",
      "Sec-Fetch-User" : "?1"
      }
      response = sesion.get(url = url, headers = headers)
      status = response.status_code
      if status != 200:
        print("login status", status)
        exit()

      access_token = strbetw(response.text, ":access_token=\"\'", "\'\"")
      self.token = access_token

    def descargar_datos(self,ticker):
      if self.start and self.end is not None:
        start = self.start 
        end = self.end
      else:
        start = "0000-00-00"
        end = "2030-01-01"
      url = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"
      headers = {
          "Host" : "clasico.rava.com",
          "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
          "Accept" : "*/*",
          "Accept-Language" : "en-US,en;q=0.5",
          "Accept-Encoding" : "gzip, deflate",
          "Content-Type" : "application/x-www-form-urlencoded",
          "Origin" : "https://datos.rava.com",
          "DNT" : "1",
          "Connection" : "keep-alive",
          "Referer" : "https://datos.rava.com/",
          "Sec-Fetch-Dest" : "empty",
          "Sec-Fetch-Mode" : "cors",
          "Sec-Fetch-Site" : "same-site"
      }
      data = {
        "access_token": self.token, # - Parece que dura 30 minutos
        "especie": ticker, #Ticker
        "fecha_inicio": "0000-00-00", #Para que traiga todo
        "fecha_fin": "2030-01-01"#Para que traiga todo
      }
      response = self.sesion.post(url = url, headers = headers, data = data)
      status = response.status_code
      if status != 200:
          print("form status", status)
          exit()
      datos = pd.DataFrame(json.loads(response.text)['body'])
      precio = pd.DataFrame(datos['cierre'])
      precio['Date'] = pd.to_datetime(datos['timestamp'], unit='s')
      precio.set_index('Date', inplace=True)
      precio.columns = ['price']
      return precio

    def precios_lista(self, assets: list):
      df_unido = pd.DataFrame()
      for activo in assets:
        try:
          df = self.descargar_datos(activo)
          df_unido = pd.concat([df_unido, df], axis=1)
        except:
          raise Exception (f'El ticker no anda {activo}')
      df_unido.columns = assets
      return df_unido


# Prueba de Ejecucion
def ejecucion():
    assets = []
    #Inicio la clase con con Args-> Fechas 
    descargar_rava = DescargarDataRava(start="2019-00-00",end="2023-06-00")
    #Obtengo el toker Dura 30min
    descargar_rava.obtener_token()
    #Realizo la Peticion :-> df
    datos_respuesta = descargar_rava.precios_lista(assets)
    #Transformo
    df = pd.DataFrame(datos_respuesta)
    # Lo Guardo
    df.to_csv('Merval_Historico.csv')
    return {'Guardado':'Correctamente'}

