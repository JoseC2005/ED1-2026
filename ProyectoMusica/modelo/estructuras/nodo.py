"""Nodo base para las estructuras de datos del reproductor."""

from __future__ import annotations

from typing import Any, Optional


class Nodo:
    """Nodo de una estructura enlazada simple.

    Solo apunta hacia adelante, porque cola y pila no necesitan
    movernos hacia atrás (eso lo haría una lista doble).

    Attributes:
        dato: Valor almacenado en el nodo.
        siguiente: Referencia al siguiente nodo o ``None``.
    """

    def __init__(
        self,
        dato: Any,
        siguiente: Optional["Nodo"] = None,
    ) -> None:
        """Inicializa el nodo con su dato y su enlace.

        Args:
            dato: Valor a almacenar en el nodo.
            siguiente: Nodo siguiente en la estructura.
        """
        self.dato = dato
        self.siguiente = siguiente

    def __repr__(self) -> str:
        """Representación técnica depurada del nodo."""
        return f"Nodo({self.dato!r})"

    def __str__(self) -> str:
        """Representación legible del nodo."""
        return str(self.dato)