import click # type: ignore
from pathlib import Path

class Regla:
    def __init__(self, cons, antecedentes, grado=1.0):
        self.cons = cons.strip()
        self.antecedentes = [antecedente.strip() for antecedente in antecedentes]
        self.grado = float(grado)

    def __repr__(self):
        antecedentes_str = ", ".join(self.antecedentes)
        return f"{self.cons} :- {antecedentes_str} [{self.grado}]"


class BaseConocimiento:
    def __init__(self):
        self.reglas = []
        self.hechos = {}

    def cargar_desde_archivo(self, filepath):
        fichero = Path(filepath)
        texto = fichero.read_text()
        for line in texto.split("\n"):
            line = line.strip()
            if line.startswith("#") or not line:
                continue
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
            else:
                if "[" in line:
                    hecho, grado = line.split("[")
                    grado = grado.rstrip("]")
                else:
                    hecho = line
                    grado = 1.0
                self.hechos[hecho.strip()] = float(grado)

    def imprimir(self):
        for regla in self.reglas:
            print(regla)
        for hecho, grado in self.hechos.items():
            print(f"{hecho} [{grado}]")

    def agregar_hecho(self, hecho, grado):
        """Agrega o actualiza un hecho en la base de conocimientos."""
        self.hechos[hecho] = grado
        print(f"Hecho '{hecho}' agregado/actualizado con grado {grado}")


import click # type: ignore
from pathlib import Path

class Regla:
    def __init__(self, cons, antecedentes, grado=1.0):
        self.cons = cons.strip()
        self.antecedentes = [antecedente.strip() for antecedente in antecedentes]
        self.grado = float(grado)

    def __repr__(self):
        antecedentes_str = ", ".join(self.antecedentes)
        return f"{self.cons} :- {antecedentes_str} [{self.grado}]"


class BaseConocimiento:
    def __init__(self):
        self.reglas = []
        self.hechos = {}

    def cargar_desde_archivo(self, filepath):
        fichero = Path(filepath)
        texto = fichero.read_text()
        for line in texto.split("\n"):
            line = line.strip()
            if line.startswith("#") or not line:
                continue
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
            else:
                if "[" in line:
                    hecho, grado = line.split("[")
                    grado = grado.rstrip("]")
                else:
                    hecho = line
                    grado = 1.0
                self.hechos[hecho.strip()] = float(grado)

    def imprimir(self):
        for regla in self.reglas:
            print(regla)
        for hecho, grado in self.hechos.items():
            print(f"{hecho} [{grado}]")

    def agregar_hecho(self, hecho, grado):
        """Agrega o actualiza un hecho en la base de conocimientos."""
        self.hechos[hecho] = grado
        print(f"Hecho '{hecho}' agregado/actualizado con grado {grado}")


