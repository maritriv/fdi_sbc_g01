import click
from utils import iniciar_bucle_interactivo
from base_conocimiento import cargar_bases_conocimiento


@click.command()
@click.argument("archivos_base_conocimiento", nargs=-1)  # Acepta uno o más archivos
def main(archivos_base_conocimiento):
    """
    Programa principal para cargar bases de conocimiento y ejecutar consultas.

    ARCHIVOS_BASE_CONOCIMIENTO: Uno o más archivos de base de conocimiento.
    """
    base_conocimiento = cargar_bases_conocimiento(archivos_base_conocimiento)

    if base_conocimiento:
        iniciar_bucle_interactivo(base_conocimiento)


if __name__ == "__main__":
    main()
