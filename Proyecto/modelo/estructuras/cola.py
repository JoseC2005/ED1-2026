"""Cola (Queue) — política FIFO con nodos manuales.

Aplicación principal en el simulador: cola de despacho de paquetes,
donde el envío que llegó primero se despacha primero.

Referencia: unidad3/ejemplos/03_cola_circular.py (INF-220)
reimplementada como cola dinámica enlazada sin colecciones nativas.
"""

from __future__ import annotations

from typing import Any, Optional

from modelo.estructuras.nodo import Nodo


class ColaVaciaError(Exception):
    """Se lanza al intentar operar sobre una cola vacía."""


class Cola:
    """Cola dinámica FIFO implementada con una lista enlazada manual.

    Mantiene punteros a ``frente`` y ``fondo`` para que ``encolar``
    y ``desencolar`` sean operaciones **O(1)**.

    Ejemplo:
        >>> cola = Cola()
        >>> cola.encolar("paquete-A")
        >>> cola.encolar("paquete-B")
        >>> cola.desencolar()
        'paquete-A'
    """

    def __init__(self) -> None:
        """Crea una cola vacía."""
        self._frente: Optional[Nodo] = None
        self._fondo: Optional[Nodo] = None
        self._tamanio: int = 0

    def encolar(self, dato: Any) -> None:
        """Agrega un elemento al fondo de la cola.

        Complejidad temporal: **O(1)**.

        Args:
            dato: Elemento a encolar.
        """
        nuevo_nodo = Nodo(dato)
        if self._fondo is None:
            self._frente = nuevo_nodo
            self._fondo = nuevo_nodo
        else:
            self._fondo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self._fondo
            self._fondo = nuevo_nodo
        self._tamanio += 1

    def desencolar(self) -> Any:
        """Elimina y retorna el elemento del frente.

        Complejidad temporal: **O(1)**.

        Returns:
            El dato que estaba al frente de la cola.

        Raises:
            ColaVaciaError: Si la cola no contiene elementos.
        """
        if self.esta_vacia():
            raise ColaVaciaError("No se puede desencolar: la cola está vacía")
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._fondo = None
        else:
            self._frente.anterior = None
        self._tamanio -= 1
        return dato

    def ver_frente(self) -> Any:
        """Retorna el elemento del frente sin eliminarlo.

        Complejidad temporal: **O(1)**.

        Returns:
            El dato al frente de la cola.

        Raises:
            ColaVaciaError: Si la cola no contiene elementos.
        """
        if self.esta_vacia():
            raise ColaVaciaError("La cola está vacía")
        return self._frente.dato

    def esta_vacia(self) -> bool:
        """Indica si la cola no contiene elementos.

        Returns:
            ``True`` si la cola está vacía.
        """
        return self._frente is None

    def __len__(self) -> int:
        """Retorna la cantidad de elementos de la cola."""
        return self._tamanio

    def a_lista(self) -> list:
        """Convierte la cola a una lista Python (solo para presentación).

        Complejidad temporal: **O(n)**.

        Returns:
            Los elementos de frente a fondo.
        """
        elementos = []
        actual = self._frente
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __str__(self) -> str:
        """Retorna la cola representada de frente a fondo."""
        elementos = [str(dato) for dato in self.a_lista()]
        if not elementos:
            return "Cola(vacía)"
        return "Cola(frente→ [" + ", ".join(elementos) + "] ←fondo)"
