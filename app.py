import streamlit as st

# Importamos nuestro módulo modular
from modulos import modulo_a

# 1. CONFIGURACIÓN GENERAL DE LA PÁGINA
st.set_page_config(page_title="Proyecto Geodesia Geométrica", layout="wide")

# 2. BARRA LATERAL (Menú de navegación)
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Seleccione el Módulo:", 
                          ["A. Elipsoide 3D (Transformación)", 
                           "B. Área de Cuadrilátero", 
                           "C. Proyección Única de Colombia"])

st.sidebar.markdown("---")
st.sidebar.subheader("Configuración Global")
# Este selector lo conectaremos después a los 10 elipsoides
elipsoide = st.sidebar.selectbox("Seleccione el Elipsoide:", 
                                 ["WGS 84", "GRS 80", "Internacional 1924"])

# 3. ENRUTADOR DE MÓDULOS
if opcion == "A. Elipsoide 3D (Transformación)":
    # Llamamos a la función que creamos en modulo_a.py
    modulo_a.mostrar_modulo()

elif opcion == "B. Área de Cuadrilátero":
    st.title("Módulo B: Área de un cuadrilátero en el elipsoide")
    st.write("Interfaz modular en construcción...")

elif opcion == "C. Proyección Única de Colombia":
    st.title("Módulo C: Proyección Única (Directo e Inverso)")
    st.write("Interfaz modular en construcción...")