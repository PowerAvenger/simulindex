import streamlit as st
import pandas as pd
import plotly.express as px
import time
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


# Crear un espacio vacío para el popup


if 'margen' not in st.session_state:
    margen=0

if 'popup_mostrado' not in st.session_state:
    st.session_state.popup_mostrado = False

if not st.session_state.popup_mostrado:
    popup = st.empty()
    with popup.container():
        st.markdown("""
            <div style="background-color:#007BFF; color:white; padding: 20px; text-align: center; border-radius: 10px;">
                <h2>¡Bienvenido a mis PowerAPPs!</h2>
                <p>No di-simules, que te he pillao... 😎.</p>
            </div>
            """, unsafe_allow_html=True)

    # Esperar 3 segundos
    time.sleep(3)
    
    # Eliminar el popup después de 3 segundos
    popup.empty()

    # Marcar que el popup ya ha sido mostrado
    st.session_state.popup_mostrado = True

#ELEMENTOS DE LA BARRA LATERAL
st.sidebar.subheader('Selecciona el valor de OMIP a un año vista')


with st.sidebar.container(border=True):
    omip=st.slider(':green[OMIP] en €/MWh',min_value=30,max_value=100,value=70, step=1) #, key='omip_value',on_change=actualizar_grafico)
    
grafico, simul20, simul30, simul61 = graf_hist(omip)

with st.sidebar.container(border=True):
    añadir_margen=st.sidebar.toggle('Quieres añadir :violet[margen]?')
    if añadir_margen:
        margen=st.sidebar.slider('Añade margen al precio base de indexado en €/MWh', min_value=1,max_value=50, value=10, step=1)
        #st.sidebar.slider('Añade margen al precio base de indexado en €/MWh', min_value=1,max_value=50, value=10, step=1,key='margen_value',on_change=change_margen)

simul20_margen=simul20+margen/10
simul30_margen=simul30+margen/10
simul61_margen=simul61+margen/10

st.sidebar.info('''
        ¿Cómo funciona?        
        \nLos :orange[puntos] son valores de indexado de los 12 últimos meses.  
        \nLas :orange[líneas] reflejan una tendencia.  
        \nLos :green[círculos] simulan los precios medios de indexado a un año vista en base a un valor de OMIP.
    ''',icon="ℹ️")


## Layout de la página principal
st.title("Simulindex PowerAPP©")
st.subheader("Tu aplicación para simular los futuros precios minoristas de indexado")
st.caption("Copyright by Jose Vidal :ok_hand:")
url_apps = "https://powerappspy-josevidal.streamlit.app/"
st.write("Visita mi página de [PowerAPPs](%s) con un montón de utilidades" % url_apps)
url_linkedin = "https://www.linkedin.com/posts/jfvidalsierra_powerapps-activity-7216715360010461184-YhHj?utm_source=share&utm_medium=member_desktop"
st.write("Deja tus comentarios y propuestas en mi perfil de [Linkedin](%s)" % url_linkedin)
#st.divider()


col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.plotly_chart(grafico)
with col2:
    with st.container(border=True):
        st.subheader(':blue-background[Datos de entrada]',divider='rainbow')
        col11,col12=st.columns(2)
        with col11:
            st.metric(':green[OMIP] (€/MWh)',value=omip,help='Este es el valor OMIP de referencia que has utilizado como entrada')
        with col12:
            st.metric(':violet[Margen] (€/MWh)',value=margen,help='Margen que añades para obtener un precio medio final más ajustado a tus necesidades')
    with st.container(border=True):
        st.subheader(':green-background[Datos de salida]',divider='rainbow')
        col13,col14=st.columns(2)
        with col13:
            st.text('Precios base')
            st.metric(':orange[Precio 2.0] c€/kWh',value=simul20, help='Este el precio 2.0 medio simulado a un año vista')
            st.metric(':red[Precio 3.0] c€/kWh',value=simul30,help='Este el precio 3.0 medio simulado a un año vista')
            st.metric(':blue[Precio 6.1] c€/kWh',value=simul61,help='Este el precio 6.1 medio simulado a un año vista')
        with col14:
            st.text('Precios con margen')
            st.metric(':orange[Precio 2.0] c€/kWh',value=round(simul20_margen,2), help='Este el precio 2.0 con el margen añadido')
            st.metric(':red[Precio 3.0] c€/kWh',value=round(simul30_margen,2),help='Este el precio 3.0 con el margen añadido')
            st.metric(':blue[Precio 6.1] c€/kWh',value=round(simul61_margen,2),help='Este el precio 6.1 con el margen añadido')
            


