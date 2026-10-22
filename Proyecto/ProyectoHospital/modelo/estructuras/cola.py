"""Cola (Queue) — política FIFO con nodos manuales.

En el hospital se usa para la **consulta externa**: los pacientes se
atienden en el orden en que llegan (primero en llegar, primero en ser
atendido).
"""

from __future__ import annotations

from typing import Any, Optional

from modelo.estructuras.nodo import Nodo


class ColaVaciaError(Exception):
    """Se lanza al intentar operar sobre una cola vacía."""


class Cola:
    """Cola dinámica FIFO implementada con nodos enlazados.

    Mantiene punteros a ``primero`` y ``último`` para que ``encolar``
    y ``desencolar`` sean operaciones **O(1)**.

    Ejemplo:
        >>> cola = Cola()
        >>> cola.encolar("paciente-A")
        >>> cola.encolar("paciente-B")
        >>> cola.desencolar()
        'paciente-A'
    """

    def __init__(self) -> None:
        """Crea una cola vacía."""
        self._nodo_primero: Optional[Nodo] = None
        self._nodo_ultimo: Optional[Nodo] = None
        self._cantidad_de_elementos: int = 0

    def encolar(self, dato: Any) -> None:
        """Agrega un elemento al final de la cola. Complejidad: **O(1)**.

        Args:
            dato: Elemento a encolar.
        """
        nuevo_nodo = Nodo(dato)
        if self._nodo_ultimo is None:
            self._nodo_primero = nuevo_nodo
            self._nodo_ultimo = nuevo_nodo
        else:
            self._nodo_ultimo.siguiente = nuevo_nodo
            self._nodo_ultimo = nuevo_nodo
        self._cantidad_de_elementos += 1

    def desencolar(self) -> Any:
        """Elimina y retorna el primer elemento. Complejidad: **O(1)**.

        Returns:
            El dato que estaba al frente de la cola.

        Raises:
            ColaVaciaError: Si la cola no contiene elementos.
        """
        if self.esta_vacia():
            raise ColaVaciaError("No se puede desencolar: la cola está vacía")
        dato = self._nodo_primero.dato
        self._nodo_primero = self._nodo_primero.siguiente
        if self._nodo_primero is None:
            self._nodo_ultimo = None
        self._cantidad_de_elementos -= 1
        return dato

    def ver_primero(self) -> Any:
        """Retorna el primer elemento sin eliminarlo.

        Returns:
            El dato al frente de la cola.

        Raises:
            ColaVaciaError: Si la cola no contiene elementos.
        """
        if self.esta_vacia():
            raise ColaVaciaError("La cola está vacía")
        return self._nodo_primero.dato

    def esta_vacia(self) -> bool:
        """Indica si la cola no contiene elementos."""
        return self._nodo_primero is None

    def __len__(self) -> int:
        """Retorna la cantidad de elementos de la cola."""
        return self._cantidad_de_elementos

    def a_lista(self) -> list:
        """Convierte la cola a una lista Python (solo para presentación).

        Returns:
            Los elementos de primero a último.
        """
        elementos = []
        actual = self._nodo_primero
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __str__(self) -> str:
        """Retorna la cola representada de primero a último."""
        elementos = [str(dato) for dato in self.a_lista()]
        if not elementos:
            return "Cola(vacía)"
        return "Cola(primero→ [" + ", ".join(elementos) + "] ←último)"
