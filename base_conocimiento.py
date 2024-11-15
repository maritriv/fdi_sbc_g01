# base_conocimiento.py

def cargar_tripleta_con_sujeto(partes):
    """
    Carga una tripleta con un sujeto explícito.
    """
    sujeto_actual = partes[0]
    verbo = partes[1]
    objeto = partes[2]
    return (sujeto_actual, verbo, objeto)


def cargar_tripleta_sin_sujeto(partes):
    """
    Carga una tripleta sin un sujeto explícito.
    """
    verbo = partes[0]
    objeto = partes[1]
    return (verbo, objeto)


def cargar_base_conocimiento(archivo):
    """
    Carga la base de conocimiento desde un archivo, procesando cada línea
    en tripletas de la forma (sujeto, verbo, objeto).
    """
    base_conocimiento = []
    sujeto_actual = None

    with open(archivo, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if linea.startswith("#") or not linea:
                continue

            partes = linea.split()
            if len(partes) < 3:
                continue

            if sujeto_actual is None:
                sujeto_actual, verbo, objeto = cargar_tripleta_con_sujeto(partes)
            else:
                verbo, objeto = cargar_tripleta_sin_sujeto(partes)

            base_conocimiento.append((sujeto_actual, verbo, objeto))

            if linea.endswith('.'):
                sujeto_actual = None
            elif linea.endswith(';'):
                continue
            else:
                raise ValueError("Formato de línea inesperado: debe terminar en ';' o '.'")

    return base_conocimiento

def cargar_multiples_bases_conocimiento(archivos):
    """
    Carga y combina múltiples bases de conocimiento en una sola lista.
    """
    base_combinada = []
    for archivo in archivos:
        try:
            base_combinada.extend(cargar_base_conocimiento(archivo))
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {archivo}")
    return base_combinada