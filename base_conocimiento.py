# base_conocimiento.py

import click

# Funciones necesarias para cargar una base de conocimiento
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


def cargar_base_conocimiento(archivo, base_conocimiento, base_combinada):
    """
    Carga la base de conocimiento desde un archivo, procesando cada línea
    en tripletas de la forma (sujeto, verbo, objeto), y agrupando las tripletas
    de un mismo sujeto.
    """
    sujetos = {}  # Diccionario para agrupar las tripletas por sujeto
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

            tripleta = (sujeto_actual, verbo, objeto)

            # Agrupar las tripletas por sujeto
            if sujeto_actual not in sujetos:
                sujetos[sujeto_actual] = []
            sujetos[sujeto_actual].append(tripleta)

            if linea.endswith('.'):
                sujeto_actual = None
            elif linea.endswith(';'):
                continue
            else:
                raise ValueError("Formato de línea inesperado: debe terminar en ';' o '.'")

    # Al final, combinamos todas las tripletas agrupadas en una lista
    base_x = []
    for sujeto, tripletas_sujeto in sujetos.items():
        base_x.extend(tripletas_sujeto)

    return base_x


#Función para cargar más de una base de conocimiento a la vez
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



