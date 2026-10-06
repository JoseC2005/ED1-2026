"""Pila (Stack) — política LIFO con nodos manuales.

Aplicación principal en el simulador: deshacer/rehacer de acciones
(Undo/Redo) mediante doble pila.

Referencia: unidad3/ejemplos/02_pila_estatica_dinamica.py (INF-220)
reimplementada sin colecciones nativas y con PEP 8.
"""

from __future__ import annotations

from typing import Any, Optional

from modelo.estructuras.nodo import Nodo


class PilaVaciaError(Exception):
    """Se lanza al intentar operar sobre una pila vacía."""


class Pila:
    """Pila dinámica implementada con una lista enlazada manual.

    El tope de la pila corresponde a la cabeza de la lista, por lo que
    ``apilar`` y ``desapilar`` son operaciones **O(1)**.

    Ejemplo:
        >>> pila = Pila()
        >>> pila.apilar(10)
        >>> pila.apilar(20)
        >>> pila.desapilar()
        20
    """

    def __init__(self) -> None:
        """Crea una pila vacía."""
        self._tope: Optional[Nodo] = None
        self._tamanio: int = 0

    def apilar(self, dato: Any) -> None:
        """Inserta un elemento en el tope de la pila.

        Complejidad temporal: **O(1)**.

        Args:
            dato: Elemento a apilar.
        """
        nuevo_nodo = Nodo(dato, siguiente=self._tope)
        self._tope = nuevo_nodo
        self._tamanio += 1

    def desapilar(self) -> Any:
        """Elimina y retorna el elemento del tope.

        Complejidad temporal: **O(1)**.

        Returns:
            El dato que estaba en el tope de la pila.

        Raises:
            PilaVaciaError: Si la pila no contiene elementos.
        """
        if self.esta_vacia():
            raise PilaVaciaError("No se puede desapilar: la pila está vacía")
        dato = self._tope.dato
        self._tope = self._tope.siguiente
        self._tamanio -= 1
        return dato

    def ver_tope(self) -> Any:
        """Retorna el tope sin eliminarlo.

        Complejidad temporal: **O(1)**.

        Returns:
            El dato en el tope de la pila.

        Raises:
            PilaVaciaError: Si la pila no contiene elementos.
        """
        if self.esta_vacia():
            raise PilaVaciaError("La pila está vacía")
        return self._tope.dato

    def esta_vacia(self) -> bool:
        """Indica si la pila no contiene elementos.

        Returns:
            ``True`` si la pila está vacía.
        """
        return self._tope is None

    def __len__(self) -> int:
        """Retorna la cantidad de elementos de la pila."""
        return self._tamanio

    def __str__(self) -> str:
        """Retorna la pila representada de tope a base."""
        elementos = []
        actual = self._tope
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        if not elementos:
            return "Pila(vacía)"
        return "Pila(tope→ [" + " | ".join(elementos) + "] ←base)"
