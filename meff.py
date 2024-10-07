# %%
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import datetime
import pandas as pd
import plotly.express as px




def obtener_historicos():
    #obtenemos los históricos guardados
    df_FTB_trimestral_historicos_FTB=pd.read_csv('historicos_FTB.csv',sep=';')
    ##LAS DOS LINEAS SIGUIENTES LAS USABA CON EL FORMATO INICIAL DE FECHA 01/01/2024 Y PRECIO SIN PUNTOS
    #df_FTB_trimestral_historicos_FTB['Precio']=df_FTB_trimestral_historicos_FTB['Precio']/100
    #df_FTB_trimestral_historicos_FTB['Fecha']=pd.to_datetime(df_FTB_trimestral_historicos_FTB['Fecha'], format='%d/%m/%Y')
    df_FTB_trimestral_historicos_FTB['Fecha']=pd.to_datetime(df_FTB_trimestral_historicos_FTB['Fecha'], format='%Y-%m-%d')
    #obtenemos la fecha del último registro
    ultimo_registro=df_FTB_trimestral_historicos_FTB['Fecha'].max().date()
    
    return df_FTB_trimestral_historicos_FTB, ultimo_registro




def obtener_param_meff(ultimo_registro):
    #OBTENEMOS LAS FECHAS DE INICIO Y FINAL PARA LA DESCARGA DE MEFF
    #datetime date
    fecha_fin=datetime.datetime.now().date()
    #str parámetro a pasar
    fecha_fin_meff=fecha_fin.strftime('%d/%m/%Y')
    #str parámetro a pasar
    fecha_ini_meff=(ultimo_registro+datetime.timedelta(days=1)).strftime('%d/%m/%Y')
    #OBTENEMOS LA RUTA PARA DESCARGAR MEFF
    #path
    ruta_app=Path.cwd()
    #convertido a str como parámetro def
    ruta_app_str=str(ruta_app)

    return ruta_app_str,fecha_ini_meff,fecha_fin_meff


def descargar_meff(ruta_app_str,fecha_ini_meff,fecha_fin_meff):

    # Configurar la descarga automática para archivos .xls
    chrome_options = webdriver.ChromeOptions()
    #la ruta debe ser en str
    prefs = {
        "download.default_directory": ruta_app_str, 
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
        }
    chrome_options.add_experimental_option("prefs", prefs)
    
    chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--window-size=1920x1080")
    #chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--disable-dev-shm-usage")


    driver = webdriver.Chrome(options=chrome_options)
    
    # Abrir la página web
    driver.get("https://www.meff.es/esp/Derivados-Commodities/Historico-Detalle")

    # Aceptar cookies
    try:
        aceptar_cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
        aceptar_cookies.click()
    
    except Exception as e:
        print(f"Error al aceptar cookies: {e}")
    print(3)
    # Introducir las fechas en los campos "Desde" y "Hasta"
    try:
        # Esperar a que el campo "Desde" esté presente e introducir la fecha
        campo_desde = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'ctl00$ctl00$Contenido$Contenido$Desde$Desde_Fecha'))
        )
        campo_desde.clear() # Limpiar el campo antes de ingresar la fecha
        
        #fecha de inicio 
        campo_desde.send_keys(fecha_ini_meff) # Introduce la fecha "Desde" aquí

        # Esperar a que el campo "Hasta" esté presente e introducir la fecha
        campo_hasta = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'ctl00$ctl00$Contenido$Contenido$Hasta$Hasta_Fecha'))
        )
        campo_hasta.clear() # Limpiar el campo antes de ingresar la fecha

        #fecha de fin
        campo_hasta.send_keys(fecha_fin_meff) 

        # Hacer clic en el botón de búsqueda/descarga
        boton_descarga = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, 'ctl00$ctl00$Contenido$Contenido$Buscar'))
        )
        boton_descarga.click()

        # Esperar unos segundos para asegurarse de que la descarga se complete
        time.sleep(3)

    except Exception as e:
        print(f"Error al interactuar con los campos de fecha o al intentar descargar el archivo: {e}")

    # Cerrar el navegador
    driver.quit()

    ruta_archivo=Path(f'{ruta_app_str}\PreciosCierreDerEnergia.xls')
    if ruta_archivo.exists():
        try:
            df_FTB_trimestral_datos_raw=pd.read_html(ruta_archivo)[0]
            #print(ruta_archivo)
            
            #filtramos codigo por FTB
            df_FTB_trimestral_ftb_meff=df_FTB_trimestral_datos_raw[df_FTB_trimestral_datos_raw['Cod.'].str.startswith('FTB')]
            df_FTB_trimestral_ftb_meff=df_FTB_trimestral_ftb_meff.copy().reset_index(drop=True)
            #df_FTB_trimestral_ftb_meff=pd.read_csv('PreciosCierreDerEnergia.xls',sep=';')
            df_FTB_trimestral_ftb_meff['Precio']=df_FTB_trimestral_ftb_meff['Precio']/100
            df_FTB_trimestral_ftb_meff['Fecha']=pd.to_datetime(df_FTB_trimestral_ftb_meff['Fecha'], format='%d/%m/%Y')
            ruta_archivo.unlink()
            return df_FTB_trimestral_ftb_meff, True
        except Exception as e:
            return None, False
    else:
        return None, False

    


