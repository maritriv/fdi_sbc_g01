# Sistema Basado en Reglas con Razonamiento Hacia Atrás y Lógica Difusa

![imagen](https://github.com/user-attachments/assets/c2fca9cd-598d-45ab-a1ac-1fb38ae7bfbb)

Este proyecto implementa un sistema basado en reglas (SBC) que utiliza razonamiento hacia atrás, permitiendo realizar consultas sobre hechos en una base de conocimiento con lógica difusa. El sistema puede cargar reglas y hechos desde un archivo de texto y responder a consultas desde la línea de comandos.

## Características

- **Base de conocimiento**: El sistema lee reglas y hechos desde un archivo. Las reglas pueden tener un grado de certeza, y los hechos pueden ser introducidos directamente en ejecución.
- **Razonamiento hacia atrás**: Implementa el algoritmo de encadenamiento hacia atrás para resolver consultas.
- **Lógica difusa**: El sistema maneja grados de certeza utilizando lógica difusa para los operadores `AND` y `OR`.
- **Interfaz interactiva**: Permite realizar consultas, agregar hechos, e imprimir la base de conocimiento desde la línea de comandos.

## Instalación

### 1. Requisitos previos

Este proyecto requiere **Python 3.6+**. Además, se utiliza la biblioteca `click` para la interfaz de línea de comandos. Instálala con:

```bash
pip install click
```

### Autores
Marina Triviño de las Heras y Pablo Alonso Romero

