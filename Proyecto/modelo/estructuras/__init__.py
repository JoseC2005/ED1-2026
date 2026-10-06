"""Estructuras de datos implementadas manualmente con nodos.

Todas las estructuras evitan depender de las colecciones nativas de
Python (list, dict, deque) como contenedor principal de sus elementos.
"""

from modelo.estructuras.nodo import Nodo
from modelo.estructuras.pila import Pila, PilaVaciaError
from modelo.estructuras.cola import Cola, ColaVaciaError
from modelo.estructuras.lista_doble import ListaDoblementeEnlazada

__all__ = [
    "Nodo",
    "Pila",
    "PilaVaciaError",
    "Cola",
    "ColaVaciaError",
    "ListaDoblementeEnlazada",
]
