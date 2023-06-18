import re
import json
import pandas as pd 
import requests
import numpy as np
import pandas as pd

class GlobalVariables:
    token = None
    s = None

class DataFetcher:
    def __init__(self):
        self.s = None

    def login(self):
        # Session
        self.s = requests.Session()

        # Funcion para el login
        def strbetw(text, left, right):
            match = re.search(left + '(.*?)' + right, text)
            if match:
                return match.group(1)
            return ''

        # url y header del login > obtener token
        url = "https://www.rava.com"
        headers = {
            "Host": "www.rava.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }
        response = self.s.get(url=url, headers=headers)
        status = response.status_code
        if status != 200:
            print("login status", status)
            exit()
        access_token = strbetw(response.text, ":access_token=\"\'", "\'\"")
        GlobalVariables.token = access_token
        GlobalVariables.s = self.s
        print(access_token)

    def fetch_data(self, especie, fecha_inicio, fecha_fin):
        if self.s is None:
            self.login()

        # Variables de la petición
        url = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"

        data = {
            "access_token": GlobalVariables.token,  # - Parece que dura 30 minutos
            "especie": especie,  # Ticker
            "fecha_inicio": fecha_inicio,  # Para que traiga todo
            "fecha_fin": fecha_fin  # Para que traiga todo
        }

        headers = {
            "Host": "clasico.rava.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://datos.rava.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://datos.rava.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site"
        }

        # Petición
        response = self.s.post(url=url, headers=headers, data=data)
        status = response.status_code
        if status != 200:
            print("form status", status)
            exit()
        datos = pd.DataFrame(json.loads(response.text)['body'])
        prices = pd.DataFrame(datos['cierre'])
        total_volumes = pd.DataFrame(datos['volumen'])
        df = pd.concat([prices, total_volumes], axis=1)
        df['Date'] = pd.to_datetime(datos['timestamp'], unit='s')
        df.set_index('Date', inplace=True)
        df.columns = ['price', 'volumes']
        return df

def traer_data2 (especie,fecha_inicio,fecha_fin):
    s = GlobalVariables.s
   # fecha_inicio,fecha_fin='2020-01-01','2022-01-01'
 #Variables de la peticion
    url = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"

    data = {
      "access_token": GlobalVariables.token,  # - Parece que dura 30 minutos 
      "especie": especie,  #Ticker
      "fecha_inicio": fecha_inicio,  #Para que traiga todo
      "fecha_fin": fecha_fin # Para que traiga todo
      }

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
    # Peticion
    response = s.post(url = url, headers = headers, data = data)
    status = response.status_code
    if status != 200:
      print("form status", status)
      exit()


    datos = pd.DataFrame(json.loads(response.text)['body'])
    prices = pd.DataFrame(datos['cierre'])

    total_volumes = pd.DataFrame(datos['volumen'])
    df= pd.concat([prices,total_volumes],axis=1)
    df['Date'] = pd.to_datetime(datos['timestamp'], unit='s')  
    df.set_index('Date',inplace=True)  
    df.columns = ['price','volumes']
    return df

#data_fetcher = DataFetcher()
#df = data_fetcher.fetch_data('MELI', '2020-01-01', '2021-01-01')

#tickers = ['MELI','GGAL']
#series = []
#for ticker in tickers:
#    series.append(traer_data2(ticker)['price'].resample('D').last())
    
#df = pd.concat(series, axis=1)
#df.columns = tickers

#df

def descargar_precios_rava(activos:list,start,end):
    data_fetcher = DataFetcher()
    df= data_fetcher.fetch_data('MELI', start, end)
    series = []
    for ticker in activos:
        series.append(traer_data2(ticker,start,end)['price'].resample('D').last())
    df = pd.concat(series, axis=1)
    df.columns = tickers
    return df

start, end ='2020-01-01', '2022-01-01'
 
tickers = ['MELI','GGAL']


a = descargar_precios_rava(tickers,start,end)

print(a)