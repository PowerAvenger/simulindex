# %% [markdown]
# # Simulindex

# %% [markdown]
# ## Importamos librerías

# %%
#En pruebas: Uso de la variables mes_seleccionado definida en el archivo 'globals.py'

# %%
import pandas as pd
import plotly.express as px
#import globals

# %% [markdown]
# ## Importamos el fichero excel

# %%
df_in=pd.read_excel('data.xlsx')
df_in=df_in.set_index('fecha')
df_in

# %%
df_out=df_in.loc[:,['spot','precio_2.0', 'precio_3.0','precio_6.1']]

df_out

# %%
df_mes=df_out.resample('M').mean()
df_mes

# %%
df_hist=df_mes.tail(12).copy()
df_hist['precio_2.0']=round(df_hist['precio_2.0']/10,1)
df_hist['precio_3.0']=round(df_hist['precio_3.0']/10,1)
df_hist['precio_6.1']=round(df_hist['precio_6.1']/10,1)
df_hist['spot']=round(df_hist['spot'],2)
df_hist

# %% [markdown]
# graf_hist=px.scatter(df_hist,x='spot',y=['precio_2.0','precio_3.0','precio_6.1'], trendline='ols',
#                 labels={'value':'c€/kWh','variable':'Precios s/ ATR','spot':'Precio medio mercado mayorista €/MWh'},
#                 height=500,
#                 
#                 )
#     
# 
#   
# 

# %%
def graf_hist(omip):
    graf_hist=px.scatter(df_hist,x='spot',y=['precio_2.0','precio_3.0','precio_6.1'], trendline='ols',
                labels={'value':'c€/kWh','variable':'Precios s/ ATR','spot':'Precio medio mercado mayorista €/MWh'},
                height=500,
    )
    
    trend_results = px.get_trendline_results(graf_hist)

    #obtención del precio 2.0 simulado a partir del gráfico de tendencia 2.0
    params_20 = trend_results[trend_results['Precios s/ ATR']=='precio_2.0'].px_fit_results.iloc[0].params
    intercept_20, slope_20 = params_20[0], params_20[1]
    simul_20=round(intercept_20+slope_20*omip,1)
                
    #obtención del precio 3.0 simulado a partir del gráfico de tendencia 3.0
    params_30 = trend_results[trend_results['Precios s/ ATR']=='precio_3.0'].px_fit_results.iloc[0].params
    intercept_30, slope_30 = params_30[0], params_30[1]
    simul_30=round(intercept_30+slope_30*omip,1)
    
    #obtención del precio 6.1 simulado a partir del gráfico de tendencia 6.1
    params_61 = trend_results[trend_results['Precios s/ ATR']=='precio_6.1'].px_fit_results.iloc[0].params
    intercept_61, slope_61 = params_61[0], params_61[1]
    simul_61=round(intercept_61+slope_61*omip,1)

    graf_hist.add_scatter(x=[omip],y=[simul_20], mode='markers', 
        marker=dict(color='rgba(255, 255, 255, 0)',size=20, line=dict(width=5, color='blue')),
        name='Simul 2.0',
        text='Simul 2.0'
    )
    graf_hist.add_scatter(x=[omip],y=[simul_30], mode='markers', 
        marker=dict(color='rgba(255, 255, 255, 0)',size=20, line=dict(width=5, color='red')),
        name='Simul 3.0',
        text='Simul 3.0'
    )
    graf_hist.add_scatter(x=[omip],y=[simul_61], mode='markers', 
        marker=dict(color='rgba(255, 255, 255, 0)',size=20, line=dict(width=5, color='green')),
        name='Simul 6.1',
        text='Simul 6.1'
    )
    graf_hist.add_shape(
        type='line',
        x0=omip,
        y0=0,
        x1=omip,
        y1=simul_20,
        line=dict(color='grey', width=1,dash='dash'),
    )
    return graf_hist,simul_20,simul_30,simul_61

