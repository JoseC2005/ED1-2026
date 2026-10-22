"""Cola de prioridad — atiende primero al elemento de mayor prioridad.

En el hospital se usa para la sala de **urgencias**: cada paciente entra con
una severidad (1–5) y siempre se atiende primero al más grave. Se implementa
con nodos enlazados: cada elemento se inserta ordenado por prioridad para que
``desencolar`` sea O(1).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from modelo.estructuras.nodo import Nodo


@dataclass
class _ElementoPrioridad:
    """Par (dato, prioridad) guardado dentro de cada nodo."""

    dato: Any
    prioridad: int


class ColaPrioridadVaciaError(Exception):
    """Se lanza al intentar operar sobre una cola de prioridad vacía."""


class ColaPrioridad:
    """Cola de prioridad implementada con nodos enlazados ordenados.

    Mayor número de prioridad = mayor urgencia = se atiende antes.

    Ejemplo:
        >>> cola = ColaPrioridad()
        >>> cola.encolar("leve", 1)
        >>> cola.encolar("crítico", 5)
        >>> cola.desencolar()
        'crítico'
    """

    def __init__(self) -> None:
        """Crea una cola de prioridad vacía."""
        self._nodo_primero: Optional[Nodo] = None
        self._cantidad_de_elementos: int = 0

    def encolar(self, dato: Any, prioridad: int) -> None:
        """Inserta un elemento según su prioridad. Complejidad: **O(n)**.

        Los elementos con mayor prioridad quedan al frente de la cola. Ante
        un empate de prioridad se conserva el orden de llegada (FIFO).

        Args:
            dato: Elemento a encolar.
            prioridad: Valor numérico; mayor número = mayor prioridad.
        """
        nuevo_nodo = Nodo(_ElementoPrioridad(dato, prioridad))
        if (
            self._nodo_primero is None
            or prioridad > self._nodo_primero.dato.prioridad
        ):
            nuevo_nodo.siguiente = self._nodo_primero
            self._nodo_primero = nuevo_nodo
        else:
            actual = self._nodo_primero
            while (
                actual.siguiente is not None
                and actual.siguiente.dato.prioridad >= prioridad
            ):
                actual = actual.siguiente
            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo
        self._cantidad_de_elementos += 1

    def desencolar(self) -> Any:
        """Elimina y retorna el elemento de mayor prioridad. **O(1)**.

        Returns:
            El dato de mayor prioridad (el que estaba al frente).

        Raises:
            ColaPrioridadVaciaError: Si la cola no contiene elementos.
        """
        if self.esta_vacia():
            raise ColaPrioridadVaciaError(
                "No se puede desencolar: la cola de prioridad está vacía"
            )
        dato = self._nodo_primero.dato.dato
        self._nodo_primero = self._nodo_primero.siguiente
        self._cantidad_de_elementos -= 1
        return dato

    def ver_primero(self) -> Any:
        """Retorna el elemento de mayor prioridad sin eliminarlo.

        Returns:
            El dato de mayor prioridad.

        Raises:
            ColaPrioridadVaciaError: Si la cola no contiene elementos.
        """
        if self.esta_vacia():
            raise ColaPrioridadVaciaError("La cola de prioridad está vacía")
        return self._nodo_primero.dato.dato

    def esta_vacia(self) -> bool:
        """Indica si la cola de prioridad no contiene elementos."""
        return self._nodo_primero is None

    def __len__(self) -> int:
        """Retorna la cantidad de elementos de la cola."""
        return self._cantidad_de_elementos

    def a_lista(self) -> list:
        """Convierte la cola a una lista Python (solo para presentación).

        Returns:
            Los datos ordenados de mayor a menor prioridad.
        """
        elementos = []
        actual = self._nodo_primero
        while actual is not None:
            elementos.append(actual.dato.dato)
            actual = actual.siguiente
        return elementos

    def __str__(self) -> str:
        """Retorna la cola representada de mayor a menor prioridad."""
        elementos = [str(dato) for dato in self.a_lista()]
        if not elementos:
            return "ColaPrioridad(vacía)"
        return "ColaPrioridad(frente→ [" + ", ".join(elementos) + "] ←final)"