class MotorInferencia:
    def __init__(self, base):
        self.base = base
        self.reglas_aplicadas = set()  # Para evitar ciclos de reglas

    def and_difuso(self, *grados):
        """ Operador AND difuso utilizando el mínimo """
        return min(grados)

    def or_difuso(self, grado1, grado2):
        """ Operador OR difuso usando inclusión-exclusión """
        return grado1 + grado2 - (grado1 * grado2)

    def backward_chain(self, consulta, nivel=0):
        # Imprimir el nivel de recursión y la consulta actual
        print(f"{'  ' * nivel}Evaluando: {consulta}")

        # Si la consulta está en los hechos conocidos
        if consulta in self.base.hechos:
            print(f"{'  ' * nivel}Hecho encontrado: {consulta} con grado {self.base.hechos[consulta]}")
            return self.base.hechos[consulta]

        # Verificar si ya hemos aplicado una regla para esta consulta (para evitar ciclos)
        if consulta in self.reglas_aplicadas:
            print(f"{'  ' * nivel}Ciclo detectado en: {consulta}. Omitiendo...")
            return None

        # Marcar esta consulta como aplicada temporalmente
        self.reglas_aplicadas.add(consulta)

        # Buscar todas las reglas que concluyan la consulta
        print(f"{'  ' * nivel}Buscando reglas para: {consulta}")
        grado_acumulado = None

        for regla in self.base.reglas:
            if regla.cons == consulta:
                print(f"{'  ' * nivel}Regla encontrada: {regla}")
                grados_antecedentes = []

                # Evaluar cada antecedente de la regla
                for antecedente in regla.antecedentes:
                    print(f"{'  ' * nivel}Evaluando antecedente: {antecedente}")
                    resultado = self.backward_chain(antecedente, nivel + 1)  # Aumentar el nivel de recursión
                    if resultado is None:
                        print(f"{'  ' * nivel}No se pudo resolver el antecedente: {antecedente}")
                        break
                    grados_antecedentes.append(resultado)
                else:
                    # Calcular el grado final de certeza usando el AND difuso
                    grado_regla = self.and_difuso(*grados_antecedentes) * regla.grado
                    print(f"{'  ' * nivel}Grado final para {consulta} con esta regla: {grado_regla} (AND difuso de {grados_antecedentes})")

                    # Acumular el grado utilizando el operador OR difuso
                    if grado_acumulado is None:
                        grado_acumulado = grado_regla
                    else:
                        grado_acumulado = self.or_difuso(grado_acumulado, grado_regla)

        # Si encontramos algún grado acumulado, lo devolvemos
        if grado_acumulado is not None:
            print(f"{'  ' * nivel}Grado acumulado para {consulta}: {grado_acumulado}")
            self.reglas_aplicadas.remove(consulta)  # Limpiamos después de encontrar una solución
            return grado_acumulado

        # Si no se encuentra ninguna regla o hecho que coincida
        print(f"{'  ' * nivel}No se encontró una regla o hecho para: {consulta}")
        self.reglas_aplicadas.remove(consulta)  # Limpiar para evitar ciclos en futuras evaluaciones
        return None




@click.command()
@click.argument('filepath')
def main(filepath):
    base = BaseConocimiento()
    base.cargar_desde_archivo(filepath)
    motor = MotorInferencia(base)

    while True:
        consulta = input("> ").strip()
        if consulta == "print":
            base.imprimir()
        elif consulta.endswith("?"):
            consulta = consulta.rstrip("?")
            resultado = motor.backward_chain(consulta)
            if resultado is None:
                print("No")
            else:
                print(f"Sí, con grado de certeza {resultado}")
        elif consulta.startswith("add "):
            # Parsear el hecho y el grado de certeza
            try:
                _, hecho, grado_str = consulta.split()
                grado = float(grado_str.strip('[]'))
                # Agregar el hecho a la base de conocimientos
                base.agregar_hecho(hecho, grado)
            except ValueError:
                print("Error en el formato. Uso: add <hecho> [grado]")
        else:
            print("Comando no reconocido")


if __name__ == "__main__":
    main()




@click.command()
@click.argument('filepath')
def main(filepath):
    base = BaseConocimiento()
    base.cargar_desde_archivo(filepath)
    motor = MotorInferencia(base)

    while True:
        consulta = input("> ").strip()
        if consulta == "print":
            base.imprimir()
        elif consulta.endswith("?"):
            consulta = consulta.rstrip("?")
            resultado = motor.backward_chain(consulta)
            if resultado is None:
                print("No")
            else:
                print(f"Sí, con grado de certeza {resultado}")
        elif consulta.startswith("add "):
            # Parsear el hecho y el grado de certeza
            try:
                _, hecho, grado_str = consulta.split()
                grado = float(grado_str.strip('[]'))
                # Agregar el hecho a la base de conocimientos
                base.agregar_hecho(hecho, grado)
            except ValueError:
                print("Error en el formato. Uso: add <hecho> [grado]")
        else:
            print("Comando no reconocido")


if __name__ == "__main__":
    main()
