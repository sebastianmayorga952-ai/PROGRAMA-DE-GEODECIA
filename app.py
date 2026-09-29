import streamlit as st
from modulos import modulo_a
from modulos import modulo_b  # AGREGAMOS ESTO: Importamos el Módulo B
from utilidades.elipsoides import DICCIONARIO_ELIPSOIDES, obtener_parametros

st.set_page_config(page_title="Proyecto Geodesia Geométrica", layout="wide")

st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Seleccione el Módulo:", 
                          ["A. Elipsoide 3D (Transformación)", 
                           "B. Área de Cuadrilátero", 
                           "C. Proyección Única de Colombia"])

st.sidebar.markdown("---")
st.sidebar.subheader("Configuración Global")

nombre_elipsoide = st.sidebar.selectbox("Seleccione el Elipsoide:", list(DICCIONARIO_ELIPSOIDES.keys()))
a, b, f, e2 = obtener_parametros(nombre_elipsoide)

st.sidebar.markdown("**Parámetros actuales:**")
st.sidebar.text(f"a  = {a} m")
st.sidebar.text(f"b  = {b:.4f} m")
st.sidebar.text(f"e² = {e2:.8f}")

if opcion == "A. Elipsoide 3D (Transformación)":
    modulo_a.mostrar_modulo(a, b)

elif opcion == "B. Área de Cuadrilátero":
    # AGREGAMOS ESTO: Llamamos a la función visual del Módulo B
    modulo_b.mostrar_modulo(a, b)

elif opcion == "C. Proyección Única de Colombia":
    st.title("Módulo C: Proyección Única (Directo e Inverso)")
    st.write("Interfaz modular en construcción...")