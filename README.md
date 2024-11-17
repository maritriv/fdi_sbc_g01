# Sistema Basado en Conocimientos Interactivo

![Logo de SPARQL](https://clhwogtywa.cloudimg.io/www.census.de/wp-content/uploads/sparql-logo-scaled.jpg)


Este proyecto es un sistema basado en conocimientos (SBC) interactivo desarrollado en Python. Permite gestionar una base de conocimiento estructurada mediante tripletas `(Sujeto, Verbo, Objeto)` y realizar consultas SPARQL simplificadas sobre ella.

## Características

- **Carga, almacenamiento y guardado** de bases de conocimiento en formato de archivo (.txt), uno o varios archivos.
- **Añadir y eliminar** tripletas en la base de conocimiento.
- Soporte para **consultas SPARQL simplificadas** con cláusulas `SELECT`, `WHERE` y `LIMIT`.
- Función interactiva que permite gestionar la base de conocimiento y ejecutar consultas de manera dinámica.
- **Salida tabulada y legible** para los resultados de las consultas.
  
## Requisitos

- Python 3.8 o superior
- Librerías necesarias: `click`

## Estructura

├── comandos.py                          # Funciones para manipular la base de conocimiento (add, delete, load, save) y el help (guía de comandos posibles)

├── consulta.py                          # Lógica para procesar y ejecutar consultas SPARQL simplificadas

├── base_conocimiento.py                 # Funciones para cargar una o varias bases de conocimiento

├── utils.py                             # Funciones de utilidad, como impresión y gestión interactiva

├── main.py                              # Archivo principal que ejecuta el sistema

├── base_conocimiento_real_madrid.txt    # Base de conocimiento del equipo Real Madrid

├── base_conocimiento_fc_barcelona.txt   # Base de conocimiento del equipo FC Barcelona

└── README.md                            # Este archivo

## Ejecutar el sistema

Para iniciar el sistema interactivo, ejecuta el archivo principal como este ejemplo:

- uv run main.py base_conocimiento_real_madrid.txt

## Comandos disponibles

En el modo interactivo, puedes usar los siguientes comandos:

SELECT: Ejecuta consultas SPARQL simplificadas sobre la base de conocimiento.
        
        Ejemplo:

    SELECT ?jugador WHERE { ?jugador t1:posicion q1:portero . } LIMIT 5

LOAD: Carga una base de conocimiento desde un archivo.

    Ejemplo:

    load base_conocimiento_real_madrid.txt

ADD: Añade una nueva tripleta (Sujeto, Verbo, Objeto) a la base de conocimiento.

    Ejemplo:

    add courtois P31 portero

DELETE: Elimina una tripleta existente.

    Ejemplo:

    delete courtois P31 portero

SAVE: Guarda la base de conocimiento actual en un archivo.

    Ejemplo:

    save base_conocimiento_real_madrid.txt

PRINT_ALL: Imprime todas las tripletas en la base de conocimiento.

    Ejemplo:

    print_all o imprimir_todo

EXIT: Finaliza el programa.

    Ejemplo:

    exit

HELP: Ayuda comandos del programa

    Ejemplo:

    help

DRAW: Dibuja la última consulta con sus relaciones

    Ejemplo:

    draw

## Ejemplo de Uso

Base de conocimiento inicial:

    "Sujeto"              "Verbo"         "Objeto"
    ---------------------------------------------------
    "q1:courtois"        "wdt:P31"        "q1:jugador"

    "q1:courtois"        "t1:posicion"    "q1:portero"


Consulta SPARQL:

    SELECT ?jugador WHERE { ?jugador wdt:P31 q1:portero }


Resultado:

    ?jugador
    --------------
    q1:courtois


## Autores

Hecho por Pablo Alonso Romero y Marina Triviño de las Heras
