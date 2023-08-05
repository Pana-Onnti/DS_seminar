
import pyRofex


api_url = "https://api.bull.xoms.com.ar/"
ws_url = "wss://api.bull.xoms.com.ar/"

# conexion a pyrofex
pyRofex._set_environment_parameter("url", api_url, pyRofex.Environment.LIVE)
pyRofex._set_environment_parameter("ws", ws_url, pyRofex.Environment.LIVE)

pyRofex.initialize(user=username,
                   password=password,
                   account=account,
                   environment=pyRofex.Environment.LIVE
                   )




import requests
import json
import pandas
import datetime


s = requests.Session()

headers = {'X-Username':username, 'X-Password': password}
url = f"https://api.bull.xoms.com.ar/auth/getToken"

response = s.post(url=url, headers=headers)

response


        