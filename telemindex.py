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
df_in=pd.read_excel('../data/telemindex_2023_2024.xlsx')
df_in

# %%
df_in.set_index('fecha')

# %% [markdown]
# ## Filtramos por año

# %%
año=2024 #con cambiar este valor ya sobra para filtrar la tabla
filtro_año=df_in['año']==año
dff =df_in[filtro_año].set_index('fecha')
dff 

# %% [markdown]
# ## Agrupamos valores por días

# %%
# Hay que hacerlo para cada uno de los 3 precios

# %%
dff_20=dff.groupby(['mes','dia'])['precio_2.0'].mean().reset_index()
dff_20

# %%
dff_30=dff.groupby(['mes','dia'])['precio_3.0'].mean().reset_index()
dff_30

# %%
dff_61=dff.groupby(['mes','dia'])['precio_6.1'].mean().reset_index()
dff_61

# %% [markdown]
# ## Unimos las tres tablas

# %%
dff_dia = pd.concat([dff_20,dff_30,dff_61], axis=1)
dff_dia


# %% [markdown]
# ### eliminamos columnas duplicadas

# %%
# se puede hacer también con dff_dia = dff_dia.loc[:, ~dff_dia.columns.duplicated()]

# %%
dff_dia=dff_dia.loc[:, ~dff_dia.T.duplicated()]
dff_dia

# %% [markdown]
# ## Graficamos los precios diarios por mes

# %%
graf=px.line(dff_dia, x='dia', y=['precio_2.0', 'precio_3.0', 'precio_6.1'], facet_col = 'mes', facet_col_wrap=3,
    height=1000,
    title="Telemindex 2024: Precios medios diarios de indexadosegún tarifas de acceso",
    labels={'value':'€/MWh','variable':'Precios s/ ATR'}
    
    
    )
graf

# %% [markdown]
# ## Creamos tabla dinámica para desagregar por horas

# %%
dff

# %%
dff.columns

# %%
pt1=dff.pivot_table(
    values=['spot','precio_2.0','precio_3.0','precio_6.1'],
    index='hora',
    aggfunc='mean'
)
pt1=pt1.reset_index()
pt1

# %%
colores_precios = {'precio_2.0': 'goldenrod', 'precio_3.0': 'darkred', 'precio_6.1': 'blue'}

# %%
graf_pt1=px.line(pt1,x='hora',y=['precio_2.0','precio_3.0','precio_6.1'],
    height=1000,
    title="Telemindex 2024: Precios medios horarios de indexado según tarifas de acceso",
    labels={'value':'€/MWh','variable':'Precios s/ ATR'},
    color_discrete_map=colores_precios,
)

graf_pt1

# %%
graf_pt1=graf_pt1.add_bar(y=pt1['spot'], name='spot', marker_color='green', width=0.5)
graf_pt1.update_layout(
    
    title_font_size=24,
    )
graf_pt1

# %%



