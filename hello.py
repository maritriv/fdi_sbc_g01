from pathlib import Path


class Regla:
    def __init__(self, cons, resto):
        self.cons = cons
		self.resto = resto


def main():
	fichero = Path("base_laboral.txt")
	texto = fichero.read_text()
	for line in texto.split("\n"):
		if line.startswith("#") or not line:
			continue
		cons, resto = line.split(" :- ")
		cons = cons.strip()
		antecedentes = rest.split(",")
		print(line)
    print("Hello from sbc-g01-p2!")


if __name__ == "__main__":
    main()
    
