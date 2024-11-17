# Funciones necesarias para leer una consulta

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

    variables = [var.strip("?") for var in select_part.split() if var.startswith("?")]
    return variables


def procesar_where(consulta):
    """
    Procesa la parte WHERE de la consulta para extraer las condiciones.
    """
    if "where" not in consulta.lower():
        raise ValueError("La consulta debe contener una cláusula 'WHERE'.")

    where_start = consulta.lower().find("where") + len("where")
    where_content = consulta[where_start:].strip()

    if "{" not in where_content or "}" not in where_content:
        raise ValueError("La cláusula 'WHERE' debe estar rodeada de llaves '{ }'.")

    where_content = where_content.split("{", 1)[1].rsplit("}", 1)[0].strip()
    tripletas = where_content.split(".")

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



def leer_consulta(consulta):
    """
    Procesa y analiza una consulta SPARQL para extraer variables, condiciones WHERE y
    limit.
    """
    variables = procesar_select(consulta)
    condiciones_where = procesar_where(consulta)
    limit = procesar_limit(consulta)

    return {
        "variables": variables,
        "condiciones_where": condiciones_where,
        "limit": limit,
    }


# Funciones necesarias para ejecutar una consulta

def agrupar_tripletas_por_sujeto(base_conocimiento):
    """
    Agrupa las tripletas por sujeto.
    """
    sujetos = {}
    for sujeto, verbo, objeto in base_conocimiento:
        if sujeto not in sujetos:
            sujetos[sujeto] = []
        sujetos[sujeto].append((verbo, objeto))
    return sujetos


def ejecutar_consulta(base_conocimiento, consulta_parsed):
    """
    Ejecuta una consulta en la base de conocimiento utilizando los criterios proporcionados.

    Esta función procesa una consulta SPARQL simplificada, aplicando los filtros y condiciones 
    especificadas en la cláusula WHERE, y devuelve los resultados que cumplen con las condiciones.

    :param base_conocimiento: Diccionario que representa la base de conocimiento, donde las claves 
                               son los sujetos y los valores son las tripletas asociadas a esos sujetos.
    :param consulta_parsed: Diccionario que representa la consulta procesada, que contiene:
                            - "variables": una lista de las variables solicitadas en la consulta.
                            - "condiciones_where": una lista de tripletas de condiciones para la cláusula WHERE.
                            - "limit": el número máximo de resultados a devolver (opcional).
    :return: Una lista de diccionarios, donde cada diccionario representa un conjunto de resultados con 
             las variables solicitadas.
    """
    variables = consulta_parsed["variables"]
    condiciones_where = consulta_parsed["condiciones_where"]
    limit = consulta_parsed.get("limit")

    resultados = []

    # Agrupar las tripletas por sujeto
    sujetos = agrupar_tripletas_por_sujeto(base_conocimiento)

    # Iterar sobre los sujetos
    for sujeto, tripletas_sujeto in sujetos.items():
        bindings = {}
        match = True

        # Evaluar cada condición en `WHERE`
        for condicion in condiciones_where:
            sujeto_cond, verbo_cond, objeto_cond = condicion

            # Buscar tripletas que cumplan con esta condición
            tripleta_match = False
            for verbo, objeto in tripletas_sujeto:
                # Crear un diccionario temporal para verificar posibles unificaciones
                temp_bindings = bindings.copy()

                # Verificar el sujeto
                if sujeto_cond.startswith("?"):  # Variable
                    if sujeto_cond[1:] not in temp_bindings:
                        temp_bindings[sujeto_cond[1:]] = sujeto
                    elif temp_bindings[sujeto_cond[1:]] != sujeto:
                        continue  # No unifica
                elif sujeto_cond != sujeto:
                    continue  # No unifica

                # Verificar el verbo
                if verbo_cond.startswith("?"):  # Variable
                    if verbo_cond[1:] not in temp_bindings:
                        temp_bindings[verbo_cond[1:]] = verbo
                    elif temp_bindings[verbo_cond[1:]] != verbo:
                        continue  # No unifica
                elif verbo_cond != verbo:
                    continue  # No unifica

                # Verificar el objeto
                if objeto_cond.startswith("?"):  # Variable
                    if objeto_cond[1:] not in temp_bindings:
                        temp_bindings[objeto_cond[1:]] = objeto
                    elif temp_bindings[objeto_cond[1:]] != objeto:
                        continue  # No unifica
                elif objeto_cond != objeto:
                    continue  # No unifica

                # Si llega aquí, la tripleta hace match
                tripleta_match = True
                bindings = temp_bindings  # Actualizar bindings globales
                break

            if not tripleta_match:
                match = False
                break

        # Si las condiciones WHERE se cumplen, agregar el resultado
        if match:
            # Agregar solo las variables solicitadas en la consulta
            resultado = {var: bindings.get(var, "") for var in variables}
            resultados.append(resultado)

    # Aplicar límite si `LIMIT` está definido
    if limit:
        resultados = resultados[:limit]

    return resultados
