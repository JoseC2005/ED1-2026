"""Pila (Stack) — política LIFO con nodos manuales.

En el hospital se usa para el **historial de atenciones**: el último
paciente atendido queda arriba, lo que permite "deshacer" la última
atención.
"""

from __future__ import annotations

from typing import Any, Optional

from modelo.estructuras.nodo import Nodo


class PilaVaciaError(Exception):
    """Se lanza al intentar operar sobre una pila vacía."""


class Pila:
    """Pila dinámica LIFO implementada con nodos enlazados.

    El elemento superior corresponde a la cabeza de la lista, por lo
    que ``apilar`` y ``desapilar`` son operaciones **O(1)**.

    Ejemplo:
        >>> pila = Pila()
        >>> pila.apilar(10)
        >>> pila.apilar(20)
        >>> pila.desapilar()
        20
    """

    def __init__(self) -> None:
        """Crea una pila vacía."""
        self._nodo_superior: Optional[Nodo] = None
        self._cantidad_de_elementos: int = 0

    def apilar(self, dato: Any) -> None:
        """Inserta un elemento en la cima de la pila. Complejidad: **O(1)**.

        Args:
            dato: Elemento a apilar.
        """
        self._nodo_superior = Nodo(dato, siguiente=self._nodo_superior)
        self._cantidad_de_elementos += 1

    def desapilar(self) -> Any:
        """Elimina y retorna el elemento de la cima. Complejidad: **O(1)**.

        Returns:
            El dato que estaba en la cima de la pila.

        Raises:
            PilaVaciaError: Si la pila no contiene elementos.
        """
        if self.esta_vacia():
            raise PilaVaciaError("No se puede desapilar: la pila está vacía")
        dato = self._nodo_superior.dato
        self._nodo_superior = self._nodo_superior.siguiente
        self._cantidad_de_elementos -= 1
        return dato

    def ver_superior(self) -> Any:
        """Retorna la cima sin eliminarla.

        Returns:
            El dato en la cima de la pila.

        Raises:
            PilaVaciaError: Si la pila no contiene elementos.
        """
        if self.esta_vacia():
            raise PilaVaciaError("La pila está vacía")
        return self._nodo_superior.dato

    def esta_vacia(self) -> bool:
        """Indica si la pila no contiene elementos."""
        return self._nodo_superior is None

    def __len__(self) -> int:
        """Retorna la cantidad de elementos de la pila."""
        return self._cantidad_de_elementos

    def a_lista(self) -> list:
        """Convierte la pila a una lista Python (solo para presentación).

        Returns:
            Los elementos de cima a base (lo más reciente primero).
        """
        elementos = []
        actual = self._nodo_superior
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __str__(self) -> str:
        """Retorna la pila representada de cima a base."""
        elementos = [str(dato) for dato in self.a_lista()]
        if not elementos:
            return "Pila(vacía)"
        return "Pila(cima→ [" + " | ".join(elementos) + "] ←base)"
