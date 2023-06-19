import os
import re
import json
import pandas
import requests

s = requests.Session()

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

response = s.get(url = url, headers = headers)
status = response.status_code
if status != 200:
  print("login status", status)  
  exit()

access_token = strbetw(response.text, ":access_token=\"\'", "\'\"")

print(access_token)


url = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"

data = {
	"access_token": access_token, # - Parece que dura 30 minutos 
	"especie": "TGSU2", #Ticker
	"fecha_inicio": "0000-00-00", #Para que traiga todo
	"fecha_fin": "2030-01-01"#Para que traiga todo
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

response = s.post(url = url, headers = headers, data = data)
status = response.status_code
if status != 200:
  print("form status", status)
  exit()

print(pandas.DataFrame(json.loads(response.text)['body']))


