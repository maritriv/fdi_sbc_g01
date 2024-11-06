import re

def tripleta_con_sujeto():

def tripleta_sin_sujeto():


def crear_tripleta(linea):
    if linea.startswith('#') or not linea.strip():
        continue  # Ignorar comentarios y líneas vacías
        
    tripleta = linea.split()
    
    if tripleta[-1] == ";":
        tripleta_con_sujeto(
    
    

def cargar_base_conocimiento(archivo):
    base_conocimiento = []
    sujeto_anterior = ""
    with open(archivo, 'r') as f:
        for linea in f:
            
           
   
                tripleta = linea.split()
                
                s, v, o, p = linea.split()
                s = s.split(":")
                s = s[1]
                v = v.split(":")
                v = v[1]
                o = o.split(":")
                o = o[1].strip('"')
                o = o[1]
                tripleta = (s,v,o)
                sujeto_anterior = s
                if p == ";"
                
                #tripleta = re.split(r'\s*;\s*', linea.strip().rstrip('.'))
  

                if (s, v, o) not in base_conocimiento:
                    base_conocimiento.append((s, v, o))
    return base_conocimiento


def ejecutar_consulta(base_conocimiento, consulta):
    # Parsear consulta (simplificada)
    variables = re.findall(r'\?(\w+)', consulta)
    where_clause = re.search(r'where \{(.*)\}', consulta, re.DOTALL).group(1).strip()

    resultados = []
    for sujeto, relaciones in base_conocimiento.items():
        # Buscar coincidencias con las tripletas en la cláusula WHERE
        match = True
        bindings = {}
        for tripleta in where_clause.split('.'):
            tripleta = tripleta.strip()
            if not tripleta:
                continue
            predicado, objeto = re.split(r'\s+', tripleta, 1)
            if objeto.startswith('?'):  # Variable
                variable = objeto[1:]
                if variable in variables:
                    bindings[variable] = sujeto
            else:
                # Comparar con el valor literal
                if objeto not in relaciones.get(predicado, []):
                    match = False
                    break
        if match:
            resultados.append(bindings)
    return resultados


import click

@click.command()
@click.argument('base_conocimiento')
def main(base_conocimiento):
    base_conocimiento = cargar_base_conocimiento(base_conocimiento)
    click.echo(f"Base de conocimiento cargada: {base_conocimiento}")
"""
    while True:
        comando = input("SBC_P3> ").strip()
        if comando.startswith("select"):
            resultados = ejecutar_consulta(base_conocimiento, comando)
            for resultado in resultados:
                click.echo("\t".join(str(resultado.get(var, "")) for var in ["var1", "var2"]))
        elif comando.startswith("exit"):
            break
        else:
            click.echo("Comando no reconocido")
"""
if __name__ == '__main__':
    main()

