import numpy as np

def calcular_geodesicas(X, Y, Z, a, b):
    """
    Transformación de coordenadas cartesianas a geodésicas.
    Implementa la solución cerrada de Bowring y maneja casos límite 
    (polos y origen) mediante tolerancia de punto flotante.
    """
    e2 = (a**2 - b**2) / a**2
    ep2 = (a**2 - b**2) / b**2
    
    p = np.sqrt(X**2 + Y**2)
    
    # 1. Caso Límite: Centro del elipsoide (Origen)
    if p < 1e-10 and np.abs(Z) < 1e-10:
        return 0.0, 0.0, -b
        
    # Longitud (Lambda)
    lamb = np.arctan2(Y, X)
    
    # 2. Caso Límite: Los Polos Norte y Sur (p tiende a cero)
    if p < 1e-10:
        phi = np.pi/2 if Z > 0 else -np.pi/2
        h = np.abs(Z) - b
        return phi, lamb, h
        
    # 3. Caso general: Ecuación cerrada de Bowring
    theta_aux = np.arctan2(Z * a, p * b)
    
    numerador = Z + ep2 * b * (np.sin(theta_aux)**3)
    denominador = p - e2 * a * (np.cos(theta_aux)**3)
    
    phi = np.arctan2(numerador, denominador)
    
    N = a / np.sqrt(1 - e2 * (np.sin(phi)**2))
    h = (p / np.cos(phi)) - N
    
    return phi, lamb, h

def generar_malla_3d(a, b, resolucion=50):
    """
    Genera las matrices paramétricas X, Y, Z iterando theta y omega
    para construir y graficar el elipsoide de revolución en 3D.
    """
    theta = np.linspace(-np.pi/2, np.pi/2, resolucion)
    omega = np.linspace(0, 2*np.pi, resolucion)
    
    theta_grid, omega_grid = np.meshgrid(theta, omega)
    
    X_malla = a * np.cos(theta_grid) * np.cos(omega_grid)
    Y_malla = a * np.cos(theta_grid) * np.sin(omega_grid)
    Z_malla = b * np.sin(theta_grid)
    
    return X_malla, Y_malla, Z_malla