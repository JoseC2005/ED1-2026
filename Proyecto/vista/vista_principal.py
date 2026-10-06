"""Vista principal del Simulador de Centro Logístico (Flet).

Esta capa **solo** construye la interfaz; toda la lógica de negocio
vive en el modelo y el controlador (MVC).
"""

from __future__ import annotations

from typing import Any, Optional

import flet as ft


class VistaPrincipal:
    """Interfaz gráfica del centro logístico construida con Flet."""

    def __init__(self, page: ft.Page) -> None:
        """Guarda la página de Flet donde se renderizará la vista.

        Args:
            page: Página de Flet proporcionada por el runtime.
        """
        self._page = page
        self._controlador: Optional[Any] = None

        # Controles de entrada
        self.campo_destino = ft.TextField(
            label="Destino",
            hint_text="Ej: La Paz, Santa Cruz, Cochabamba...",
            width=280,
        )
        self.campo_peso = ft.TextField(
            label="Peso (kg)",
            hint_text="Ej: 12.5",
            width=140,
        )
        self.interruptor_urgente = ft.Switch(label="Urgente", value=False)

        # Etiquetas de estado
        self.etiqueta_mensaje = ft.Text("", size=14)
        self.etiqueta_pendientes = ft.Text("0", size=28, weight="bold")
        self.etiqueta_despachados = ft.Text("0", size=28, weight="bold")

        # Listas de la interfaz
        self.lista_cola = ft.Column(spacing=6)
        self.lista_historial = ft.Column(spacing=6)

    def asignar_controlador(self, controlador: Any) -> None:
        """Conecta esta vista con su controlador.

        Args:
            controlador: Instancia de ``ControladorPrincipal``.
        """
        self._controlador = controlador

    def construir(self) -> None:
        """Diseña la interfaz y la publica en la página."""
        page = self._page
        page.title = "Simulador de Centro Logístico"
        page.window.width = 960
        page.window.height = 640
        page.padding = 20
        page.theme_mode = ft.ThemeMode.LIGHT

        boton_registrar = ft.OutlinedButton(
            "Registrar paquete",
            icon=ft.Icons.ADD_SHOPPING_CART,
            on_click=self._al_registrar,
        )
        boton_despachar = ft.FilledButton(
            "Despachar siguiente",
            icon=ft.Icons.LOCAL_SHIPPING,
            on_click=self._al_despachar,
        )

        formulario = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Registro de paquetes", size=18, weight="bold"),
                    ft.Row(
                        [self.campo_destino, self.campo_peso],
                        spacing=12,
                    ),
                    ft.Row(
                        [
                            self.interruptor_urgente,
                            boton_registrar,
                            boton_despachar,
                        ],
                        spacing=12,
                    ),
                    self.etiqueta_mensaje,
                ],
                spacing=12,
            ),
            padding=16,
            border=self._borde(ft.Colors.OUTLINE),
            border_radius=10,
        )

        tarjetas_resumen = ft.Row(
            [
                self._tarjeta(
                    "Paquetes pendientes", self.etiqueta_pendientes
                ),
                self._tarjeta(
                    "Paquetes despachados", self.etiqueta_despachados
                ),
            ],
            spacing=16,
        )

        panel_cola = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Cola de despacho (FIFO)", size=16,
                            weight="bold"),
                    self.lista_cola,
                ],
                spacing=10,
            ),
            padding=16,
            border=self._borde(ft.Colors.OUTLINE),
            border_radius=10,
            expand=True,
        )

        panel_historial = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Historial de despachos", size=16,
                            weight="bold"),
                    self.lista_historial,
                ],
                spacing=10,
            ),
            padding=16,
            border=self._borde(ft.Colors.OUTLINE),
            border_radius=10,
            expand=True,
        )

        page.add(
            ft.AppBar(
                title=ft.Text("📦 Centro Logístico de Distribución"),
                bgcolor=ft.Colors.SURFACE_CONTAINER,
            ),
            ft.Column(
                [
                    tarjetas_resumen,
                    formulario,
                    ft.Row(
                        [panel_cola, panel_historial],
                        spacing=16,
                        expand=True,
                    ),
                ],
                spacing=16,
                expand=True,
            ),
        )


    def _tarjeta(self, titulo: str, valor: ft.Text) -> ft.Container:
        """Crea una tarjeta de resumen con un título y un valor.

        Args:
            titulo: Texto superior de la tarjeta.
            valor: Control de texto con el contador.

        Returns:
            Contenedor con el diseño de la tarjeta.
        """
        return ft.Container(
            content=ft.Column(
                [ft.Text(titulo, size=13), valor],
                spacing=4,
                horizontal_alignment="center",
            ),
            padding=16,
            border=self._borde(ft.Colors.OUTLINE),
            border_radius=10,
            width=220,
            alignment=ft.Alignment.CENTER,
        )

    def _borde(self, color: ft.Colors) -> ft.Border:
        """Crea un borde de 1 px con el color indicado.

        Args:
            color: Color del borde.

        Returns:
            Objeto :class:`ft.Border` de cuatro lados iguales.
        """
        lado = ft.BorderSide(1, color)
        return ft.Border(left=lado, right=lado, top=lado, bottom=lado)

    def mostrar_mensaje(self, texto: str, color: ft.Colors) -> None:
        """Muestra un mensaje de estado en la interfaz.

        Args:
            texto: Mensaje a mostrar.
            color: Color del mensaje (éxito, error, advertencia).
        """
        self.etiqueta_mensaje.value = texto
        self.etiqueta_mensaje.color = color
        self._page.update()

    def actualizar_estado(self, cola: list, historial: list,
                          pendientes: int, despachados: int) -> None:
        """Actualiza listas y contadores con el estado del modelo.

        Args:
            cola: Paquetes pendientes (de frente a fondo).
            historial: Paquetes despachados (más recientes primero).
            pendientes: Cantidad de paquetes en cola.
            despachados: Cantidad de paquetes despachados.
        """
        self.etiqueta_pendientes.value = str(pendientes)
        self.etiqueta_despachados.value = str(despachados)

        self.lista_cola.controls = (
            [self._tarjeta_paquete(p) for p in cola]
            or [ft.Text("Cola vacía.", italic=True, color=ft.Colors.GREY)]
        )
        self.lista_historial.controls = (
            [self._tarjeta_paquete(p) for p in historial]
            or [
                ft.Text("Sin despachos registrados.",
                        italic=True, color=ft.Colors.GREY)
            ]
        )
        self._page.update()

    def _tarjeta_paquete(self, paquete: Any) -> ft.Container:
        """Dibuja un paquete como tarjeta dentro de una lista.

        Args:
            paquete: Instancia de ``Paquete``.

        Returns:
            Contenedor con los datos del paquete.
        """
        color_borde = (
            ft.Colors.ORANGE if paquete.urgente else ft.Colors.OUTLINE
        )
        return ft.Container(
            content=ft.Text(str(paquete), size=13),
            padding=10,
            border=self._borde(color_borde),
            border_radius=8,
        )

    def _al_registrar(self, evento: ft.TapEvent) -> None:
        """Manejador del botón «Registrar paquete»."""
        if self._controlador is None:
            return
        self._controlador.registrar_paquete(
            destino=self.campo_destino.value or "",
            peso_txt=self.campo_peso.value or "",
            urgente=bool(self.interruptor_urgente.value),
        )
        self.campo_destino.value = ""
        self.campo_peso.value = ""
        self._page.update()

    def _al_despachar(self, evento: ft.TapEvent) -> None:
        """Manejador del botón «Despachar siguiente»."""
        if self._controlador is None:
            return
        self._controlador.despachar_siguiente()