# %% [markdown]
# #graf_hist()
# graf_hist()
# 

# %% [markdown]
# omip=50

# %% [markdown]
# trend_results = px.get_trendline_results(graf_hist())
# trend_results

# %% [markdown]
# #obtención del precio 2.0 simulado a partir del gráfico de tendencia 2.0
# params_20 = trend_results[trend_results['Precios s/ ATR']=='precio_2.0'].px_fit_results.iloc[0].params
# intercept_20, slope_20 = params_20[0], params_20[1]
# simul_20=intercept_20+slope_20*omip

# %% [markdown]
# #obtención del precio 3.0 simulado a partir del gráfico de tendencia 3.0
# params_30 = trend_results[trend_results['Precios s/ ATR']=='precio_3.0'].px_fit_results.iloc[0].params
# intercept_30, slope_30 = params_30[0], params_30[1]
# simul_30=intercept_30+slope_30*omip
# 

# %% [markdown]
# #obtención del precio 6.1 simulado a partir del gráfico de tendencia 6.1
# params_61 = trend_results[trend_results['Precios s/ ATR']=='precio_6.1'].px_fit_results.iloc[0].params
# intercept_61, slope_61 = params_61[0], params_61[1]
# simul_61=round(intercept_61+slope_61*omip,1)

# %% [markdown]
# graf_hist.add_scatter(x=[omip],y=[simul_20], mode='markers', 
#     marker=dict(color='rgba(255, 255, 255, 0)',size=20, line=dict(width=5, color='blue')),
#     name='Simul 2.0',
#     text='Simul 2.0'
# )
# graf_hist.add_scatter(x=[omip],y=[simul_30], mode='markers', 
#     marker=dict(color='rgba(255, 255, 255, 0)',size=20, line=dict(width=5, color='red')),
#     name='Simul 3.0',
#     text='Simul 3.0'
# )
# graf_hist.add_scatter(x=[omip],y=[simul_61], mode='markers', 
#     marker=dict(color='rgba(255, 255, 255, 0)',size=20, line=dict(width=5, color='green')),
#     name='Simul 6.1',
#     text='Simul 6.1'
# )
# graf_hist.add_shape(
#     type='line',
#     x0=omip,
#     y0=0,
#     x1=omip,
#     y1=simul_20,
#     line=dict(color='grey', width=1,dash='dash'),
#     
# )
# graf_hist

# %% [markdown]
# ### Interacción en streamlit: Listado de meses disponibles para usar en un select_box

# %%
lista_meses=df_in['mes_nombre'].unique().tolist()
lista_meses

# %%
orden_meses = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12
}

# %%
lista_meses=sorted(lista_meses,key=lambda x:orden_meses[x])
lista_meses

# %% [markdown]
# ## Telemindex horario para streamlit

# %%
### Inicializamos dffm, que es el la tabla filtrada por el usuario

# %% [markdown]
# def aplicar_margen(mes_seleccionado,margen_aplicado):
#     #dffa_copia=dffa
#     dffa_copia['precio_2.0']=dffa['precio_2.0'] #+=margen_aplicado #=dffm['precio_2.0']+margen
#     dffa_copia['precio_3.0']=dffa['precio_3.0'] #+=margen_aplicado #dffm['precio_3.0']+margen
#     dffa_copia['precio_6.1']=dffa['precio_6.1'] #+=margen_aplicado #dffm['precio_6.1']+margen
#     dffa_copia['precio_2.0']+=margen_aplicado #=dffm['precio_2.0']+margen
#     dffa_copia['precio_3.0']+=margen_aplicado #dffm['precio_3.0']+margen
#     dffa_copia['precio_6.1']+=margen_aplicado #dffm['precio_6.1']+margen
#     
#     filtrar_mes(mes_seleccionado)
# 
#     return dffa_copia

# %% [markdown]
# ### De esta tabla sale el gráfico

# %% [markdown]
# ### Gráfico de salida para visualizar en streamlit


