"""Nodo base para las estructuras de datos lineales del simulador."""

from __future__ import annotations

from typing import Any, Optional


class Nodo:
    """Nodo de una estructura enlazada.

    Cada nodo almacena un dato y referencias a sus vecinos, lo que
    permite construir listas simples, dobles, circulares, pilas y
    colas sin depender de las colecciones nativas de Python.

    Attributes:
        dato: Valor almacenado en el nodo.
        siguiente: Referencia al siguiente nodo o ``None``.
        anterior: Referencia al nodo anterior o ``None``.
    """

    def __init__(
        self,
        dato: Any,
        siguiente: Optional["Nodo"] = None,
        anterior: Optional["Nodo"] = None,
    ) -> None:
        """Inicializa el nodo con sus tres referencias.

        Args:
            dato: Valor a almacenar en el nodo.
            siguiente: Nodo siguiente en la estructura.
            anterior: Nodo anterior en la estructura.
        """
        self.dato = dato
        self.siguiente = siguiente
        self.anterior = anterior

    def __repr__(self) -> str:
        """Representación técnica depurada del nodo."""
        return f"Nodo({self.dato!r})"

    def __str__(self) -> str:
        """Representación legible del nodo."""
        return str(self.dato)
