import streamlit as st
import pandas as pd
import plotly.express as px
#import globals

from backend import graf_hist #max_reg, lista_meses, filtrar_mes, aplicar_margen, pt1_trans,graf_pt1, pt5_trans



st.set_page_config(
    page_title="Simulindex",
    page_icon=":bulb:",
    layout='wide',
    menu_items={
        'Get help':'https://www.linkedin.com/in/jfvidalsierra/',
        'About':'https://www.linkedin.com/in/jfvidalsierra/'
        }
    )


#elementos de la barra lateral

st.sidebar.subheader('Selecciona el valor de OMIP a un año vista')
form1=st.sidebar.form('asdf')
with form1:
    omip = st.slider('OMIP en €/MWh',min_value=30,max_value=100,value=70, step=1)
    st.form_submit_button('Recalcular')

#exp=st.expander('Si quieres saber cómo funciona...')
with st.sidebar.expander('Si quieres saber cómo funciona...'):
    st.caption('Los :orange[puntos] son valores de indexado de los 12 últimos meses')
    st.caption('Las :orange[líneas] reflejan una tendencia')
    st.caption('Los :green[círculos] simulan los precios medios de indexado a un año vista en base a un valor de OMIP')





## Layout de la página principal
st.title("Simulindex 2024 webapp")
st.subheader("Tu aplicación para simular los futuros precios minoristas de indexado")
st.caption("Copyright by Jose Vidal :ok_hand:")
url_apps = "https://powerappspy-josevidal.streamlit.app/"
st.write("Visita mi página de [PowerAPPs](%s) con un montón de utilidades" % url_apps)
st.divider()


grafico,simul20,simul30,simul61=graf_hist(omip)
#st.plotly_chart(grafico)

col1,col2=st.columns([0.8,0.2])
with col1:
    st.plotly_chart(grafico)
    
with col2:
    with st.container(border=True):
        st.subheader(':blue-background[Resultados]',divider='rainbow')
        st.metric('OMIP de referencia €/MWh',value=omip,help='Este es el valor OMIP de referencia que has utilizado como entrada')
        st.divider()
        st.metric('Precio 2.0 c€/kWh',value=simul20, help='Este el precio 2.0 medio simulado a un año vista')
        #with col12:
        st.metric('Precio 3.0 c€/kWh',value=simul30,help='Este el precio 3.0 medio simulado a un año vista')
        #with col13:
        st.metric('Precio 6.1 c€/kWh',value=simul61,help='Este el precio 6.1 medio simulado a un año vista')


