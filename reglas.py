# reglas.py


# Construcción de la clase regla
class Regla:
    """ 
    Construcción de la clase Regla donde se definen sus atributos;
    conclusión de la regla, lista de antecedentes y grado de certeza 
    """
    def __init__(self, cons, antecedentes, grado=1.0):
        self.cons = cons.strip()  # La conclusión de la regla, eliminando espacios
        self.antecedentes = [
            antecedente.strip() for antecedente in antecedentes
        ]  # Lista de antecedentes
        self.grado = float(grado)  # El grado de certeza de la regla

    def __repr__(self):
        # Formato para representar una regla como "conclusión :- antecedentes [grado]"
        antecedentes_str = ", ".join(self.antecedentes)
        return f"{self.cons} :- {antecedentes_str} [{self.grado}]"
