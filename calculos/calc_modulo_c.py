import numpy as np

def calcular_origen_nacional(phi_deg, lambda_deg, a, b):
    """
    Convierte coordenadas geodésicas (Lat, Lon) a planas (Este, Norte)
    utilizando las ecuaciones de Transversa de Mercator para la 
    Proyección Única de Colombia (CTM12 - Origen Nacional).
    """
    # 1. Parámetros Oficiales del Origen Nacional de Colombia (CTM12)
    phi0_deg = 4.0        # Latitud del origen (4° 0' 0" N)
    lambda0_deg = -73.0   # Longitud del origen (73° 0' 0" W)
    k0 = 0.9992           # Factor de escala en el meridiano central
    FE = 5000000.0        # Falso Este (m)
    FN = 2000000.0        # Falso Norte (m)

    # Conversión de grados a radianes para operar trigonométricamente
    phi = np.radians(phi_deg)
    lambda_rad = np.radians(lambda_deg)
    phi0 = np.radians(phi0_deg)
    lambda0 = np.radians(lambda0_deg)

    # 2. Propiedades del Elipsoide (Excentricidad al cuadrado y prima al cuadrado)
    e2 = (a**2 - b**2) / a**2
    ep2 = (a**2 - b**2) / b**2

    # 3. Cálculo de la Distancia Meridiana M(phi)
    # Desarrollo en series para mayor precisión geodésica
    def calcular_M(lat):
        term1 = 1 - e2/4 - 3*e2**2/64 - 5*e2**3/256
        term2 = 3*e2/8 + 3*e2**2/32 + 45*e2**3/1024
        term3 = 15*e2**2/256 + 45*e2**3/1024
        term4 = 35*e2**3/3072
        
        M = a * (term1 * lat - term2 * np.sin(2*lat) + term3 * np.sin(4*lat) - term4 * np.sin(6*lat))
        return M

    M = calcular_M(phi)
    M0 = calcular_M(phi0)

    # 4. Variables intermedias de la proyección
    N = a / np.sqrt(1 - e2 * np.sin(phi)**2) # Gran Normal
    T = np.tan(phi)**2
    C = ep2 * np.cos(phi)**2
    A = (lambda_rad - lambda0) * np.cos(phi)

    # 5. Cálculo de la Coordenada Este (X plana)
    term_E1 = A
    term_E2 = (1 - T + C) * (A**3 / 6.0)
    term_E3 = (5 - 18*T + T**2 + 72*C - 58*ep2) * (A**5 / 120.0)
    Este = FE + k0 * N * (term_E1 + term_E2 + term_E3)

    # 6. Cálculo de la Coordenada Norte (Y plana)
    term_N1 = M - M0
    term_N2 = N * np.tan(phi) * (A**2 / 2.0)
    term_N3 = N * np.tan(phi) * (5 - T + 9*C + 4*C**2) * (A**4 / 24.0)
    term_N4 = N * np.tan(phi) * (61 - 58*T + T**2 + 600*C - 330*ep2) * (A**6 / 720.0)
    Norte = FN + k0 * (term_N1 + term_N2 + term_N3 + term_N4)

    return Este, Norte

# --- BLOQUE DE PRUEBAS ---
if __name__ == "__main__":
    # Parámetros WGS84
    a_wgs = 6378137.0
    b_wgs = 6356752.3142
    
    # Prueba clásica: Proyectar el mismo origen
    # Si metemos 4°N y -73°W, debe devolver exactamente los falsos orígenes
    E, N = calcular_origen_nacional(4.0, -73.0, a_wgs, b_wgs)
    
    print("\n--- PRUEBA MÓDULO C ---")
    print(f"Coordenadas calculadas en el origen (4°N, -73°W):")
    print(f"Este (E): {E:,.3f} m (Debería ser 5,000,000.000)")
    print(f"Norte (N): {N:,.3f} m (Debería ser 2,000,000.000)\n")