"""Lista doblemente enlazada con acceso bidireccional.

Aplicación principal en el simulador: historial de movimientos y
recorridos hacia adelante/atras de la operación logística.

Referencia: codigo_base_referencial.py (DoublyLinkedList) adaptado a
español, PEP 8 y nodos compartidos.
"""

from __future__ import annotations

from typing import Any, Optional

from modelo.estructuras.nodo import Nodo


class ElementoNoEncontradoError(Exception):
    """Se lanza cuando el dato a eliminar no existe en la lista."""


class ListaDoblementeEnlazada:
    """Lista doblemente enlazada con punteros a cabeza y cola.

    Al mantener referencias a ``_cabeza`` y ``_cola``, las operaciones
    en los extremos (insertar al final, eliminar el último) son
    **O(1)**; buscar o eliminar un elemento intermedio es **O(n)**.

    Ejemplo:
        >>> lista = ListaDoblementeEnlazada()
        >>> lista.insertar_final("A")
        >>> lista.insertar_final("B")
        >>> len(lista)
        2
    """

    def __init__(self) -> None:
        """Crea una lista vacía."""
        self._cabeza: Optional[Nodo] = None
        self._cola: Optional[Nodo] = None
        self._tamanio: int = 0

    @property
    def cabeza(self) -> Optional[Nodo]:
        """Retorna el primer nodo de la lista."""
        return self._cabeza

    @property
    def cola(self) -> Optional[Nodo]:
        """Retorna el último nodo de la lista."""
        return self._cola

    def insertar_inicio(self, dato: Any) -> None:
        """Inserta un elemento al inicio de la lista.

        Complejidad temporal: **O(1)**.

        Args:
            dato: Elemento a insertar.
        """
        nuevo_nodo = Nodo(dato, siguiente=self._cabeza)
        if self._cabeza is None:
            self._cola = nuevo_nodo
        else:
            self._cabeza.anterior = nuevo_nodo
        self._cabeza = nuevo_nodo
        self._tamanio += 1

    def insertar_final(self, dato: Any) -> None:
        """Inserta un elemento al final de la lista.

        Complejidad temporal: **O(1)**.

        Args:
            dato: Elemento a insertar.
        """
        nuevo_nodo = Nodo(dato, anterior=self._cola)
        if self._cola is None:
            self._cabeza = nuevo_nodo
        else:
            self._cola.siguiente = nuevo_nodo
        self._cola = nuevo_nodo
        self._tamanio += 1

    def eliminar(self, dato: Any) -> bool:
        """Elimina la primera aparición de un elemento.

        Complejidad temporal: **O(n)**.

        Args:
            dato: Elemento a eliminar.

        Returns:
            ``True`` si el elemento existía y fue eliminado.
        """
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                if actual.anterior is None:
                    self._cabeza = actual.siguiente
                else:
                    actual.anterior.siguiente = actual.siguiente

                if actual.siguiente is None:
                    self._cola = actual.anterior
                else:
                    actual.siguiente.anterior = actual.anterior

                self._tamanio -= 1
                return True
            actual = actual.siguiente
        return False

    def buscar(self, dato: Any) -> bool:
        """Indica si un elemento existe en la lista.

        Complejidad temporal: **O(n)**.

        Args:
            dato: Elemento a buscar.

        Returns:
            ``True`` si el elemento está en la lista.
        """
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def a_lista(self) -> list:
        """Convierte la lista a una lista Python (solo para presentación).

        Complejidad temporal: **O(n)**.

        Returns:
            Los elementos de cabeza a cola.
        """
        elementos = []
        actual = self._cabeza
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def a_lista_invertida(self) -> list:
        """Convierte la lista a una lista Python de cola a cabeza.

        Complejidad temporal: **O(n)**.

        Returns:
            Los elementos de cola a cabeza.
        """
        elementos = []
        actual = self._cola
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.anterior
        return elementos

    def esta_vacia(self) -> bool:
        """Indica si la lista no contiene elementos.

        Returns:
            ``True`` si la lista está vacía.
        """
        return self._cabeza is None

    def __len__(self) -> int:
        """Retorna la cantidad de elementos de la lista."""
        return self._tamanio

    def __str__(self) -> str:
        """Retorna la lista representada de cabeza a cola."""
        elementos = [str(dato) for dato in self.a_lista()]
        if not elementos:
            return "ListaDoble(vacía)"
        return "ListaDoble([" + " ↔ ".join(elementos) + "])"
