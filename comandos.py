# comandos.py

import click
from base_conocimiento import cargar_multiples_bases_conocimiento

# Comando load 
# Función para cargar una base de conocimiento en tiempo real
def load(base_conocimiento, comando):
    """
    Carga un nuevo archivo de base de conocimiento especificado en el comando 'load'.

    :param base_conocimiento: La base de conocimiento actual.
    :param comando: El comando 'load' con el nombre del archivo.
    :return: La base de conocimiento actualizada.
    """
    try:
        base_anadida = cargar_nueva_base(comando, base_conocimiento)
        return base_conocimiento + base_anadida
    except FileNotFoundError as e:
        click.echo(f"Error al cargar el archivo: {e}")
    except IndexError:
        click.echo("Por favor, especifique el archivo después de 'load'.")
    return base_conocimiento

def cargar_nueva_base(comando, base_conocimiento):
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

# Comando add
def add(base_conocimiento, comando):
    """
    Añade una afirmación (tripleta) a la base de conocimiento, verificando que
    tenga sujeto, verbo y objeto y asignando los prefijos correspondientes si es necesario.

    :param base_conocimiento: La base de conocimiento actual.
    :param comando: El comando 'add' con el sujeto, verbo y objeto.
    """
    # Extraer los tres elementos del comando (sujeto, verbo, objeto)
    partes = comando.split(" ", 3)
    if len(partes) < 4:
        click.echo("Error: El comando 'add' requiere tres parámetros (sujeto, verbo, objeto).")
        return

    sujeto, verbo, objeto = partes[1], partes[2], partes[3]

    # Función para verificar si una parte tiene un prefijo
    def tiene_prefijo(parte):
        return ':' in parte and parte.split(':')[0]  # Si tiene ':' es un prefijo

    # Verificar si el sujeto, verbo o objeto ya tienen prefijos
    if tiene_prefijo(sujeto):
        click.echo(f"Advertencia: El sujeto '{sujeto}' ya tiene un prefijo. Por favor, ingrese el sujeto sin prefijo.")
        return

    if tiene_prefijo(objeto):
        click.echo(f"Advertencia: El objeto '{objeto}' ya tiene un prefijo. Por favor, ingrese el objeto sin prefijo.")
        return

    if tiene_prefijo(verbo):
        click.echo(f"Advertencia: El verbo '{verbo}' ya tiene un prefijo. Por favor, ingrese el verbo sin prefijo.")
        return

    # Asignar el prefijo 'q1:' a sujeto y objeto (por defecto), y 't1:' al verbo
    sujeto_prefijado = f"q1:{sujeto}"
    objeto_prefijado = f"q1:{objeto}"

    # Si el verbo es especial, como P31 de Wikidata, asignar el prefijo 'wdt:'
    if verbo.lower() == "P31".lower():
        verbo_prefijado = f"wdt:{verbo}"
    else:
        verbo_prefijado = f"t1:{verbo}"

    # Crear la tripleta con los prefijos
    tripleta_con_prefijos = (sujeto_prefijado, verbo_prefijado, objeto_prefijado)

    # Añadir la tripleta a la base de conocimiento, evitando duplicados
    if tripleta_con_prefijos not in base_conocimiento:
        base_conocimiento.append(tripleta_con_prefijos)
        click.echo(f"Se ha añadido la afirmación: {tripleta_con_prefijos}")
    else:
        click.echo(f"La afirmación {tripleta_con_prefijos} ya existe en la base de conocimiento.")


# Comando delete
def delete(base_conocimiento, comando):
    """
    Elimina una afirmación de la base de conocimiento en tiempo real.

    :param base_conocimiento: La base de conocimiento actual.
    :param comando: El comando 'delete' con la afirmación en el formato:
                    'delete <sujeto> <verbo> <objeto>'
    :return: La base de conocimiento actualizada.
    """
    partes = comando.split()

    # Verificar que el comando tiene la estructura correcta
    if len(partes) != 4:
        click.echo("El comando debe tener el formato: 'delete <sujeto> <verbo> <objeto>'")
        return base_conocimiento

    # Extraer sujeto, verbo y objeto
    _, sujeto, verbo, objeto = partes

    # Añadir el prefijo 't1:' al verbo
    verbo = f"t1:{verbo}"

    # Crear la tripleta a eliminar
    tripleta = (sujeto, verbo, objeto)

    # Eliminar la tripleta si existe
    if tripleta in base_conocimiento:
        base_conocimiento.remove(tripleta)
        click.echo(f"Se ha eliminado la afirmación: {tripleta}")
    else:
        click.echo(f"La afirmación {tripleta} no se encuentra en la base de conocimiento.")

    return base_conocimiento


# Comando save
def guardar_base_conocimiento(base_conocimiento, archivo):
    """
    Guarda la base de conocimiento en el archivo especificado, agrupando tripletas
    por sujeto, separadas por ';' y terminando cada conjunto con un '.'.
    Después de cada ';' o '.', se agrega un salto de línea.
    """
    with open(archivo, 'w', encoding='utf-8') as f:
        sujetos = {}

        # Agrupar las tripletas por sujeto
        for sujeto, verbo, objeto in base_conocimiento:
            if sujeto not in sujetos:
                sujetos[sujeto] = []
            sujetos[sujeto].append((verbo, objeto))

        # Guardar las tripletas agrupadas por sujeto
        for sujeto, tripletas in sujetos.items():
            tripletas_str = ""
            for verbo, objeto in tripletas:
                # Agrega cada tripleta con un salto de línea después del ';'
                tripletas_str += f"{verbo} {objeto} ;\n"
            
            # Elimina el último salto de línea después del último ';' y agrega el '.'
            tripletas_str = tripletas_str.rstrip(" ;\n") + " .\n"
            
            # Escribir la tripleta del sujeto y las tripletas
            f.write(f"{sujeto} {tripletas_str}")

    click.echo(f"Base de conocimiento guardada en el archivo {archivo}.")

def save(base_conocimiento, comando):
    """
    Procesa el comando 'save' para guardar la base de conocimiento en un archivo.

    :param base_conocimiento: La base de conocimiento actual.
    :param comando: El comando 'save' con el nombre del archivo en el formato:
                    'save <nombre_archivo>'
    """
    partes = comando.split()

    # Verificar que el comando tiene la estructura correcta
    if len(partes) != 2:
        click.echo("El comando debe tener el formato: 'save <nombre_archivo>'")
        return base_conocimiento

    # Extraer el nombre del archivo
    _, archivo = partes

    # Llamar a la función para guardar la base de conocimiento
    guardar_base_conocimiento(base_conocimiento, archivo)

    return base_conocimiento