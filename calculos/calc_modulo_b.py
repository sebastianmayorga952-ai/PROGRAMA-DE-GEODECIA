import numpy as np

def gms_a_decimal(grados, minutos, segundos):
    """
    Convierte grados, minutos y segundos a grados decimales.
    Maneja correctamente coordenadas negativas (Hemisferio Sur u Oeste).
    """
    signo = -1 if grados < 0 else 1
    return signo * (abs(grados) + (minutos / 60.0) + (segundos / 3600.0))

def calcular_area_elipsoide(phi1_deg, lambda1_deg, phi2_deg, lambda2_deg, a, b):
    """
    Calcula el área física de un cuadrilátero delimitado por dos meridianos 
    y dos paralelos sobre la superficie del elipsoide biaxial.
    Retorna el área en m², km² y Hectáreas.
    """
    # Excentricidad al cuadrado y excentricidad lineal
    e2 = (a**2 - b**2) / a**2
    e = np.sqrt(e2)
    
    # La matemática requiere trabajar en radianes
    phi1 = np.radians(phi1_deg)
    phi2 = np.radians(phi2_deg)
    lambda1 = np.radians(lambda1_deg)
    lambda2 = np.radians(lambda2_deg)
    
    # La diferencia de longitudes determina el ancho del sector
    delta_lambda = abs(lambda2 - lambda1)
    
    # Función de latitud isométrica derivada de la integral de superficie
    def evaluar_q(phi):
        termino1 = np.sin(phi) / (1 - e2 * np.sin(phi)**2)
        
        # Manejo matemático para evitar logaritmos de números negativos
        argumento_ln = (1 + e * np.sin(phi)) / (1 - e * np.sin(phi))
        termino2 = (1 / (2 * e)) * np.log(argumento_ln)
        
        return termino1 + termino2
        
    # Ecuación analítica del área elipsoidal
    area_m2 = (b**2 * delta_lambda / 2.0) * abs(evaluar_q(phi2) - evaluar_q(phi1))
    
    # Conversiones solicitadas en el tablero
    area_km2 = area_m2 / 1_000_000.0
    area_has = area_m2 / 10_000.0
    
    return area_m2, area_km2, area_has