#webmeff es un flag true o false. si es true, vamos a la web de meff y actualizamos el histórico csv FTB. 
#en caso contrario, abrimos el histórico directamente
def obtener_FTB(web_meff):
    df_FTB_trimestral_historicos, ultimo_registro=obtener_historicos()
    if web_meff:
        ruta_app_str,fecha_ini_meff,fecha_fin_meff=obtener_param_meff(ultimo_registro)
        df_FTB_trimestral_ftb_meff, hay_datos=descargar_meff(ruta_app_str,fecha_ini_meff,fecha_fin_meff)
        #print(df_FTB_trimestral_ftb_meff)
        
        if hay_datos:
            df_FTB_trimestral_FTB=pd.concat([df_FTB_trimestral_historicos,df_FTB_trimestral_ftb_meff],ignore_index=True)
            df_FTB_trimestral_FTB.to_csv('historicos_FTB.csv',sep=';',index=False)
        else:
            df_FTB_trimestral_FTB=df_FTB_trimestral_historicos
        
    else:
        df_FTB_trimestral_FTB=df_FTB_trimestral_historicos

    return df_FTB_trimestral_FTB



# %%
def obtener_meff_trimestral(web_meff):
    
    df_FTB_trimestral = obtener_FTB(web_meff)
    #filtramos por Periodo 'Trimestral'
    df_FTB_trimestral=df_FTB_trimestral[df_FTB_trimestral['Cod.'].str.startswith('FTBCQ')]
    #hacemos copy del df_FTB_trimestral
    #df_FTB_trimestral=df_FTB_trimestral.copy()
    #eliminamos columnas innecesarias
    df_FTB_trimestral=df_FTB_trimestral.iloc[:,[0,1,5,7,14]]
    df_FTB_trimestral=df_FTB_trimestral.copy()
    # calculamos año y trimestre de la fecha actual
    current_date = datetime.datetime.now()
    current_trim = (current_date.month - 1) // 3 + 1
    current_year = current_date.year % 100  # Tomamos los últimos dos dígitos del año

    # generamos los trimestres siguientes al actual
    next_quarters = []
    for i in range(1, 5):
        next_trim = current_trim + i
        next_year = current_year
        if next_trim > 4:  # Si pasamos de Q4, volvemos a Q1 y aumentamos el año
            next_trim = next_trim % 4
            if next_trim==0:
                next_trim=4
            next_year += 1
        next_quarters.append(f'Q{next_trim}-{next_year}')

    # Paso 3: Filtrar el DataFrame para los siguientes cuatro trimestres
    df_FTB_trimestral['Entrega_Año'] = df_FTB_trimestral['Entrega'].str.split('-').str[1].astype(int)
    df_FTB_trimestral['Entrega_Trim'] = df_FTB_trimestral['Entrega'].str.split('-').str[0].str[1].astype(int)

    # Concatenamos trimestre y año para comparar con la lista generada
    df_FTB_trimestral['Trim_Año'] = df_FTB_trimestral['Entrega'].apply(lambda x: x)

    # Filtramos los trimestres que coinciden con los próximos cuatro
    df_FTB_trimestral_filtrado = df_FTB_trimestral[df_FTB_trimestral['Trim_Año'].isin(next_quarters)]

    # Elimina las columnas temporales si lo deseas
    df_FTB_trimestral_filtrado = df_FTB_trimestral_filtrado.drop(columns=['Entrega_Año', 'Entrega_Trim', 'Trim_Año'])
    trimestres_entrega=df_FTB_trimestral_filtrado['Entrega'].unique()

    #VALOR EXPORTADO
    fecha_ultimo_omip=df_FTB_trimestral_filtrado['Fecha'].max().strftime('%d.%m.%Y')
    #VALOR EXPORTADO
    media_omip=round(df_FTB_trimestral_filtrado['Precio'].iloc[-4:].mean(),2)
        
    return df_FTB_trimestral_filtrado, fecha_ultimo_omip, media_omip

# %%
#df_FTB_trimestral_filtrado,fecha_ultimo_omip, media_omip = obtener_meff_trimestral()

# %%
def obtener_grafico_meff(df_FTB_trimestral_filtrado):
    graf_omip_trim=px.line(df_FTB_trimestral_filtrado,
        x='Fecha',
        y='Precio',
        facet_col='Entrega',
        labels={'Precio':'€/MWh'}
        )
    return graf_omip_trim

# %%
#graf_omip_trim=obtener_grafico_meff(df_FTB_trimestral_filtrado)

# %%
#graf_omip_trim


