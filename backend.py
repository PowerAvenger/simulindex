# %% [markdown]
# # Telemindex

# %% [markdown]
# ## Importamos librerías

# %%
import pandas as pd
import plotly.express as px


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

# %%
def graf_hist(omip):
    colores_precios = {'precio_2.0': 'goldenrod', 'precio_3.0': 'darkred', 'precio_6.1': 'cyan'}
    graf_hist=px.scatter(df_hist,x='spot',y=['precio_2.0','precio_3.0','precio_6.1'], trendline='ols',
                labels={'value':'c€/kWh','variable':'Precios s/ ATR','spot':'Precio medio mercado mayorista €/MWh'},
                height=600,
                color_discrete_map=colores_precios,
                title='Simulación de los precios medios de indexado',
                
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
        marker=dict(color='rgba(255, 255, 255, 0)',size=20, line=dict(width=5, color='goldenrod')),
        name='Simul 2.0',
        text='Simul 2.0'
    )
    graf_hist.add_scatter(x=[omip],y=[simul_30], mode='markers', 
        marker=dict(color='rgba(255, 255, 255, 0)',size=20, line=dict(width=5, color='darkred')),
        name='Simul 3.0',
        text='Simul 3.0'
    )
    graf_hist.add_scatter(x=[omip],y=[simul_61], mode='markers', 
        marker=dict(color='rgba(255, 255, 255, 0)',size=20, line=dict(width=5, color='cyan')),
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
    graf_hist.update_layout(
            title={'x':0.5,'xanchor':'center'},
    )
    return graf_hist,simul_20,simul_30,simul_61

