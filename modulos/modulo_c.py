import streamlit as st
import plotly.graph_objects as go

# Importamos el motor matemático del Módulo C
from calculos.calc_modulo_c import calcular_origen_nacional

def mostrar_modulo(a, b):
    st.title("Módulo C: Proyección Única de Colombia (CTM12)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Entrada de Datos Geodésicos")
        st.write("Ingrese las coordenadas a proyectar:")
        
        # Por defecto dejamos las coordenadas del origen (4°N, 73°W)
        phi = st.number_input("Latitud (φ) en grados decimales", value=4.000000, format="%.6f")
        lam = st.number_input("Longitud (λ) en grados decimales", value=-73.000000, format="%.6f")
        
        if st.button("Calcular Coordenadas Planas", type="primary"):
            # 1. Llamamos a la matemática pura
            este, norte = calcular_origen_nacional(phi, lam, a, b)
            
            # 2. Guardamos en el estado de Streamlit para que el gráfico no se borre al interactuar
            st.session_state['este_c'] = este
            st.session_state['norte_c'] = norte
            
            # 3. Mostramos resultados
            st.success("✅ Proyección exitosa")
            st.markdown(f"""
            - **Este (X):** `{este:,.3f} m`
            - **Norte (Y):** `{norte:,.3f} m`
            """)
            
    with col2:
        st.subheader("Visualización en Plano Cartesiano")
        
        # Recuperamos los datos calculados o usamos el Falso Origen por defecto
        este_plot = st.session_state.get('este_c', 5000000.0)
        norte_plot = st.session_state.get('norte_c', 2000000.0)
        
        fig = go.Figure()
        
        # 1. Dibujamos la estrella roja del Origen Nacional
        fig.add_trace(go.Scatter(
            x=[5000000.0], y=[2000000.0],
            mode='markers+text',
            marker=dict(size=14, color='red', symbol='star'),
            name='Origen Nacional',
            text=['Origen (5M, 2M)'],
            textposition="bottom center"
        ))
        
        # 2. Dibujamos el punto ingresado por el usuario (si es diferente al origen)
        if abs(este_plot - 5000000.0) > 0.1 or abs(norte_plot - 2000000.0) > 0.1:
            fig.add_trace(go.Scatter(
                x=[este_plot], y=[norte_plot],
                mode='markers+text',
                marker=dict(size=10, color='blue', symbol='circle'),
                name='Punto Proyectado',
                text=['Punto Calculado'],
                textposition="top center"
            ))
            
        # Configuramos los ejes del mapa plano
        fig.update_layout(
            xaxis_title='Coordenada Este (m)',
            yaxis_title='Coordenada Norte (m)',
            height=500,
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            margin=dict(l=0, r=0, b=0, t=0)
        )
        
        # Para que los ejes tengan la misma escala geométrica
        fig.update_yaxes(scaleanchor="x", scaleratio=1)
        
        st.plotly_chart(fig, use_container_width=True)