import click
from base_conocimiento import BaseConocimiento
from motor_inferencia import MotorInferencia


@click.command()
@click.argument("filepath")
def main(filepath):
    # Función principal para ejecutar el sistema experto.
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
                grado = float(grado_str.strip("[]"))
                base.agregar_hecho(hecho, grado)
            except ValueError:
                print("Error en el formato. Uso: add <hecho> [grado]")

        else:
            print("Comando no reconocido")


if __name__ == "__main__":
    main()
