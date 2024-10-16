import click
from pathlib import Path

""" 
Construcción de la clase Regla donde se definen sus atributos;
conclusión de la regla, lista de antecedentes y grado de certeza 
"""
#Construcción de la clase regla
class Regla:
    def __init__(self, cons, antecedentes, grado=1.0):
        self.cons = cons.strip()  # La conclusión de la regla, eliminando espacios
        self.antecedentes = [antecedente.strip() for antecedente in antecedentes]  # Lista de antecedentes
        self.grado = float(grado)  # El grado de certeza de la regla

    def __repr__(self):
        # Formato para representar una regla como "conclusión :- antecedentes [grado]"
        antecedentes_str = ", ".join(self.antecedentes)
        return f"{self.cons} :- {antecedentes_str} [{self.grado}]"

"""
Construcción de la clase BaseConocimiento y sus atributos que son 
lista de reglas y diccionarios de grados de certezas. Incluye la función de la carga del archivo,
la función de imprimir la base de conocimiento y la funciónn para agregar un hecho a la base.

""" 
class BaseConocimiento:
    def __init__(self):
        self.reglas = []  # Lista de reglas
        self.hechos = {}  # Diccionario de hechos con su grado de certeza

    def cargar_desde_archivo(self, filepath):
        #Carga reglas y hechos desde un archivo de texto.
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
        #Imprime todas las reglas y hechos en la base de conocimientos.
        print("\n", "Reglas:")
        for regla in self.reglas:
            print(regla)
        print("\n")

        print("Hechos:")
        for hecho, grado in self.hechos.items():
            print(f"{hecho} [{grado}]")
        print("\n")

    def agregar_hecho(self, hecho, grado):
        #Agrega o actualiza un hecho en la base de conocimientos.
        self.hechos[hecho] = grado
        print(f"Hecho '{hecho}' agregado con grado {grado}", "\n")

"""
Construcción de la clase MotorInferencia y sus atributos. También se definen
las funciones and_difuso para el mínimo valor, or_difuso utilizando la fórmula de inclusión-exclusión
y la función principal de backward_chain que realiza todo el algoritmo de encadenamiento hacia atrás.

"""

class MotorInferencia:
    def __init__(self, base):
        self.base = base  # Base de conocimientos
        self.reglas_aplicadas = set()  # Para evitar ciclos de reglas

    def and_difuso(self, *grados):
        #Operador AND difuso utilizando el mínimo valor.
        return min(grados)

    def or_difuso(self, grado1, grado2):
        #Operador OR difuso utilizando la fórmula de inclusión-exclusión.
        return grado1 + grado2 - (grado1 * grado2)

    def backward_chain(self, consulta, nivel=0):
        #Encadenamiento hacia atrás para deducir si una consulta es verdadera.
        print(f"{'  ' * nivel}Evaluando: {consulta}")

        # Si la consulta es un hecho conocido
        if consulta in self.base.hechos:
            print(f"{'  ' * nivel}Hecho encontrado: {consulta} con grado {self.base.hechos[consulta]}" ,"\n")
            return self.base.hechos[consulta]

        # Verificar si ya hemos aplicado una regla para esta consulta
        if consulta in self.reglas_aplicadas:
            print(f"{'  ' * nivel}Ciclo detectado en: {consulta}. Omitiendo...")
            return None

        # Marcar la consulta como aplicada
        self.reglas_aplicadas.add(consulta)
        grado_acumulado = None  # Para acumular el grado de certeza

        # Buscar reglas que concluyan en la consulta
        for regla in self.base.reglas:
            if regla.cons == consulta:
                print(f"{'  ' * nivel}Regla encontrada: {regla}", "\n")
                grados_antecedentes = []

                # Evaluar los antecedentes de la regla
                for antecedente in regla.antecedentes:
                    print(f"{'  ' * nivel}Evaluando antecedente: {antecedente}")
                    resultado = self.backward_chain(antecedente, nivel + 1)
                    if resultado is None:
                        print(f"{'  ' * nivel}No se pudo resolver el antecedente: {antecedente}", "\n")
                        break
                    grados_antecedentes.append(resultado)
                else:
                    # Calcular el grado de certeza de la regla usando AND difuso
                    grado_regla = self.and_difuso(*grados_antecedentes) * regla.grado
                    print(f"{'  ' * nivel}Grado final para {consulta} con esta regla: {round(grado_regla, 2)}")

                    # Acumular el grado usando OR difuso
                    if grado_acumulado is None:
                        grado_acumulado = grado_regla
                    else:
                        grado_acumulado = self.or_difuso(grado_acumulado, grado_regla)

        # Retornar el grado acumulado si se encontró algún resultado
        if grado_acumulado is not None:
            print(f"{'  ' * nivel}Grado acumulado para {consulta}: {round(grado_acumulado, 2)}", "\n")
            self.reglas_aplicadas.remove(consulta)
            return grado_acumulado

        # Si no se encuentra una regla o hecho para la consulta
        print(f"{'  ' * nivel}No se encontró una regla o hecho para: {consulta}")
        self.reglas_aplicadas.remove(consulta)
        return None


@click.command()
@click.argument('filepath')
def main(filepath):
    #Función principal para ejecutar el sistema experto.
    base = BaseConocimiento()
    base.cargar_desde_archivo(filepath)  # Cargar reglas y hechos desde el archivo
    motor = MotorInferencia(base)

    # Bucle para interactuar con el sistema
    while True:
        consulta = input("> ").strip()

        if consulta == "print":  # Comando para imprimir la base de conocimientos
            base.imprimir()

        elif consulta.endswith("?"):  # Comando para hacer una consulta
            consulta = consulta.rstrip("?")
            print("\n")
            resultado = motor.backward_chain(consulta)
            if resultado is None:
                print("\n")
            else:
                print(f"Sí, con grado de certeza {round(resultado, 2)}")

        elif consulta.startswith("add "):  # Comando para agregar hechos
            try:
                _, hecho, grado_str = consulta.split()
                grado = float(grado_str.strip('[]'))
                base.agregar_hecho(hecho, grado)
            except ValueError:
                print("Error en el formato. Uso: add <hecho> [grado]")

        else:
            print("Comando no reconocido")


if __name__ == "__main__":
    main()
