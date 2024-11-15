import re

def procesar_select(consulta):
    """
    Procesa la parte SELECT de la consulta para extraer las variables.
    """
    partes = consulta.lower().split("select")
    if len(partes) < 2:
        raise ValueError("La consulta debe comenzar con 'SELECT'.")
    
    select_part = partes[1].strip()
    if "where" in select_part:
        select_part = select_part.split("where")[0].strip()
    
    variables = [var.strip('?') for var in select_part.split() if var.startswith('?')]
    return variables


def procesar_where(consulta):
    """
    Procesa la parte WHERE de la consulta para extraer las condiciones.
    """
    if "where" not in consulta.lower():
        raise ValueError("La consulta debe contener una cláusula 'WHERE'.")

    where_start = consulta.lower().find("where") + len("where")
    where_content = consulta[where_start:].strip()

    if '{' not in where_content or '}' not in where_content:
        raise ValueError("La cláusula 'WHERE' debe estar rodeada de llaves '{ }'.")

    where_content = where_content.split('{', 1)[1].rsplit('}', 1)[0].strip()
    tripletas = where_content.split('.')
    
    condiciones_where = []
    for tripleta in tripletas:
        tripleta = tripleta.strip()
        if tripleta:
            partes = tripleta.split()
            if len(partes) == 3:
                condiciones_where.append(partes)
    
    return condiciones_where


def procesar_limit(consulta):
    """
    Procesa la parte LIMIT de la consulta para extraer el valor.
    """
    if "limit" in consulta.lower():
        limit_part = consulta.lower().split("limit")[-1].strip()
        try:
            return int(limit_part.split()[0])
        except ValueError:
            raise ValueError("El valor de 'LIMIT' debe ser un número entero.")
    return None


def procesar_order_by(consulta):
    """
    Procesa la parte ORDER BY de la consulta para extraer la variable y la dirección.
    """
    if "order by" in consulta.lower():
        order_part = consulta.lower().split("order by")[-1].strip()
        order_parts = order_part.split()
        if len(order_parts) >= 2:
            order_direction = order_parts[0]
            if order_direction in ("asc", "desc"):
                variable = order_parts[1].strip('()')
                if variable.startswith('?'):
                    return (variable[1:], order_direction)
            else:
                raise ValueError("ORDER BY debe estar seguido de ASC o DESC y una variable entre paréntesis.")
    return None


def leer_consulta(consulta):
    """
    Procesa y analiza una consulta SPARQL para extraer variables, condiciones WHERE,
    limit, y order by.
    """
    variables = procesar_select(consulta)
    condiciones_where = procesar_where(consulta)
    limit = procesar_limit(consulta)
    order_by = procesar_order_by(consulta)

    return {
        'variables': variables,
        'condiciones_where': condiciones_where,
        'limit': limit,
        'order_by': order_by
    }


def ejecutar_consulta(base_conocimiento, consulta_parsed):
    """
    Ejecuta la consulta en la base de conocimiento utilizando los criterios proporcionados.
    """
    variables = consulta_parsed['variables']
    condiciones_where = consulta_parsed['condiciones_where']
    limit = consulta_parsed.get('limit')
    order_by = consulta_parsed.get('order_by')

    resultados = []

    # Iterar sobre las tripletas en la base de conocimiento
    for sujeto, verbo, objeto in base_conocimiento:
        bindings = {}
        match = True

        # Evaluar cada condición en `WHERE`
        for condicion in condiciones_where:
            sujeto_cond, verbo_cond, objeto_cond = condicion

            if sujeto_cond.startswith('?'):  # Es una variable
                if sujeto_cond[1:] not in bindings:
                    bindings[sujeto_cond[1:]] = sujeto
                elif bindings[sujeto_cond[1:]] != sujeto:
                    match = False

            elif sujeto_cond != sujeto:
                match = False

            if verbo_cond.startswith('?'):  # Es una variable
                if verbo_cond[1:] not in bindings:
                    bindings[verbo_cond[1:]] = verbo
                elif bindings[verbo_cond[1:]] != verbo:
                    match = False

            elif verbo_cond != verbo:
                match = False

            if objeto_cond.startswith('?'):  # Es una variable
                if objeto_cond[1:] not in bindings:
                    bindings[objeto_cond[1:]] = objeto
                elif bindings[objeto_cond[1:]] != objeto:
                    match = False

            elif objeto_cond != objeto:
                match = False

            if not match:
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


