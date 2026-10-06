"""Unidad III: Lista enlazada simple."""

from typing import Any


class _Nodo:
    def __init__(self, dato: Any, siguiente: "_Nodo | None" = None) -> None:
        self.dato = dato
        self.siguiente = siguiente


class ListaSimple:
    def __init__(self) -> None:
        self._cabeza: _Nodo | None = None
        self._tamanio = 0

    def insertar_inicio(self, dato: Any) -> None:
        self._cabeza = _Nodo(dato, self._cabeza)
        self._tamanio += 1

    def insertar_final(self, dato: Any) -> None:
        nuevo = _Nodo(dato)
        if self._cabeza is None:
            self._cabeza = nuevo
        else:
            actual = self._cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._tamanio += 1

    def buscar(self, dato: Any) -> bool:
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def eliminar(self, dato: Any) -> bool:
        if self._cabeza is None:
            return False
        if self._cabeza.dato == dato:
            self._cabeza = self._cabeza.siguiente
            self._tamanio -= 1
            return True
        anterior = self._cabeza
        actual = self._cabeza.siguiente
        while actual is not None:
            if actual.dato == dato:
                anterior.siguiente = actual.siguiente
                self._tamanio -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def __len__(self) -> int:
        return self._tamanio

    def __str__(self) -> str:
        elementos = []
        actual = self._cabeza
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        return " -> ".join(elementos) + " -> None"


if __name__ == "__main__":
    lista = ListaSimple()
    lista.insertar_inicio(20)
    lista.insertar_inicio(10)
    lista.insertar_final(30)

    print(lista)
    print("Buscar 20:", lista.buscar(20))
    print("Eliminar 20:", lista.eliminar(20))
    print(lista)
