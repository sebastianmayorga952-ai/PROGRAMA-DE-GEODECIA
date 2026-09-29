import streamlit as st
import numpy as np
import plotly.graph_objects as go

def mostrar_modulo():
    st.title("Módulo A: Transformación de Coordenadas y Elipsoide 3D")
    
    # Dividimos la pantalla en dos columnas
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Entrada de Datos Cartesiana")
        st.write("Ingrese las coordenadas (X, Y, Z):")
        x_val = st.number_input("Coordenada X", value=6378137.0, format="%.4f")
        y_val = st.number_input("Coordenada Y", value=0.0, format="%.4f")
        z_val = st.number_input("Coordenada Z", value=0.0, format="%.4f")
        
        if st.button("Calcular Geodésicas"):
            st.info("Próximamente: Aquí conectaremos el algoritmo para calcular φ, λ, h, ω, θ.")
            
    with col2:
        st.subheader("Visualización del Elipsoide 3D")
        
        # Parámetros del elipsoide (WGS84 por defecto)
        a = 6378137.0  
        b = 6356752.314245 
        
        # Generación de la malla matemática para el 3D
        u = np.linspace(-np.pi/2, np.pi/2, 60)
        v = np.linspace(0, 2*np.pi, 60)
        U, V = np.meshgrid(u, v)
        
        X = a * np.cos(U) * np.cos(V)
        Y = a * np.cos(U) * np.sin(V)
        Z = b * np.sin(U)
        
        # Creación de la figura con Plotly
        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Blues', opacity=0.7)])
        fig.update_layout(
            scene=dict(
                xaxis_title='Eje X', yaxis_title='Eje Y', zaxis_title='Eje Z',
                aspectratio=dict(x=1, y=1, z=b/a)
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            height=500
        )
        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)