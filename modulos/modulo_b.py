import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Importamos las funciones matemáticas aisladas
from calculos.calc_modulo_b import calcular_area_elipsoide
from calculos.calc_modulo_a import generar_malla_3d

def mostrar_modulo(a, b):
    st.title("Módulo B: Área de un cuadrilátero en el elipsoide")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Entrada de Datos (Geodésicas)")
        
        st.write("**Punto 1 (Inferior Izquierdo):**")
        phi_1 = st.number_input("Latitud (φ1)", value=0.0, format="%.6f")
        lam_1 = st.number_input("Longitud (λ1)", value=0.0, format="%.6f")
        
        st.write("**Punto 2 (Superior Derecho):**")
        phi_2 = st.number_input("Latitud (φ2)", value=1.0, format="%.6f")
        lam_2 = st.number_input("Longitud (λ2)", value=1.0, format="%.6f")
        
        if st.button("Calcular Área", type="primary"):
            # 1. Ejecutamos la matemática desde nuestro archivo puro
            area_m2, area_km2, area_has = calcular_area_elipsoide(phi_1, lam_1, phi_2, lam_2, a, b)
            
            # 2. Mostramos los resultados en Km2 y Has (Requisito del tablero)
            st.success("✅ Cálculo exitoso")
            st.markdown(f"""
            - **Área en Kilómetros Cuadrados:** `{area_km2:,.4f} Km²`
            - **Área en Hectáreas:** `{area_has:,.4f} Has`
            """)
            
    with col2:
        st.subheader("Visualización 3D del Cuadrilátero")
        
        # Llamamos a la función de malla para no repetir código (resolución 60 como tenías)
        X, Y, Z = generar_malla_3d(a, b, resolucion=60)
        
        # Mantenemos el renderizado con tu configuración y color verde
        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Greens', opacity=0.5)])
        fig.update_layout(
            scene=dict(
                xaxis_title='Eje X', yaxis_title='Eje Y', zaxis_title='Eje Z',
                aspectratio=dict(x=1, y=1, z=b/a)
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)