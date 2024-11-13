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
    sujeto_actual = partes[0]
    verbo = partes[1]
    if ":" in partes[2]:
    	objeto = partes[2]
    else:
    	objeto = partes[2].strip('"')
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
    verbo = partes[0]
    if ":" in partes[1]:
    	objeto = partes[1]
    else:
    	objeto = partes[1].strip('"')
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


def leer_consulta(consulta):
    """
    Procesa y analiza una consulta SPARQL para extraer variables, condiciones WHERE,
    limit, y order by sin usar expresiones regulares.

    Parameters:
    consulta (str): La consulta SPARQL en formato string.

    Returns:
    dict: Un diccionario con los elementos de la consulta analizados.
    """
    # Inicializar las variables
    variables = []
    condiciones_where = []
    limit = None
    order_by = None

    # Analizar la cláusula SELECT
    partes = consulta.lower().split("select")
    if len(partes) < 2:
        raise ValueError("La consulta debe comenzar con 'SELECT'.")

    select_part = partes[1].strip()
    if "where" in select_part:
        select_part = select_part.split("where")[0].strip()
    variables = [var.strip('?') for var in select_part.split() if var.startswith('?')]

    # Analizar la cláusula WHERE
    if "where" in consulta.lower():
        where_start = consulta.lower().find("where") + len("where")
        where_content = consulta[where_start:].strip()
        
        if '{' not in where_content or '}' not in where_content:
            raise ValueError("La cláusula 'WHERE' debe estar rodeada de llaves '{ }'.")
        
        # Extraer contenido de WHERE entre llaves
        where_content = where_content.split('{', 1)[1].rsplit('}', 1)[0].strip()
        
        # Dividir en tripletas por el separador "."
       
        tripletas = where_content.split('.')
        for tripleta in tripletas:
            tripleta = tripleta.strip()
            if tripleta:
                partes = tripleta.split()
                
                if len(partes) == 3:
                    tripleta = partes
                    condiciones_where.append(tripleta)
                    
    # Analizar LIMIT
    if "limit" in consulta.lower():
        limit_part = consulta.lower().split("limit")[-1].strip()
        try:
            limit = int(limit_part.split()[0])
        except ValueError:
            raise ValueError("El valor de 'LIMIT' debe ser un número entero.")

    # Analizar ORDER BY
    if "order by" in consulta.lower():
        order_part = consulta.lower().split("order by")[-1].strip()
        order_parts = order_part.split()
        if len(order_parts) >= 2:
            order_direction = order_parts[0]
            if order_direction in ("asc", "desc"):
                variable = order_parts[1].strip('()')
                if variable.startswith('?'):
                    order_by = (variable[1:], order_direction)
            else:
                raise ValueError("ORDER BY debe estar seguido de ASC o DESC y una variable entre paréntesis.")

    # Estructurar la consulta analizada
    print(variables, condiciones_where)
    return {
        'variables': variables,
        'condiciones_where': condiciones_where,
        'limit': limit,
        'order_by': order_by
    }


def ejecutar_consulta(base_conocimiento, consulta_parsed):
    """
    Ejecuta la consulta en la base de conocimiento utilizando los criterios proporcionados
    por `consulta_parsed`.

    Parameters:
    base_conocimiento (list): Lista de tripletas en forma de (sujeto, verbo, objeto).
    consulta_parsed (dict): Diccionario con los elementos de la consulta analizados.

    Returns:
    list: Lista de resultados de la consulta.
    """
    variables = consulta_parsed['variables']
    condiciones_where = consulta_parsed['condiciones_where']
    limit = consulta_parsed.get('limit')
    order_by = consulta_parsed.get('order_by')

    resultados = []

    # Iterar sobre las tripletas en la base de conocimiento
    for sujeto, verbo, objeto in base_conocimiento:
        match = True
        bindings = {}

        # Evaluar cada condición en `WHERE`
        for condicion in condiciones_where:
            predicado, valor = re.split(r'\s+', condicion, 1)

            if valor.startswith('?'):
                variable = valor[1:]
                if variable in variables:
                    bindings[variable] = objeto if predicado == verbo else None
            else:
                if valor != objeto:
                    match = False
                    break

        if match:
            # Agregar solo las variables solicitadas en la consulta
            resultado = {var: bindings.get(var, "") for var in variables}
            resultados.append(resultado)

    # Ordenar los resultados si `ORDER BY` está definido
    if order_by:
        variable, direction = order_by
        reverse = direction.lower() == "desc"
        resultados = sorted(resultados, key=lambda x: x.get(variable, ""), reverse=reverse)

    # Aplicar límite si `LIMIT` está definido
    if limit:
        resultados = resultados[:limit]

    return resultados

@click.command()
@click.argument('archivo_base_conocimiento')
def main(archivo_base_conocimiento):
    # Cargar la base de conocimiento desde el archivo especificado
    base_conocimiento = cargar_base_conocimiento(archivo_base_conocimiento)

    while True:
        # Leer el comando de entrada del usuario
        comando = input("SBC_P3> ").strip()

        if comando.startswith("select"):
            try:
                # Procesar la consulta con leer_consulta para obtener su estructura
                consulta_parsed = leer_consulta(comando)
                
                # Ejecutar la consulta en la base de conocimiento usando la estructura obtenida
                resultados = ejecutar_consulta(base_conocimiento, consulta_parsed)
                
                # Mostrar los resultados de la consulta
                if resultados:
                    for resultado in resultados:
                        click.echo("\t".join(f"{var}: {resultado.get(var, '')}" for var in resultado))
                else:
                    click.echo("No se encontraron resultados para la consulta.")
            except ValueError as e:
                click.echo(f"Error en la consulta: {e}")
        
        elif comando.startswith("exit"):
            break

        else:
            click.echo("Comando no reconocido")

if __name__ == '__main__':
    main()
