"""Controlador principal del Reproductor de Música.

Conecta la vista (Flet) con el modelo (estructuras y dominio) sin
que ninguno de los dos se conozca directamente.
"""

from __future__ import annotations

from typing import Optional

import flet as ft

from modelo.dominio.cancion import Cancion
from modelo.estructuras.cola import Cola, ColaVaciaError
from modelo.estructuras.pila import Pila
from vista.vista_principal import VistaPrincipal


class ControladorPrincipal:
    """Coordina la interacción entre :class:`VistaPrincipal` y el modelo.

    En este avance el controlador:

    - Agrega canciones nuevas a la cola de reproducción (FIFO).
    - Reproduce la canción que lleva más tiempo esperando.
    - Guarda lo ya reproducido en una pila (lo último arriba).
    """

    def __init__(self, page: ft.Page) -> None:
        """Inicializa el controlador con su vista y modelo.

        Args:
            page: Página de Flet donde se renderizará la interfaz.
        """
        self.vista = VistaPrincipal(page)
        self.cola_de_reproduccion = Cola()
        self.historial_de_reproducidas = Pila()
        self.cancion_sonando: Optional[Cancion] = None

    def iniciar(self) -> None:
        """Muestra la interfaz inicial y registra los manejadores."""
        self.vista.asignar_controlador(self)
        self.vista.construir()
        self.actualizar_vista()

    def agregar_cancion(self, titulo: str, artista: str,
                        duracion: str, favorita: bool) -> None:
        """Valida la entrada y agrega una canción a la cola.

        Args:
            titulo: Nombre de la canción.
            artista: Intérprete de la canción.
            duracion: Duración en formato texto (ej. "3:45").
            favorita: Si la canción se marca como favorita.
        """
        titulo = titulo.strip()
        if not titulo:
            self.vista.mostrar_mensaje(
                "Debe ingresar un título válido.", ft.Colors.RED
            )
            return

        cancion = Cancion(
            titulo=titulo,
            artista=artista.strip() or "Desconocido",
            duracion=duracion.strip() or "?:??",
            favorita=favorita,
        )
        self.cola_de_reproduccion.encolar(cancion)
        self.vista.mostrar_mensaje(
            f"Canción {cancion.identificador} «{cancion.titulo}» "
            f"agregada a la cola.",
            ft.Colors.GREEN,
        )
        self.actualizar_vista()

    def reproducir_siguiente(self) -> None:
        """Reproduce la primera canción de la cola (FIFO)."""
        try:
            cancion = self.cola_de_reproduccion.desencolar()
        except ColaVaciaError:
            self.vista.mostrar_mensaje(
                "No hay canciones en la cola.",
                ft.Colors.ORANGE,
            )
            return

        # La que venía sonando pasa al historial (pila LIFO)
        if self.cancion_sonando is not None:
            self.historial_de_reproducidas.apilar(self.cancion_sonando)
        self.cancion_sonando = cancion

        self.vista.mostrar_mensaje(
            f"Reproduciendo {cancion.identificador} «{cancion.titulo}».",
            ft.Colors.GREEN,
        )
        self.actualizar_vista()

    def actualizar_vista(self) -> None:
        """Refresca la vista con el estado actual del modelo."""
        self.vista.actualizar_estado(
            sonando=self.cancion_sonando,
            en_cola=self.cola_de_reproduccion.a_lista(),
            reproducidas=self.historial_de_reproducidas.a_lista(),
            cantidad_en_cola=len(self.cola_de_reproduccion),
            cantidad_reproducidas=len(self.historial_de_reproducidas),
        )