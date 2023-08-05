import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class validar():
  def __init__(self,df):
    if not isinstance(df, pd.DataFrame):
            raise TypeError('Debe ser un DataFrame')
    #if not isinstance(df.index, pd.DatetimeIndex or pd.DatetimeArray or str):
    #        raise ValueError('El índice no es del tipo datetime')
    self.df = df

  def devolver_df(self):
    return self.df

  def verificar_nulos_totales(self):
    total_nulos = self.df.isnull().sum().sum()
    total_validos = self.df.notnull().sum().sum()
    ratio = (total_nulos*100)/total_validos
    return f'el porcentaje de nulos es -> {round(ratio,2)} %'

  def verificar_nulos_fecha (self):
    nulos_por_fecha = self.df.isnull().sum(axis=1)
    fechas = pd.to_datetime(self.df.index).date
    df_nulos = pd.DataFrame({'Fecha': fechas, 'Valores Nulos': nulos_por_fecha})
    df_nulos.set_index('Fecha', inplace=True)
    df_nulos = df_nulos.sort_values('Valores Nulos', ascending=False)
    return df_nulos

  def verificar_nulos(self, grafico=False, tabla=False):
    nulos = self.df.isnull().sum().sort_values(ascending=False)
    total_valores = self.df.shape[0]
    porcentaje_nulos = (nulos / total_valores) * 100

    if grafico:
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        ax1.bar(nulos.index, nulos.values, label='Valores Nulos')
        ax2.plot(nulos.index, porcentaje_nulos, color='red', marker='o', label='Porcentaje de Nulos')
        ax1.set_title('Valores Nulos y Porcentaje de Nulos por Columna')
        ax1.set_xlabel('Columnas')
        ax1.set_ylabel('Cantidad de Nulos')
        ax2.set_ylabel('Porcentaje de Nulos')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax1.xaxis.set_tick_params(rotation=90)
        ax1.xaxis.grid(True)  
        ax1.yaxis.grid(True) 
        plt.show()
    if tabla :
      return nulos

  def mapa_calor_nulos (self):
    nulos_matriz = self.df.isnull()
    plt.figure(figsize=(12, 6))
    sns.heatmap(nulos_matriz.sort_values(by='Date', ascending=False), cbar=False, cmap='Blues')
    ax = plt.gca()
    labels = [item.get_text()[:10] for item in ax.get_yticklabels()]
    ax.set_yticklabels(labels)
    plt.title('Distribución de Valores Nulos a lo largo del tiempo')
    plt.xlabel('Columnas')
    plt.ylabel('Fecha')
    plt.show()

  def distribucion_nulos (self):
    nulos_matriz = self.df.isnull()
    plt.figure(figsize=(12, 6))
    ax = sns.heatmap(nulos_matriz.sort_values(by='Date', ascending=False).T, cbar=False, cmap='Blues', linewidths=0.5)
    labels_x = [item.get_text()[:10] for item in ax.get_xticklabels()]
    labels_y = [item.get_text() for item in ax.get_yticklabels()]
    ax.set_xticklabels(labels_x[::-1], rotation=90)
    ax.set_yticklabels(labels_y)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.annotate(labels_x[-1], xy=(0, 1), xycoords=('axes fraction', 'axes fraction'),
                xytext=(10, 10), textcoords='offset points', fontsize=12)
    ax.annotate(labels_x[0], xy=(1, 1), xycoords=('axes fraction', 'axes fraction'),
                xytext=(-40, 10), textcoords='offset points', ha='right', fontsize=12)
    plt.text(0.5, 1.1, 'Distribución de Valores Nulos a lo largo del tiempo', transform=ax.transAxes, ha='center', fontsize=14)
    plt.show()

  def distribucion_nulos_v(self):
    nulos_por_fecha = self.df.isnull().sum(axis=1)
    fechas = pd.to_datetime(self.df.index).date
    fig, ax = plt.subplots(figsize=(12, 6))
    rolling_mean = nulos_por_fecha.rolling(window=1, center=True).mean()
    ax.plot(fechas, rolling_mean, color='red', label='Media móvil')
    mask_outliers = nulos_por_fecha > rolling_mean
    colors = np.where(mask_outliers, 'black', 'lightblue')
    bar_width = 0.8
    bar_alpha = 0.8
    ax.bar(fechas, nulos_por_fecha, color=colors, width=bar_width, alpha=bar_alpha)
    outliers = nulos_por_fecha[mask_outliers]
    ax.bar(fechas[mask_outliers], outliers, color='red', width=bar_width, alpha=bar_alpha)
    ax.set_title('Distribución de Valores Nulos por Fecha')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Cantidad de Valores Nulos')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=90)
    ax.legend()
    plt.show()
