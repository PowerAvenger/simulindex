import streamlit as st
import pandas as pd
import plotly.express as px
import time
from backend import graf_hist
from meff import obtener_meff_trimestral,obtener_grafico_meff

st.set_page_config(
    page_title="Simulindex",
    page_icon=":bulb:",
    layout='wide',
    menu_items={
        'Get help':'https://www.linkedin.com/in/jfvidalsierra/',
        'About':'https://www.linkedin.com/in/jfvidalsierra/'
        }
    )

#popup de bienvenida
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


#inicializamos variable webmeff para actualizar o no el histórico
if 'web_meff' not in st.session_state:
    st.session_state.web_meff=False

def reset_slider():
    st.session_state.omip_slider=media_omip


df_FTB_trimestral_filtrado,fecha_ultimo_omip, media_omip = obtener_meff_trimestral(st.session_state.web_meff)
graf_omip_trim=obtener_grafico_meff(df_FTB_trimestral_filtrado)

# Inicializamos margen a cero
if 'margen' not in st.session_state:
    margen=0

#ELEMENTOS DE LA BARRA LATERAL

#Primer grupo
st.sidebar.subheader('Datos de OMIP', divider='rainbow')
st.sidebar.info('Aquí tienes el valor medio de :green[OMIP] en €/MWh a partir de los siguientes trimestres, así como la fecha del último registro.',icon="ℹ️")
st.sidebar.metric('Fecha', value=fecha_ultimo_omip)
st.sidebar.metric(':green[OMIP] medio', value=media_omip)

with st.sidebar.popover('Actualizar OMIP'):
    st.markdown('⚠️ ¡Sólo autorizados! ⚠️')
    password=st.text_input('Introduce la contraseña',type='password')
    if password=='josepass':
        st.session_state.web_meff=True
        df_FTB_trimestral_filtrado,fecha_ultimo_omip, media_omip = obtener_meff_trimestral(st.session_state.web_meff)
        reset_slider()
           
    st.session_state.web_meff=False    

if 'omip_slider' not in st.session_state:
    st.session_state.omip_slider=media_omip



st.sidebar.subheader('¡Personaliza la simulación!', divider='rainbow')
st.sidebar.info('Usa el deslizador para modificar el valor de :green[OMIP]. No te preocupes, siempre puedes resetear al valor por defecto.',icon="ℹ️")
with st.sidebar.container(border=True):
    omip=st.slider(':green[OMIP] en €/MWh',min_value=30,max_value=150, step=1, key='omip_slider')
    reset_omip=st.sidebar.button('Resetear OMIP',on_click=reset_slider)
    

grafico, simul20, simul30, simul61 = graf_hist(omip)

with st.sidebar.container(border=True):
    st.sidebar.subheader('¡Más interacción!', divider='rainbow')
    st.sidebar.info('¿Quieres afinar un poco más. Añade :violet[margen] al gusto y obtén un precio medio de indexado más ajustado con tus necesidades.',icon="ℹ️")
    añadir_margen=st.sidebar.toggle('Quieres añadir :violet[margen]?')
    if añadir_margen:
        margen=st.sidebar.slider('Añade margen al precio base de indexado en €/MWh', min_value=1,max_value=50, value=10, step=1)
        
simul20_margen=simul20+margen/10
simul30_margen=simul30+margen/10
simul61_margen=simul61+margen/10



## Layout de la página principal
st.title("Simulindex PowerAPP©")
st.subheader("Tu aplicación para simular los futuros precios minoristas de indexado")
st.caption("Copyright by Jose Vidal :ok_hand:")
url_apps = "https://powerappspy-josevidal.streamlit.app/"
st.write("Visita mi página de [PowerAPPs](%s) con un montón de utilidades" % url_apps)
url_linkedin = "https://www.linkedin.com/posts/jfvidalsierra_powerapps-activity-7216715360010461184-YhHj?utm_source=share&utm_medium=member_desktop"
st.write("Deja tus comentarios y propuestas en mi perfil de [Linkedin](%s)" % url_linkedin)
#st.divider()

#PRIMERA TANDA DE GRÁFICOS. OMIP TRIMESTRAL.
st.write(graf_omip_trim)

st.info('**¿Cómo funciona?** Los :orange[puntos] son valores de indexado de los 12 últimos meses. Las :orange[líneas] reflejan una tendencia. Los :green[círculos] simulan los precios medios de indexado a un año vista en base al valor de OMIP usado por defecto o seleccionado por ti. Además, reflejarán el margen si así lo añades.',icon="ℹ️")

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
            




