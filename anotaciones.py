from precios_rava import descargar_precios_rava
from precios_yahoo import descargar_precios_yahoo

start, end ='2020-01-01', '2022-01-01'
tickers = ['MELI','GGAL']

a = descargar_precios_rava(tickers,start,end)

print (a)