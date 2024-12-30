# base_conocimiento.py
from pathlib import Path
from reglas import Regla


class BaseConocimiento:
    """
    Construcción de la clase BaseConocimiento y sus atributos que son
    lista de reglas y diccionarios de grados de certezas. Incluye la función de la carga del archivo,
    la función de imprimir la base de conocimiento y la funciónn para agregar un hecho a la base.
    """

    def __init__(self):
        self.reglas = []  # Lista de reglas
        self.hechos = {}  # Diccionario de hechos con su grado de certeza

    def cargar_desde_archivo(self, filepath):
        # Carga reglas y hechos desde un archivo de texto.
        fichero = Path(filepath)
        texto = fichero.read_text()

        for line in texto.split("\n"):
            line = line.strip()
            # Ignorar comentarios y líneas vacías
            if line.startswith("#") or not line:
                continue
            # Cargar una regla
            if ":-" in line:
                cons, resto = line.split(" :- ")
                if "[" in resto:
                    antecedentes, grado = resto.split("[")
                    grado = grado.rstrip("]")
                else:
                    antecedentes = resto
                    grado = 1.0
                antecedentes = antecedentes.split(",")
                regla = Regla(cons, antecedentes, grado)
                self.reglas.append(regla)
            # Cargar un hecho
            else:
                if "[" in line:
                    hecho, grado = line.split("[")
                    grado = grado.rstrip("]")
                else:
                    hecho = line
                    grado = 1.0
                self.hechos[hecho.strip()] = float(grado)

    def imprimir(self):
        # Imprime todas las reglas y hechos en la base de conocimientos.
        print("\n", "Reglas:")
        for regla in self.reglas:
            print(regla)
        print("\n")

        print("Hechos:")
        for hecho, grado in self.hechos.items():
            print(f"{hecho} [{grado}]")
        print("\n")

    def agregar_hecho(self, hecho, grado):
        # Agrega o actualiza un hecho en la base de conocimientos.
        self.hechos[hecho] = grado
        print(f"Hecho '{hecho}' agregado con grado {grado}", "\n")
