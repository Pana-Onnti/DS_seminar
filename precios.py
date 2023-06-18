from urllib.parse import urlencode
import time, datetime
import urllib3  # pip install urllib3
import requests#pip install requests
import pandas#pip install pandas
import json
from variables import end,start

#start = '2019-12-2'
#end = '2019-12-30'

activos = ['GD30']
#activos = ['GD30','CEPU']

def refactor_activos (list:activos):
   lista_activos_refactor = []
   for activo in activos :
      activo = activo+' 48HS'
      lista_activos_refactor.append(activo)
   return lista_activos_refactor


def descargar_data_byma(activos:list,start,end):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    start_datetime = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_datetime = datetime.datetime.strptime(end, '%Y-%m-%d')
    start_timestamp = int(start_datetime.timestamp())
    end_timestamp = int(end_datetime.timestamp())
    
    srv = 'open.bymadata.com.ar'
    url = f'https://{srv}/vanoms-be-core/rest/api/bymadata/free/chart/historical-series/history'
    
    activos = refactor_activos(activos)

    symbol = 'asd'
       
    #prm = {'symbol' : symbol, 'resolution' : 'S', 'from' : start_timestamp, 'to' : end_timestamp}
    prm = {'symbol' : 'CEPUC 48HS', 'resolution' : 'S', 'from' : start_timestamp, 'to' : end_timestamp}

    print (prm)


    url = f'{url}?{urlencode(prm)}'

    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}
    
    response = requests.get(url = url, headers = headers, verify = False)
    status = response.status_code
    print(status)
    if status != 200:
        print("status != 200", status)
        exit()
    df =  pandas.read_json(response.text)
    df['t'] = pandas.to_datetime(df['t'], unit='s')
    print (df)
    time.sleep(30)

















start_datetime = datetime.datetime.strptime(start, '%Y-%m-%d')
start_timestamp = int(start_datetime.timestamp())
end_datetime = datetime.datetime.strptime(end, '%Y-%m-%d')
end_timestamp = int(end_datetime.timestamp())



# Obtener el timestamp en segundos
timestamp = start_datetime.timestamp()

print(timestamp)


def descargar_datos_byma(activos:list,start,end):
    start_datetime = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_datetime = datetime.datetime.strptime(end, '%Y-%m-%d')
    start_timestamp = int(start_datetime.timestamp())
    end_timestamp = int(end_datetime.timestamp())

    srv = 'open.bymadata.com.ar'
    url = f'https://{srv}/vanoms-be-core/rest/api/bymadata/free/chart/historical-series/history'
    
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}

    ###
    url = f'{url}?{urlencode(prm)}'
    prm = {'symbol' : 'GD30 48HS', 'resolution' : 'S', 'from' : start_timestamp, 'to' : end_timestamp}






