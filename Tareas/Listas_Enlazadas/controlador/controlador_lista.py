"""Controlador del patron MVC: conecta la Vista con el Modelo.

Traduce eventos de la vista en llamadas a ListaSimple, y refleja el
resultado de vuelta en la vista.
"""


class ControladorLista:
    """Coordina la ListaSimple (modelo) y la VistaPrincipal (vista)."""

    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self._nodo_apartado = None
        self.vista.asignar_controlador(self)
        self._refrescar_vista()

    def insertar_al_inicio(self, valor):
        """Inserta un valor al inicio de la lista."""
        if not self._validar_valor(valor):
            return
        self.modelo.insertar_al_inicio(valor)
        self.vista.limpiar_entrada()
        self.vista.mostrar_mensaje_info(f"'{valor}' insertado al inicio.")
        self._refrescar_vista()

    def insertar_al_final(self, valor):
        """Inserta un valor al final de la lista."""
        if not self._validar_valor(valor):
            return
        self.modelo.insertar_al_final(valor)
        self.vista.limpiar_entrada()
        self.vista.mostrar_mensaje_info(f"'{valor}' insertado al final.")
        self._refrescar_vista()

    def buscar(self, valor):
        """Busca un valor en la lista y muestra si existe."""
        if not self._validar_valor(valor):
            return

        nodo = self.modelo.buscar(valor)
        if nodo is None:
            self.vista.mostrar_mensaje_error(
                f"'{valor}' no esta en la lista.")
        else:
            self.vista.mostrar_dialogo_info(
                "Busqueda", f"'{valor}' SI esta en la lista.")
            self.vista.mostrar_mensaje_info(f"'{valor}' encontrado.")

    def eliminar(self, valor):
        """Desenlaza un valor de la lista y lo aparta como bloque flotante

        El nodo deja de formar parte de la lista (se desconecta) pero
        todavia existe en memoria
        """
        if not self._validar_valor(valor):
            return

        nodo = self.modelo.eliminar_por_valor(valor)
        self.vista.limpiar_entrada()
        if nodo is None:
            self.vista.mostrar_mensaje_error(
                f"'{valor}' no estaba en la lista.")
            return

        self._nodo_apartado = nodo
        self.vista.mostrar_mensaje_info(
            f"'{valor}' Eliminado.")
        self._refrescar_vista()

    def eliminar_fisicamente(self):
        """Libera de la memoria el nodo que estaba apartado (si lo hay)."""
        if self._nodo_apartado is None:
            self.vista.mostrar_mensaje_error(
                "No hay ningun bloque apartado que eliminar. "
                "Pulsa primero 'Eliminar'.")
            return

        valor = self._nodo_apartado.valor
        self.modelo.liberar_nodo(self._nodo_apartado)
        self._nodo_apartado = None
        self.vista.mostrar_mensaje_info(
            "Memoria Liberada")
        self._refrescar_vista()

    def _validar_valor(self, valor):
        if not valor or not valor.strip():
            self.vista.mostrar_mensaje_error("Escribe un valor primero")
            return False
        return True

    def _refrescar_vista(self):
        if self.modelo.esta_vacia():
            self.vista.mostrar_mensaje_info("Lista vacia")
        # Redibuja los bloques
        self.vista.actualizar_lista(
            list(self.modelo.recorrer()),
            self._nodo_apartado.valor if self._nodo_apartado else None)
