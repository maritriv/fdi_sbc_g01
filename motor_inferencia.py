# motor_inferencia.py



class MotorInferencia:
    """
    Construcción de la clase MotorInferencia y sus atributos. También se definen
    las funciones and_difuso para el mínimo valor, or_difuso utilizando la fórmula de inclusión-exclusión
    y la función principal de backward_chain que realiza todo el algoritmo de encadenamiento hacia atrás.

    """
    def __init__(self, base):
        self.base = base  # Base de conocimientos
        self.reglas_aplicadas = set()  # Para evitar ciclos de reglas

    def and_difuso(self, *grados):
        # Operador AND difuso utilizando el mínimo valor.
        return min(grados)

    def or_difuso(self, grado1, grado2):
        # Operador OR difuso utilizando la fórmula de inclusión-exclusión.
        return grado1 + grado2 - (grado1 * grado2)

    def backward_chain(self, consulta, nivel=0):
        # Encadenamiento hacia atrás para deducir si una consulta es verdadera.
        print(f"{'  ' * nivel}Evaluando: {consulta}")

        # Si la consulta es un hecho conocido
        if consulta in self.base.hechos:
            print(
                f"{'  ' * nivel}Hecho encontrado: {consulta} con grado {self.base.hechos[consulta]}",
                "\n",
            )
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
                        print(
                            f"{'  ' * nivel}No se pudo resolver el antecedente: {antecedente}",
                            "\n",
                        )
                        break
                    grados_antecedentes.append(resultado)
                else:
                    # Calcular el grado de certeza de la regla usando AND difuso
                    grado_regla = self.and_difuso(*grados_antecedentes) * regla.grado
                    print(
                        f"{'  ' * nivel}Grado final para {consulta} con esta regla: {round(grado_regla, 2)}"
                    )

                    # Acumular el grado usando OR difuso
                    if grado_acumulado is None:
                        grado_acumulado = grado_regla
                    else:
                        grado_acumulado = self.or_difuso(grado_acumulado, grado_regla)

        # Retornar el grado acumulado si se encontró algún resultado
        if grado_acumulado is not None:
            print(
                f"{'  ' * nivel}Grado acumulado para {consulta}: {round(grado_acumulado, 2)}",
                "\n",
            )
            self.reglas_aplicadas.remove(consulta)
            return grado_acumulado

        # Si no se encuentra una regla o hecho para la consulta
        print(f"{'  ' * nivel}No se encontró una regla o hecho para: {consulta}")
        self.reglas_aplicadas.remove(consulta)
        return None
