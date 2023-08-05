import numpy as np
import pandas as pd
import riskfolio as rp
import matplotlib.pyplot as plt


activos_now = pd.read_csv('definitivo_panel_lider_now.csv')
activos_now['Date'] = pd.to_datetime(activos_now['Date'])
activos_now = activos_now.set_index(activos_now['Date'])
activos_now= activos_now.drop(columns=(['Date']))
precios = activos_now

weights = [0.078182, 0.043547, 0.052573, 0.048691, 0.049757, 0.039227, 0.032345, 0.059888, 0.027772, 0.021094, 0.052213, 0.08018, 0.01284, 0.058932, 0.049437, 0.055613, 0.030349, 0.076932, 0.094556, 0.035871]


returns = precios.pct_change()[1:]
log_returns = np.log(1 + precios.pct_change()[1:])


cummulative_r = (1+returns).cumprod()
cummulative_r.fillna(1, inplace = True)

cummulative_r.iloc[-1]

cummulative_r.to_csv('onnti.csv')


cummulative_r.plot()
plt.show()
returns.mean()
returns.var()
returns.cov()
returns.corr()
returns.std()

annualized_cummulative = cummulative_r[1:]**(252/len(cummulative_r))-1

peaks = cummulative_r.cummax()
dd = (cummulative_r - peaks)/peaks
mdd = dd.min()
print(mdd)

returns.std()
Vol_annual = returns.std() * np.sqrt(252)
rf = 38.57 /100

df = pd.DataFrame(index=returns.columns)
df['CAGR'] = annualized_cummulative.iloc[-1].round(3)
df['Vol_annual'] = Vol_annual.round(3)
df['Sharpe'] = ((df['CAGR'] - rf)/ df['Vol_annual'])

returns = returns.drop(columns=['Portfolio weighted'])

cartera_cagr = np.dot(annualized_cummulative.iloc[-1],weights)
returns_w = returns.dot(weights)



peaks_portfolio = returns.dot(weights).cummax()
dd_portfolio = ((returns.dot(weights) - peaks_portfolio) / peaks_portfolio)
ddp_min = dd_portfolio.min()
dd_portfolio.plot()
plt.show()

returns_w = returns_w.sum(axis=0)

returns_w
cummulative_cartera = (1+returns_w).cumprod()
cummulative_cartera.plot()
plt.show()


ddp_min = dd_portfolio.min()
ddp_min