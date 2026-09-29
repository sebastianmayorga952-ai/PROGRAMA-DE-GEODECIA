import streamlit as st
import numpy as np
import plotly.graph_objects as go

def mostrar_modulo(a, b):
    st.title("Módulo B: Área de un cuadrilátero en el elipsoide")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Entrada de Datos (Geodésicas)")
        
        st.write("**Punto 1 (Inferior Izquierdo):**")
        phi_1 = st.number_input("Latitud (φ1)", value=0.0, format="%.6f")
        lam_1 = st.number_input("Longitud (λ1)", value=0.0, format="%.6f")
        
        st.write("**Punto 2 (Superior Derecho):**")
        phi_2 = st.number_input("Latitud (φ2)", value=5.0, format="%.6f")
        lam_2 = st.number_input("Longitud (λ2)", value=-74.0, format="%.6f")
        
        if st.button("Calcular Área"):
            st.info("Próximamente: Algoritmo para cálculo de área en Km² y Hectáreas.")
            
    with col2:
        st.subheader("Visualización 3D del Cuadrilátero")
        
        # Generamos la base del elipsoide para cumplir el requisito de rotación 3D
        u = np.linspace(-np.pi/2, np.pi/2, 60)
        v = np.linspace(0, 2*np.pi, 60)
        U, V = np.meshgrid(u, v)
        
        X = a * np.cos(U) * np.cos(V)
        Y = a * np.cos(U) * np.sin(V)
        Z = b * np.sin(U)
        
        # Usamos un color verde para diferenciar este módulo
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