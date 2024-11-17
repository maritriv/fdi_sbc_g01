# base_conocimiento.py

import click


# Función para cargar una base de conocimiento
def cargar_base_conocimiento(archivo, tripletas_unicas):
    """
    Carga la base de conocimiento desde un archivo, procesando cada línea
    en tripletas de la forma (sujeto, verbo, objeto), y agrupando las tripletas
    por sujeto incluso si no están consecutivas en el archivo.
    """
    sujetos = {}  # Diccionario para agrupar las tripletas por sujeto
    sujeto = None

    # Apertura del archivo
    with open(archivo, "r") as f:
        # Lectura de cada línea
        for linea in f:
            linea = linea.strip()
            if linea.startswith("#") or not linea:
                continue

            # Dividir la línea en partes (sujeto, verbo, objeto)
            partes = linea.split()
            if len(partes) < 3:
                continue

            # Línea con sujeto
            if len(partes) == 4:
                sujeto = partes[0]
                verbo = partes[1]
                objeto = partes[2]
            else:
                if sujeto is None:
                    raise ValueError(
                        "No se puede interpretar la linea: falta el sujeto."
                    )
                # Línea sin sujeto
                verbo = partes[0]
                objeto = partes[1]

            # Crear la tripleta
            tripleta = (sujeto, verbo, objeto)

            # Agrupar las tripletas por sujeto si son únicas
            if tripleta not in tripletas_unicas:
                if sujeto not in sujetos:
                    sujetos[sujeto] = []
                sujetos[sujeto].append(tripleta)
                tripletas_unicas.add(tripleta)

            # Actualizar el sujeto según el terminador
            if linea.endswith("."):
                sujeto_actual = None  # Termina el grupo de tripletas para este sujeto
            elif linea.endswith(";"):
                continue  # Continuar con el mismo sujeto

    # Combinar todas las tripletas agrupadas en una lista
    base_x = []
    for sujeto, tripletas_sujeto in sujetos.items():
        base_x.extend(tripletas_sujeto)

    return base_x


# Función para cargar más de una base de conocimiento a la vez
def cargar_multiples_bases_conocimiento(archivos, base_conocimiento):
    """
    Carga y combina múltiples bases de conocimiento en una sola lista.
    """
    tripletas_unicas = set(base_conocimiento)
    base_combinada = []
    for archivo in archivos:
        try:
            base_combinada = cargar_base_conocimiento(archivo, tripletas_unicas)
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {archivo}")
    return base_combinada


# Función para cargar una o varias bases de conocimiento por primera vez
def cargar_bases_conocimiento(archivos_base_conocimiento):
    """
    Carga las bases de conocimiento desde los archivos especificados.

    :param archivos_base_conocimiento: Lista de archivos a cargar.
    :return: Lista combinada de bases de conocimiento.
    """
    if not archivos_base_conocimiento:
        click.echo("Debes especificar al menos un archivo de base de conocimiento.")
        return []

    try:
        return cargar_multiples_bases_conocimiento(archivos_base_conocimiento, [])
    except FileNotFoundError as e:
        click.echo(f"Error al cargar los archivos: {e}")
        return []
