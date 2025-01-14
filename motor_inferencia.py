class MotorInferencia:
    """
    Motor de inferencia con razonamiento difuso y construcción de un árbol
    que muestra cómo se llegó a la respuesta.
    """

    def __init__(self, base):
        self.base = base
        self.reglas_aplicadas = set()

    def and_difuso(self, *grados):
        return min(grados)

    def or_difuso(self, grado1, grado2):
        return grado1 + grado2 - (grado1 * grado2)

    def backward_chain(self, consulta, nivel=0):
        # Evaluación de una consulta y construcción del árbol de razonamiento.
        if consulta in self.base.hechos:
            return self.base.hechos[consulta], {
                "consulta": consulta,
                "grado": self.base.hechos[consulta],
                "antecedentes": [],
            }

        if consulta in self.reglas_aplicadas:
            return None, {"consulta": consulta, "grado": None, "antecedentes": []}

        self.reglas_aplicadas.add(consulta)
        grado_acumulado = None
        arbol = {"consulta": consulta, "grado": None, "antecedentes": []}

        for regla in self.base.reglas:
            if regla.cons == consulta:
                grados_antecedentes = []
                sub_arboles = []

                for antecedente in regla.antecedentes:
                    resultado, sub_arbol = self.backward_chain(antecedente, nivel + 1)
                    sub_arboles.append(sub_arbol)

                    if resultado is None:
                        break
                    grados_antecedentes.append(resultado)

                if len(grados_antecedentes) == len(regla.antecedentes):
                    grado_regla = self.and_difuso(*grados_antecedentes) * regla.grado
                    arbol["antecedentes"].append(
                        {
                            "regla": str(regla),
                            "grado_regla": grado_regla,
                            "antecedentes": sub_arboles,
                        }
                    )

                    if grado_acumulado is None:
                        grado_acumulado = grado_regla
                    else:
                        grado_acumulado = self.or_difuso(grado_acumulado, grado_regla)

        arbol["grado"] = grado_acumulado
        self.reglas_aplicadas.remove(consulta)
        return grado_acumulado, arbol

    def mostrar_arbol(self, arbol, nivel=0):
        # Imprime el árbol de razonamiento en formato jerárquico.
        indent = "  " * nivel
        print(f"{indent}{arbol['consulta']} (grado: {arbol['grado']})")
        for antecedente in arbol.get("antecedentes", []):
            print(f"{indent}  Usando regla: {antecedente['regla']}")
            for sub_arbol in antecedente["antecedentes"]:
                self.mostrar_arbol(sub_arbol, nivel + 2)
