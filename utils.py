# utils.py

import click

def imprimir_tabla(resultados, variables):
    """
    Imprime los resultados en formato de tabla alineada.
    """
    if resultados:
        column_widths = {var: max(len(var), 14) for var in variables}

        encabezado = " | ".join(f"?{var:{column_widths[var]}}" for var in variables)
        separador = "-+-".join("-" * column_widths[var] for var in variables)

        click.echo(encabezado)
        click.echo(separador)

        for resultado in resultados:
            fila = " | ".join(f"{resultado.get(var, ''):{column_widths[var]}}" for var in variables)
            click.echo(fila)
    else:
        click.echo("No se encontraron resultados para la consulta.")
