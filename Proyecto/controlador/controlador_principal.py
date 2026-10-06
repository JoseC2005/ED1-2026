"""Controlador principal del Simulador de Centro Logístico.

Conecta la vista (Flet) con el modelo (estructuras y dominio) sin
que ninguno de los dos se conozca directamente.
"""

from __future__ import annotations

import flet as ft

from modelo.dominio.paquete import Paquete
from modelo.estructuras.cola import Cola, ColaVaciaError
from modelo.estructuras.lista_doble import ListaDoblementeEnlazada
from modelo.estructuras.pila import Pila
from vista.vista_principal import VistaPrincipal


class ControladorPrincipal:
    """Coordina la interacción entre :class:`VistaPrincipal` y el modelo.

    En este primer avance el controlador:

    - Registra paquetes nuevos en la cola de despacho (FIFO).
    - Despacha el paquete al frente de la cola.
    - Mantiene el historial de despachos en una lista doble.
    - Reserva la pila para el futuro deshacer/rehacer (Undo/Redo).
    """

    def __init__(self, page: ft.Page) -> None:
        """Inicializa el controlador con su vista y modelo.

        Args:
            page: Página de Flet donde se renderizará la interfaz.
        """
        self._vista = VistaPrincipal(page)
        self._cola_despacho = Cola()
        self._historial = ListaDoblementeEnlazada()
        self._pila_deshacer = Pila()
        self._pila_rehacer = Pila()

    def iniciar(self) -> None:
        """Muestra la interfaz inicial y registra los manejadores."""
        self._vista.asignar_controlador(self)
        self._vista.construir()
        self.actualizar_vista()

    def registrar_paquete(self, destino: str, peso_txt: str,
                          urgente: bool) -> None:
        """Valida la entrada y registra un paquete en la cola.

        Args:
            destino: Ciudad o dirección de destino.
            peso_txt: Peso en kilogramos ingresado como texto.
            urgente: Si el paquete debe despacharse con prioridad.
        """
        destino = destino.strip()
        if not destino:
            self._vista.mostrar_mensaje(
                "Debe ingresar un destino válido.", ft.Colors.RED
            )
            return

        try:
            peso = float(peso_txt) if peso_txt.strip() else 0.0
            if peso < 0:
                raise ValueError
        except ValueError:
            self._vista.mostrar_mensaje(
                "El peso debe ser un número mayor o igual a 0.",
                ft.Colors.RED,
            )
            return

        paquete = Paquete(destino=destino, peso_kg=peso, urgente=urgente)
        self._cola_despacho.encolar(paquete)
        self._vista.mostrar_mensaje(
            f"Paquete {paquete.identificador} registrado hacia "
            f"{destino}.",
            ft.Colors.GREEN,
        )
        self.actualizar_vista()

    def despachar_siguiente(self) -> None:
        """Despacha el paquete al frente de la cola (FIFO)."""
        try:
            paquete = self._cola_despacho.desencolar()
        except ColaVaciaError:
            self._vista.mostrar_mensaje(
                "No hay paquetes pendientes de despacho.",
                ft.Colors.ORANGE,
            )
            return

        self._historial.insertar_final(paquete)
        self._vista.mostrar_mensaje(
            f"Despachado {paquete.identificador} hacia {paquete.destino}.",
            ft.Colors.GREEN,
        )
        self.actualizar_vista()

    def actualizar_vista(self) -> None:
        """Refresca la vista con el estado actual del modelo."""
        self._vista.actualizar_estado(
            cola=self._cola_despacho.a_lista(),
            historial=self._historial.a_lista_invertida(),
            pendientes=len(self._cola_despacho),
            despachados=len(self._historial),
        )
