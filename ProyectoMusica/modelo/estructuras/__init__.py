"""Estructuras de datos implementadas manualmente con nodos."""

from modelo.estructuras.cola import Cola, ColaVaciaError
from modelo.estructuras.nodo import Nodo
from modelo.estructuras.pila import Pila, PilaVaciaError

__all__ = [
    "Nodo",
    "Cola",
    "ColaVaciaError",
    "Pila",
    "PilaVaciaError",
]