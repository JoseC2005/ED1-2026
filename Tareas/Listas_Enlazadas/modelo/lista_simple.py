import gc


class Nodo:
    """Nodo individual de la lista enlazada.

    Attributes:
        valor: Dato almacenado en el nodo. Puede ser cualquier objeto.
        siguiente: Referencia al proximo Nodo, o None si es el ultimo.
    """

    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

    def __repr__(self):
        return f"Nodo({self.valor!r})"

    def __del__(self):
        # Se ejecuta en el momento exacto en que Python libera (borra
        # fisicamente) este objeto de la memoria, cuando ya no le queda
        # ninguna referencia activa.
        print(f"  [GC] Nodo({self.valor!r}) liberado fisicamente de la memoria.")


class ListaVaciaError(Exception):
    """Se lanza cuando se intenta operar sobre una lista vacia"""


class ListaSimple:
    """Lista enlazada simple con operaciones basicas de gestion
    """

    def __init__(self):
        self._cabeza = None
        self._cola = None
        self._tamano = 0

    def esta_vacia(self):
        """Indica si la lista no contiene elementos
        """
        return self._tamano == 0

    def __len__(self):
        return self._tamano

    def insertar_al_inicio(self, valor):
        """Inserta un nuevo elemento como primer nodo de la lista
        """
        nuevo = Nodo(valor)
        nuevo.siguiente = self._cabeza
        self._cabeza = nuevo
        if self._cola is None:
            # La lista estaba vacia: el nuevo nodo tambien es la cola.
            self._cola = nuevo
        self._tamano += 1

    def insertar_al_final(self, valor):
        """Inserta un nuevo elemento como ultimo nodo de la lista
        """
        nuevo = Nodo(valor)
        if self.esta_vacia():
            self._cabeza = nuevo
            self._cola = nuevo
        else:
            self._cola.siguiente = nuevo
            self._cola = nuevo
        self._tamano += 1

    def buscar(self, valor):
        """Busca un valor y devuelve el Nodo que lo contiene

        Retorna None si el valor no existe en la lista
        """
        actual = self._cabeza
        while actual is not None:
            if actual.valor == valor:
                return actual
            actual = actual.siguiente
        return None

    def eliminar_por_valor(self, valor):
        """
        Desenlaza la primera aparicion de un valor en la lista.
        """
        if self._cabeza is None:
            return None

        # el valor esta en la cabeza
        if self._cabeza.valor == valor:
            nodo_a_borrar = self._cabeza
            self._cabeza = self._cabeza.siguiente
            nodo_a_borrar.siguiente = None
            if self._cabeza is None:
                self._cola = None
            self._tamano -= 1
            return nodo_a_borrar

        anterior = self._cabeza
        actual = self._cabeza.siguiente
        while actual is not None:
            if actual.valor == valor:
                anterior.siguiente = actual.siguiente
                if actual is self._cola:
                    # El nodo a eliminar era la cola.
                    self._cola = anterior
                actual.siguiente = None
                self._tamano -= 1
                return actual
            anterior = actual
            actual = actual.siguiente

        return None

    def liberar_nodo(self, nodo):
        """Libera fisicamente (de la memoria) el Nodo dado

        Borra la referencia con `del` y fuerza para que destruya el objeto
        """
        del nodo
        gc.collect()

    def recorrer(self):
        """Genera los valores de la lista en orden, de cabeza a cola
        """
        actual = self._cabeza
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def __iter__(self):
        return self.recorrer()

    def __str__(self):
        if self.esta_vacia():
            return "ListaSimple(vacia)"
        valores = " -> ".join(str(valor) for valor in self.recorrer())
        return f"ListaSimple({valores})"

    def __repr__(self):
        return self.__str__()
