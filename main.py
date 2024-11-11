import re
import click
import re
import click

def cargar_tripleta_con_sujeto(partes):
    """
    Carga una tripleta con un sujeto explícito.

    Parameters:
    partes (list): Partes de la línea que contienen el sujeto, verbo y objeto.

    Returns:
    tuple: Una tripleta en forma de (sujeto, verbo, objeto).
    """
    sujeto_actual = partes[0].split(":")[1]
    verbo = partes[1].split(":")[1]
    objeto = partes[2].split(":")[1] if ":" in partes[2] else partes[2].strip('"')
    return (sujeto_actual, verbo, objeto)

def cargar_tripleta_sin_sujeto(partes):
    """
    Carga una tripleta sin un sujeto explícito, donde el verbo y el objeto
    son continuaciones de la tripleta anterior.

    Parameters:
    partes (list): Partes de la línea que contienen el verbo y el objeto.

    Returns:
    tuple: Una tripleta parcial en forma de (verbo, objeto), sin el sujeto.
    """
    verbo = partes[0].split(":")[1]
    objeto = partes[1].split(":")[1] if ":" in partes[1] else partes[1].strip('"')
    return (verbo, objeto)

def cargar_base_conocimiento(archivo):
    """
    Carga la base de conocimiento desde un archivo, procesando cada línea
    en tripletas de la forma (sujeto, verbo, objeto).

    Cada tripleta se construye de acuerdo al sujeto presente en la línea.
    Las líneas terminadas en ';' continúan el mismo sujeto, mientras que las
    que terminan en '.' reinician el sujeto.

    Parameters:
    archivo (str): La ruta del archivo de la base de conocimiento.

    Returns:
    list: Lista de tripletas en forma de (sujeto, verbo, objeto).
    """
    base_conocimiento = []
    sujeto_actual = None  # Guarda el sujeto mientras se construyen tripletas relacionadas

    with open(archivo, 'r') as f:
        for linea in f:
            # Ignorar comentarios y líneas vacías
            linea = linea.strip()
            if linea.startswith("#") or not linea:
                continue

            # Separar la línea en partes de la tripleta
            partes = linea.split()
            if len(partes) < 3:
                continue  # Si no tiene suficientes partes, ignora la línea

            # Extraer el sujeto, verbo y objeto
            if sujeto_actual is None:  # Si no hay sujeto actual, toma uno nuevo
                sujeto_actual, verbo, objeto = cargar_tripleta_con_sujeto(partes)
            else:
                verbo, objeto = cargar_tripleta_sin_sujeto(partes)

            base_conocimiento.append((sujeto_actual, verbo, objeto))

            # Actualizar el sujeto según el fin de la línea
            if linea.endswith('.'):
                sujeto_actual = None  # Reiniciar el sujeto si la línea termina en "."
            elif linea.endswith(';'):
                continue  # Continuar con el mismo sujeto para la siguiente línea
            else:
                raise ValueError("Formato de línea inesperado: debe terminar en ';' o '.'")

    return base_conocimiento


# Función para ejecutar la consulta
def ejecutar_consulta(base_conocimiento, consulta):
    # Parsear consulta (simplificada)
    variables = re.findall(r'\?(\w+)', consulta)  # Extraer variables del 'select'

    # Obtener la cláusula where y quitar los espacios innecesarios
    where_clause = re.search(r'where\s*\{(.*?)\}', consulta, re.DOTALL)

    if where_clause:
        where_clause = where_clause.group(1).strip()
    else:
        raise ValueError("La cláusula 'where' no está bien definida en la consulta")

    # Inicializar resultados
    resultados = []

    # Iterar sobre las tripletas de la base de conocimiento
    for sujeto, verbo, objeto in base_conocimiento:
        match = True
        bindings = {}

        # Procesar la cláusula where
        for tripleta in where_clause.split('.'):
            tripleta = tripleta.strip()
            if not tripleta:
                continue
            predicado, valor = re.split(r'\s+', tripleta, 1)

            # Si el valor es una variable
            if valor.startswith('?'):
                variable = valor[1:]
                if variable in variables:
                    bindings[variable] = objeto if predicado == verbo else None
            else:
                # Comparar con el valor literal
                if valor != objeto:
                    match = False
                    break

        if match:
            # Si la tripleta coincide, se añade a los resultados
            # Solo devolver las variables que estaban en la consulta
            result = {var: bindings.get(var, "") for var in variables}
            resultados.append(result)

    return resultados

@click.command()
@click.argument('archivo_base_conocimiento')
def main(archivo_base_conocimiento):
    base_conocimiento = cargar_base_conocimiento(archivo_base_conocimiento)
    click.echo(f"Base de conocimiento cargada: {base_conocimiento}")

    while True:
        comando = input("SBC_P3> ").strip()
        if comando.startswith("select"):
            # Ejecutar la consulta
            resultados = ejecutar_consulta(base_conocimiento, comando)
            if resultados:
                for resultado in resultados:
                    # Mostrar solo las variables solicitadas en la consulta
                    click.echo("\t".join(f"{var}: {resultado.get(var, '')}" for var in resultado))
            else:
                click.echo("No se encontraron resultados para la consulta.")
        elif comando.startswith("exit"):
            break
        else:
            click.echo("Comando no reconocido")

if __name__ == '__main__':
    main()
