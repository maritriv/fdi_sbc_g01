# Sistema Basado en Conocimientos Interactivo

Este proyecto es un sistema basado en conocimientos (SBC) interactivo desarrollado en Python. Permite gestionar una base de conocimiento estructurada mediante tripletas `(Sujeto, Verbo, Objeto)` y realizar consultas SPARQL simplificadas sobre ella.

## Características

- **Carga y almacenamiento** de bases de conocimiento en formato de archivo (.txt), uno o varios archivos.
- **Añadir y eliminar** tripletas en la base de conocimiento.
- Soporte para **consultas SPARQL simplificadas** con cláusulas `SELECT`, `WHERE` y `LIMIT`.
- Función interactiva que permite gestionar la base de conocimiento y ejecutar consultas de manera dinámica.
- **Salida tabulada y legible** para los resultados de las consultas.
  
## Requisitos

- Python 3.8 o superior
- Librerías necesarias: `click`

Para instalar las dependencias, puedes usar:

```bash
pip install -r requirements.txt
