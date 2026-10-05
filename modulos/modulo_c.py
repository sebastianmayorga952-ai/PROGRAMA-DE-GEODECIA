import streamlit as st
import plotly.graph_objects as go

# Importamos ambas funciones matemáticas
from calculos.calc_modulo_c import calcular_directo_ctm12, calcular_inverso_ctm12

def mostrar_modulo(a, b):
    st.title("Módulo C: Proyección Única de Colombia")
    
    tab_directo, tab_inverso = st.tabs(["Problema Directo", "Problema Inverso"])
    
    # --- PESTAÑA 1: PROBLEMA DIRECTO ---
    with tab_directo:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Entrada (Geodésicas a Planas)")
            phi = st.number_input("Latitud (φ) en grados", value=4.0, format="%.6f")
            lam = st.number_input("Longitud (λ) en grados", value=-73.0, format="%.6f")
            st.write("Parámetros del Origen CTM12:")
            st.info("Falso Norte: 2,000,000 m\n\nFalso Este: 5,000,000 m")
            
            lat_plot_dir, lon_plot_dir = None, None
            
            if st.button("Calcular Norte y Este", type="primary"):
                este, norte = calcular_directo_ctm12(phi, lam, a, b)
                st.success("✅ Problema Directo Exitoso")
                st.markdown(f"**Este (X):** `{este:,.3f} m` \n\n**Norte (Y):** `{norte:,.3f} m`")
                lat_plot_dir, lon_plot_dir = phi, lam
                
        with col2:
            mostrar_mapa_colombia("Directo", lat_punto=lat_plot_dir, lon_punto=lon_plot_dir)

    # --- PESTAÑA 2: PROBLEMA INVERSO ---
    with tab_inverso:
        col3, col4 = st.columns([1, 2])
        with col3:
            st.subheader("Entrada (Planas a Geodésicas)")
            este_inv = st.number_input("Coordenada Este (E) en metros", value=5000000.0, format="%.3f")
            norte_inv = st.number_input("Coordenada Norte (N) en metros", value=2000000.0, format="%.3f")
            st.write("Parámetros del Origen CTM12:")
            st.info("Falso Norte: 2,000,000 m\n\nFalso Este: 5,000,000 m")
            
            lat_plot_inv, lon_plot_inv = None, None
            
            if st.button("Calcular Latitud y Longitud", type="primary", key="btn_inverso"):
                lat_calc, lon_calc = calcular_inverso_ctm12(este_inv, norte_inv, a, b)
                st.success("✅ Problema Inverso Exitoso")
                st.markdown(f"**Latitud (φ):** `{lat_calc:.8f}°` \n\n**Longitud (λ):** `{lon_calc:.8f}°`")
                lat_plot_inv, lon_plot_inv = lat_calc, lon_calc
                
        with col4:
            mostrar_mapa_colombia("Inverso", lat_punto=lat_plot_inv, lon_punto=lon_plot_inv)

def mostrar_mapa_colombia(tipo, lat_punto=None, lon_punto=None):
    st.subheader(f"Mapa 2D - Territorio Colombiano ({tipo})")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scattergeo(
        lon = [-73.0], lat = [4.0],
        text = ["Origen Nacional CTM12"],
        mode = 'markers',
        name = 'Origen',
        marker = dict(size=10, color='red', symbol='star')
    ))
    
    if lat_punto is not None and lon_punto is not None:
        fig.add_trace(go.Scattergeo(
            lon = [lon_punto], lat = [lat_punto],
            text = ["Punto Calculado"],
            mode = 'markers',
            name = 'Punto',
            marker = dict(size=8, color='blue')
        ))
    
    fig.update_geos(
        visible=True, resolution=50,
        showcountries=True, countrycolor="Black",
        showcoastlines=True, coastlinecolor="Black",
        showland=True, landcolor="lightgreen",
        center=dict(lon=-74, lat=4.5),
        projection_scale=15
    )
    
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=500, showlegend=True)
    st.plotly_chart(fig, use_container_width=True, key=tipo)