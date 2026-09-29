# Diccionario con los 10 elipsoides exigidos.
# 'a' es el semieje mayor en metros.
# 'rf' es el inverso del achatamiento (1/f).

DICCIONARIO_ELIPSOIDES = {
    "WGS 84": {"a": 6378137.0, "rf": 298.257223563},
    "GRS 80": {"a": 6378137.0, "rf": 298.257222101},
    "Internacional 1924 (Hayford)": {"a": 6378388.0, "rf": 297.0},
    "Clarke 1866": {"a": 6378206.4, "rf": 294.9786982},
    "Krassovsky 1940": {"a": 6378245.0, "rf": 298.3},
    "Bessel 1841": {"a": 6377397.155, "rf": 299.1528128},
    "WGS 72": {"a": 6378135.0, "rf": 298.26},
    "GRS 67": {"a": 6378160.0, "rf": 298.247167427},
    "Clarke 1880": {"a": 6378249.145, "rf": 293.465},
    "Everest 1830": {"a": 6377276.345, "rf": 300.8017}
}

def obtener_parametros(nombre_elipsoide):
    """
    Recibe el nombre del elipsoide y calcula los parámetros faltantes.
    Retorna: a (semieje mayor), b (semieje menor), f (achatamiento), e2 (excentricidad al cuadrado).
    """
    a = DICCIONARIO_ELIPSOIDES[nombre_elipsoide]["a"]
    rf = DICCIONARIO_ELIPSOIDES[nombre_elipsoide]["rf"]
    
    f = 1.0 / rf
    b = a * (1.0 - f)
    e2 = 2*f - f**2  # Primera excentricidad al cuadrado (fundamental para las fórmulas después)
    
    return a, b, f, e2