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

"""def cargar_base_conocimiento(archivo):
    
    Carga la base de conocimiento desde un archivo, procesando cada línea
    en tripletas de la forma (sujeto, verbo, objeto).
    
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
"""
def cargar_base_conocimiento(archivo, base_conocimiento, base_combinada):
    """
    Carga la base de conocimiento desde un archivo, procesando cada línea
    en tripletas de la forma (sujeto, verbo, objeto).
    """
    sujeto_actual = None
    base_x = []
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

            tripleta = (sujeto_actual, verbo, objeto)

            if tripleta not in base_conocimiento and tripleta not in base_combinada and tripleta not in base_x:
                base_x.append(tripleta)

            if linea.endswith('.'):
                sujeto_actual = None
            elif linea.endswith(';'):
                continue
            else:
                raise ValueError("Formato de línea inesperado: debe terminar en ';' o '.'")

    return base_x

def cargar_multiples_bases_conocimiento(archivos, base_conocimiento):
    """
    Carga y combina múltiples bases de conocimiento en una sola lista.
    """

    base_combinada = []
    for archivo in archivos:
        try:
            base_variable = []
            base_variable = cargar_base_conocimiento(archivo, base_conocimiento, base_combinada)
            base_combinada = base_combinada + base_variable
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {archivo}")
    return base_combinada

def load(comando, base_conocimiento):
    """
    Carga una base de conocimiento desde un archivo, evitando duplicados en el sistema.
    """
    base_anadida = []
    partes = comando.split(' ', 1)
    archivos = partes[1].strip()
    archivos = archivos.split()
    base_anadida = cargar_multiples_bases_conocimiento(archivos, base_conocimiento)
    print("OK!")

    return base_anadida


def imprimir_base_conocimiento(base_conocimiento):
    """
    Imprime todas las tripletas de la base de conocimiento con un formato alineado.
    """
    if not base_conocimiento:
        print("La base de conocimiento está vacía.")
        return

    # Imprimir encabezado
    print(f"{'Sujeto':<20} {'Verbo':<20} {'Objeto'}")
    print("="*60)

    # Imprimir cada tripleta
    for tripleta in base_conocimiento:
        if len(tripleta) == 3:
            sujeto, verbo, objeto = tripleta
            # Imprimir las tripletas con espacio alineado
            print(f"{sujeto:<20} {verbo:<20} {objeto}")
