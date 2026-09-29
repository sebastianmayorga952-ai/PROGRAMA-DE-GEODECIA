import streamlit as st
from modulos import modulo_a
from utilidades.elipsoides import DICCIONARIO_ELIPSOIDES, obtener_parametros

st.set_page_config(page_title="Proyecto Geodesia Geométrica", layout="wide")

st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Seleccione el Módulo:", 
                          ["A. Elipsoide 3D (Transformación)", 
                           "B. Área de Cuadrilátero", 
                           "C. Proyección Única de Colombia"])

st.sidebar.markdown("---")
st.sidebar.subheader("Configuración Global")

# AHORA el menú desplegable lee automáticamente los 10 elipsoides
nombre_elipsoide = st.sidebar.selectbox("Seleccione el Elipsoide:", list(DICCIONARIO_ELIPSOIDES.keys()))

# Calculamos a, b, f, e2 según lo que el usuario haya seleccionado
a, b, f, e2 = obtener_parametros(nombre_elipsoide)

# Mostramos los valores abajo en el menú para que el profesor vea que sí cambian
st.sidebar.markdown("**Parámetros actuales:**")
st.sidebar.text(f"a  = {a} m")
st.sidebar.text(f"b  = {b:.4f} m")
st.sidebar.text(f"e² = {e2:.8f}")

if opcion == "A. Elipsoide 3D (Transformación)":
    # Le PASAMOS los parámetros al Módulo A para que el gráfico use el correcto
    modulo_a.mostrar_modulo(a, b)

elif opcion == "B. Área de Cuadrilátero":
    st.title("Módulo B: Área de un cuadrilátero")
    st.write("Interfaz modular en construcción...")

elif opcion == "C. Proyección Única de Colombia":
    st.title("Módulo C: Proyección Única (Directo e Inverso)")
    st.write("Interfaz modular en construcción...")
    