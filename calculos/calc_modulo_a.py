import numpy as np

def calcular_geodesicas(X, Y, Z, a, b):
    """
    Recibe cartesianas y semiejes.
    Retorna phi (radianes), lambda (radianes) y h (metros).
    """
    e2 = (a**2 - b**2) / a**2
    ep2 = (a**2 - b**2) / b**2
    
    p = np.sqrt(X**2 + Y**2)
    
    # Manejo de error si el punto está en el centro de la tierra
    if p == 0 and Z == 0:
        return 0.0, 0.0, 0.0
        
    lamb = np.arctan2(Y, X)
    
    theta_aux = np.arctan((Z * a) / (p * b))
    
    numerador = Z + ep2 * b * (np.sin(theta_aux)**3)
    denominador = p - e2 * a * (np.cos(theta_aux)**3)
    phi = np.arctan(numerador / denominador)
    
    N = a / np.sqrt(1 - e2 * (np.sin(phi)**2))
    h = (p / np.cos(phi)) - N
    
    return phi, lamb, h

def generar_malla_3d(a, b, resolucion=50):
    """
    Genera las matrices paramétricas para graficar el elipsoide.
    """
    theta = np.linspace(-np.pi/2, np.pi/2, resolucion)
    omega = np.linspace(0, 2*np.pi, resolucion)
    
    theta_grid, omega_grid = np.meshgrid(theta, omega)
    
    X_malla = a * np.cos(theta_grid) * np.cos(omega_grid)
    Y_malla = a * np.cos(theta_grid) * np.sin(omega_grid)
    Z_malla = b * np.sin(theta_grid)
    
    return X_malla, Y_malla, Z_malla