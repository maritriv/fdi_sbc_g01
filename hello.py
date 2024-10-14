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


class MotorInferencia:
    def __init__(self, base):
        self.base = base

    def and_difuso(self, *grados):
        """ Operador AND difuso utilizando mínimo """
        return min(grados)

    def or_difuso(self, grado1, grado2):
        """ Operador OR difuso usando inclusión-exclusión """
        return grado1 + grado2 - (grado1 * grado2)

    def backward_chain(self, consulta):
        if consulta in self.base.hechos:
            return self.base.hechos[consulta]

        for regla in self.base.reglas:
            if regla.cons == consulta:
                grados_antecedentes = []
                for antecedente in regla.antecedentes:
                    resultado = self.backward_chain(antecedente)
                    if resultado is None:
                        return None
                    grados_antecedentes.append(resultado)

                grado_final = self.and_difuso(*grados_antecedentes) * regla.grado
                return grado_final
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
            _, hecho, grado = consulta.split()
            base.hechos[hecho] = float(grado)
        else:
            print("Comando no reconocido")


if __name__ == "__main__":
    main()
