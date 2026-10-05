import numpy as np

def calcular_directo_ctm12(phi_deg, lambda_deg, a, b):
    """
    Problema Directo: Convierte Latitud y Longitud a Norte y Este 
    usando el Origen Nacional Único de Colombia (CTM12).
    """
    # Parámetros Oficiales del Origen Nacional
    phi0_deg = 4.0        # Latitud del origen
    lambda0_deg = -73.0   # Longitud del origen
    k0 = 0.9992           # Factor de escala
    FE = 5000000.0        # Falso Este
    FN = 2000000.0        # Falso Norte

    # Conversión a radianes
    phi = np.radians(phi_deg)
    lambda_rad = np.radians(lambda_deg)
    phi0 = np.radians(phi0_deg)
    lambda0 = np.radians(lambda0_deg)

    e2 = (a**2 - b**2) / a**2
    ep2 = (a**2 - b**2) / b**2

    # Cálculo de la Distancia Meridiana
    def calcular_M(lat):
        term1 = 1 - e2/4 - 3*e2**2/64 - 5*e2**3/256
        term2 = 3*e2/8 + 3*e2**2/32 + 45*e2**3/1024
        term3 = 15*e2**2/256 + 45*e2**3/1024
        term4 = 35*e2**3/3072
        return a * (term1 * lat - term2 * np.sin(2*lat) + term3 * np.sin(4*lat) - term4 * np.sin(6*lat))

    M = calcular_M(phi)
    M0 = calcular_M(phi0)

    # Variables de proyección
    N = a / np.sqrt(1 - e2 * np.sin(phi)**2)
    T = np.tan(phi)**2
    C = ep2 * np.cos(phi)**2
    A = (lambda_rad - lambda0) * np.cos(phi)

    # Coordenadas finales
    Este = FE + k0 * N * (A + (1 - T + C) * (A**3 / 6.0) + (5 - 18*T + T**2 + 72*C - 58*ep2) * (A**5 / 120.0))
    Norte = FN + k0 * (M - M0 + N * np.tan(phi) * (A**2 / 2.0 + (5 - T + 9*C + 4*C**2) * (A**4 / 24.0) + (61 - 58*T + T**2 + 600*C - 330*ep2) * (A**6 / 720.0)))

    return Este, Norte

def calcular_inverso_ctm12(este, norte, a, b):
    """
    Problema Inverso: Convierte coordenadas Planas (Este, Norte) 
    a Geodésicas (Latitud, Longitud) en el sistema CTM12.
    """
    # Parámetros Oficiales CTM12
    phi0_deg = 4.0
    lambda0_deg = -73.0
    k0 = 0.9992
    FE = 5000000.0
    FN = 2000000.0

    phi0 = np.radians(phi0_deg)
    lambda0 = np.radians(lambda0_deg)

    e2 = (a**2 - b**2) / a**2
    ep2 = (a**2 - b**2) / b**2

    # 1. Distancia Meridiana del Origen
    def calcular_M(lat):
        term1 = 1 - e2/4 - 3*e2**2/64 - 5*e2**3/256
        term2 = 3*e2/8 + 3*e2**2/32 + 45*e2**3/1024
        term3 = 15*e2**2/256 + 45*e2**3/1024
        term4 = 35*e2**3/3072
        return a * (term1 * lat - term2 * np.sin(2*lat) + term3 * np.sin(4*lat) - term4 * np.sin(6*lat))

    M0 = calcular_M(phi0)

    # 2. Desproyectar usando el factor de escala
    E_prima = (este - FE) / k0
    N_prima = (norte - FN) / k0
    M = M0 + N_prima

    # 3. Cálculo de la Latitud Pie (Latitud de la base de la normal)
    e1 = (1 - np.sqrt(1 - e2)) / (1 + np.sqrt(1 - e2))
    mu = M / (a * (1 - e2/4 - 3*e2**2/64 - 5*e2**3/256))
    
    phi_f = mu + (3*e1/2 - 27*e1**3/32)*np.sin(2*mu) + (21*e1**2/16 - 55*e1**4/32)*np.sin(4*mu) + (151*e1**3/96)*np.sin(6*mu)

    # 4. Parámetros del elipsoide evaluados en la Latitud Pie (phi_f)
    N_f = a / np.sqrt(1 - e2 * np.sin(phi_f)**2)
    R_f = a * (1 - e2) / (1 - e2 * np.sin(phi_f)**2)**(3/2)
    T_f = np.tan(phi_f)**2
    C_f = ep2 * np.cos(phi_f)**2
    D = E_prima / N_f

    # 5. Cálculo final de Latitud y Longitud
    term_lat1 = (D**2 / 2.0)
    term_lat2 = (5 + 3*T_f + 10*C_f - 4*C_f**2 - 9*ep2) * (D**4 / 24.0)
    term_lat3 = (61 + 90*T_f + 298*C_f + 45*T_f**2 - 252*ep2 - 3*C_f**2) * (D**6 / 720.0)
    
    phi_rad = phi_f - (N_f * np.tan(phi_f) / R_f) * (term_lat1 - term_lat2 + term_lat3)

    term_lon1 = D
    term_lon2 = (1 + 2*T_f + C_f) * (D**3 / 6.0)
    term_lon3 = (5 - 2*C_f + 28*T_f - 3*C_f**2 + 8*ep2 + 24*T_f**2) * (D**5 / 120.0)
    
    lambda_rad = lambda0 + (term_lon1 - term_lon2 + term_lon3) / np.cos(phi_f)

    # Convertir a grados decimales
    return np.degrees(phi_rad), np.degrees(lambda_rad)