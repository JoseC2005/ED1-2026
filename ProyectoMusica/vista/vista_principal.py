"""Vista principal del Reproductor de Música (Flet).

Solo dibuja la interfaz (tema oscuro y diseño simple);
la lógica vive en el modelo y el controlador (MVC).
"""

from __future__ import annotations

from typing import Any, Optional

import flet as ft


class VistaPrincipal:
    """Interfaz gráfica del reproductor de música."""

    def __init__(self, page: ft.Page) -> None:
        """Guarda la página de Flet donde se dibujará la interfaz."""
        self.pagina = page
        self.controlador: Optional[Any] = None

        # Campos para agregar una canción
        self.campo_titulo = ft.TextField(label="Título", width=240)
        self.campo_artista = ft.TextField(label="Artista", width=200)
        self.campo_duracion = ft.TextField(label="Duración (3:45)",
                                           width=140)
        self.casilla_favorita = ft.Checkbox(label="Favorita", value=False)

        # Textos que cambian con el estado del sistema
        self.texto_mensaje = ft.Text("", size=14)
        self.texto_sonando = ft.Text(
            "♪ Nada sonando todavía", size=16, weight="bold"
        )
        self.texto_en_cola = ft.Text("0", size=24, weight="bold")
        self.texto_reproducidas = ft.Text("0", size=24, weight="bold")

        # Listas donde se dibujan las canciones
        self.lista_cola = ft.Column(
            spacing=6, scroll=ft.ScrollMode.AUTO, expand=True
        )
        self.lista_reproducidas = ft.Column(
            spacing=6, scroll=ft.ScrollMode.AUTO, expand=True
        )

    def asignar_controlador(self, controlador: Any) -> None:
        """Conecta esta vista con su controlador."""
        self.controlador = controlador

    def construir(self) -> None:
        """Diseña la interfaz oscura y la publica en la página."""
        self.pagina.title = "Reproductor de Música"
        self.pagina.window.width = 940
        self.pagina.window.height = 600
        self.pagina.padding = 16
        self.pagina.theme_mode = ft.ThemeMode.DARK

        boton_agregar = ft.FilledButton(
            "Agregar a la cola",
            icon=ft.Icons.PLAYLIST_ADD,
            on_click=self._al_agregar,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: "#6A1B9A",
                    ft.ControlState.HOVERED: "#8E24AA",
                },
                color="#FFFFFF",
                icon_color="#FFFFFF",
                icon_size=18,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=18,
                elevation=2,
            ),
        )
        boton_reproducir = ft.OutlinedButton(
            "Reproducir siguiente",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self._al_reproducir,
            style=ft.ButtonStyle(
                color="#CE93D8",
                bgcolor={
                    ft.ControlState.DEFAULT: "transparent",
                    ft.ControlState.HOVERED: "#2A1B3A",
                },
                side=ft.BorderSide(1.5, "#CE93D8"),
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=18,
                icon_size=18,
            ),
        )

        barra_sonando = ft.Container(
            content=self.texto_sonando,
            padding=14,
            bgcolor="#2A1B3A",
            border_radius=10,
        )

        self.pagina.add(
            ft.Column(
                [
                    ft.Text("🎵 Reproductor de Música",
                            size=24, weight="bold"),
                    ft.Row(
                        [
                            self.campo_titulo,
                            self.campo_artista,
                            self.campo_duracion,
                            self.casilla_favorita,
                        ],
                        spacing=10,
                    ),
                    ft.Row(
                        [boton_agregar, boton_reproducir],
                        spacing=10,
                    ),
                    self.texto_mensaje,
                    barra_sonando,
                    ft.Row(
                        [
                            self._crear_panel(
                                "Cola de reproducción (FIFO)",
                                self.texto_en_cola,
                                self.lista_cola,
                            ),
                            self._crear_panel(
                                "Historial (lo último arriba)",
                                self.texto_reproducidas,
                                self.lista_reproducidas,
                            ),
                        ],
                        spacing=12,
                        expand=True,
                    ),
                ],
                spacing=14,
                expand=True,
            )
        )

    def _crear_panel(self, titulo: str, contador: ft.Text,
                     lista: ft.Column) -> ft.Container:
        """Crea un panel con su título, su contador y su lista."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(titulo, size=16, weight="bold"),
                            contador,
                        ]
                    ),
                    lista,
                ],
                spacing=8,
                expand=True,
            ),
            padding=12,
            bgcolor="#1E2430",
            border_radius=10,
            expand=True,
        )

    def mostrar_mensaje(self, texto: str, color: Any) -> None:
        """Muestra un mensaje de estado debajo de los botones."""
        self.texto_mensaje.value = texto
        self.texto_mensaje.color = color
        self.pagina.update()

    def actualizar_estado(self, sonando: Any, en_cola: list,
                          reproducidas: list, cantidad_en_cola: int,
                          cantidad_reproducidas: int) -> None:
        """Actualiza los contadores, la barra y las listas.

        Args:
            sonando: Canción sonando ahora o ``None``.
            en_cola: Canciones esperando en la cola (primero a último).
            reproducidas: Canciones reproducidas (más reciente primero).
            cantidad_en_cola: Cuántas canciones esperan en la cola.
            cantidad_reproducidas: Cuántas canciones ya sonaron.
        """
        self.texto_en_cola.value = str(cantidad_en_cola)
        self.texto_reproducidas.value = str(cantidad_reproducidas)

        if sonando is None:
            self.texto_sonando.value = "♪ Nada sonando todavía"
        else:
            self.texto_sonando.value = f"♪ Sonando: {sonando}"

        self.lista_cola.controls = (
            [self._crear_linea(c) for c in en_cola]
            or [ft.Text("La cola está vacía.", italic=True,
                        color=ft.Colors.GREY)]
        )
        self.lista_reproducidas.controls = (
            [self._crear_linea(c) for c in reproducidas]
            or [ft.Text("Aún no terminó ninguna canción.",
                        italic=True, color=ft.Colors.GREY)]
        )
        self.pagina.update()

    def _crear_linea(self, cancion: Any) -> ft.Text:
        """Dibuja una canción como una línea de texto
        (dorada si es favorita)."""
        if cancion.favorita:
            return ft.Text(str(cancion), size=13, color="#FFD54F")
        return ft.Text(str(cancion), size=13)

    def _al_agregar(self, evento: ft.TapEvent) -> None:
        """Se ejecuta al presionar «Agregar a la cola»."""
        if self.controlador is None:
            return
        self.controlador.agregar_cancion(
            titulo=self.campo_titulo.value or "",
            artista=self.campo_artista.value or "",
            duracion=self.campo_duracion.value or "",
            favorita=bool(self.casilla_favorita.value),
        )
        self.campo_titulo.value = ""
        self.campo_duracion.value = ""
        self.casilla_favorita.value = False
        self.pagina.update()

    def _al_reproducir(self, evento: ft.TapEvent) -> None:
        """Se ejecuta al presionar «Reproducir siguiente»."""
        if self.controlador is None:
            return
        self.controlador.reproducir_siguiente()
