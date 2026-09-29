import streamlit as st
import plotly.graph_objects as go

def mostrar_modulo(a, b):
    st.title("Módulo C: Proyección Única de Colombia")
    
    # Abstracción visual: Pestañas para separar Directo e Inverso
    tab_directo, tab_inverso = st.tabs(["Problema Directo", "Problema Inverso"])
    
    # --- PESTAÑA 1: PROBLEMA DIRECTO ---
    with tab_directo:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Entrada (Geodésicas a Planas)")
            phi = st.number_input("Latitud (φ)", value=4.0, format="%.6f")
            lam = st.number_input("Longitud (λ)", value=-73.0, format="%.6f")
            st.write("Parámetros del Origen:")
            m_val = st.number_input("Falso Norte/Este (m)", value=5000000.0)
            
            if st.button("Calcular Norte y Este"):
                st.info("Próximamente: Cálculos del Problema Directo.")
                
        with col2:
            mostrar_mapa_colombia("Directo")

    # --- PESTAÑA 2: PROBLEMA INVERSO ---
    with tab_inverso:
        col3, col4 = st.columns([1, 2])
        with col3:
            st.subheader("Entrada (Planas a Geodésicas)")
            norte = st.number_input("Coordenada Norte (N)", value=5000000.0)
            este = st.number_input("Coordenada Este (E)", value=5000000.0)
            st.write("Parámetros del Origen:")
            m_val_inv = st.number_input("Falso Norte/Este (m) ", value=5000000.0)
            
            if st.button("Calcular Latitud y Longitud"):
                st.info("Próximamente: Cálculos del Problema Inverso.")
                
        with col4:
            mostrar_mapa_colombia("Inverso")

# Función auxiliar (abstracción) para no repetir el código del mapa 2D
def mostrar_mapa_colombia(tipo):
    st.subheader(f"Mapa 2D - Territorio Colombiano ({tipo})")
    
    # Mapa básico 2D centrado en Colombia
    fig = go.Figure(go.Scattergeo(
        lon = [-74.0817], lat = [4.6097],
        text = ["Origen Nacional (Aprox)"],
        mode = 'markers',
        marker = dict(size=8, color='red')
    ))
    
    fig.update_geos(
        visible=True, resolution=50,
        showcountries=True, countrycolor="Black",
        showcoastlines=True, coastlinecolor="Black",
        showland=True, landcolor="lightgreen",
        center=dict(lon=-74, lat=4.5), # Centrado en Colombia
        projection_scale=15 # Zoom
    )
    
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=500)
    st.plotly_chart(fig, use_container_width=True)