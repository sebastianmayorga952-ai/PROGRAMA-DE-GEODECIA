import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Importamos las funciones matemáticas aisladas
from calculos.calc_modulo_a import calcular_geodesicas, generar_malla_3d

def mostrar_modulo(a, b):
    st.title("Módulo A: Transformación de Coordenadas y Elipsoide 3D")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Entrada de Datos Cartesiana")
        st.write("Ingrese las coordenadas (X, Y, Z):")
        x_val = st.number_input("Coordenada X", value=6378137.0, format="%.4f")
        y_val = st.number_input("Coordenada Y", value=0.0, format="%.4f")
        z_val = st.number_input("Coordenada Z", value=0.0, format="%.4f")
        
        if st.button("Calcular Geodésicas", type="primary"):
            # 1. Llamamos a nuestra función matemática pura
            phi, lamb, h = calcular_geodesicas(x_val, y_val, z_val, a, b)
            
            # 2. Convertimos a grados para la presentación
            phi_deg = np.degrees(phi)
            lamb_deg = np.degrees(lamb)
            
            # 3. Mostramos los resultados
            st.success("Resultados del cálculo:")
            st.markdown(f"""
            - **Latitud ($\phi$):** `{phi_deg:.8f}°`
            - **Longitud ($\lambda$):** `{lamb_deg:.8f}°`
            - **Altura ($h$):** `{h:.4f} m`
            """)
            
    with col2:
        st.subheader("Visualización del Elipsoide 3D")
        
        # En lugar de hacer los cálculos aquí, llamamos a la función de la capa matemática
        # Esto mantiene el archivo visual limpio. (resolucion=60 igual que tenías)
        X_malla, Y_malla, Z_malla = generar_malla_3d(a, b, resolucion=60)
        
        # Renderizamos con tu configuración de Plotly
        fig = go.Figure(data=[go.Surface(x=X_malla, y=Y_malla, z=Z_malla, colorscale='Blues', opacity=0.7)])
        
        fig.update_layout(
            scene=dict(
                xaxis_title='Eje X', 
                yaxis_title='Eje Y', 
                zaxis_title='Eje Z',
                aspectratio=dict(x=1, y=1, z=b/a)
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)