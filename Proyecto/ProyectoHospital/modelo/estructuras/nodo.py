"""Nodo doblemente enlazado (dato + anterior + siguiente)."""

from __future__ import annotations

from typing import Any, Optional


class Nodo:
    """Nodo con enlaces hacia el elemento anterior y el siguiente.

    Attributes:
        dato: Elemento almacenado dentro del nodo.
        anterior: Nodo previo (``None`` si no existe).
        siguiente: Nodo siguiente (``None`` si no existe).
    """

    def __init__(
        self,
        dato: Any,
        anterior: Optional["Nodo"] = None,
        siguiente: Optional["Nodo"] = None,
    ) -> None:
        """Crea un nodo con su dato y sus enlaces."""
        self.dato = dato
        self.anterior = anterior
        self.siguiente = siguiente

    def __str__(self) -> str:
        """Retorna el dato del nodo convertido a texto."""
        return str(self.dato)
