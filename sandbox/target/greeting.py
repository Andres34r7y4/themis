"""Módulo de saludo mínimo gobernado por Themis.

Provee una función saludar(nombre) y un punto de entrada por línea de
comandos para imprimir un saludo parametrizado.
"""


def saludar(nombre: str = "mundo") -> str:
    """Devuelve un saludo para el nombre dado."""
    return f"Hola, {nombre}"


if __name__ == "__main__":
    import sys

    nombre = sys.argv[1] if len(sys.argv) > 1 else "mundo"
    print(saludar(nombre))
