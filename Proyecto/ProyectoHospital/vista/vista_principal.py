"""Vista principal del Sistema Hospitalario (Flet).

Dibuja una única pantalla con:

- Un formulario para registrar pacientes (nombre, edad, motivo, área y
  severidad).
- Tres paneles que muestran el estado de las estructuras: urgencias (cola
  de prioridad), consulta externa (cola FIFO) e historial (pila).
- Botones para atender urgencia, atender consulta y deshacer la última
  atención.

La vista no contiene lógica de negocio: solo dibuja y avisa al controlador
(patrón MVC).
"""

from __future__ import annotations

from typing import Any, Optional

import flet as ft

from modelo.dominio.paciente import Paciente

# --- Paleta de colores ---------------------------------------------------
AZUL = "#1E88E5"
VERDE = "#43A047"
ROJO = "#E53935"
NARANJA = "#FB8C00"
GRIS = "#757575"
GRIS_LINEA = "#E0E0E0"
TEXTO = "#212121"
BLANCO = "#FFFFFF"
FONDO = "#F5F7FA"

AREAS = ["urgencias", "consulta"]

SEVERIDAD_TEXTO = {
    1: "1 · Leve",
    2: "2 · Moderada",
    3: "3 · Media",
    4: "4 · Alta",
    5: "5 · Crítico",
}


class VistaPrincipal:
    """Interfaz gráfica del sistema hospitalario."""

    def __init__(self, page: ft.Page) -> None:
        """Guarda la página de Flet y crea todos los controles.

        Args:
            page: Página de Flet donde se renderizará la interfaz.
        """
        self.pagina = page
        self.controlador: Optional[Any] = None
        self._crear_controles()

    # ------------------------------------------------------------------
    # Creación de controles
    # ------------------------------------------------------------------
    def _crear_controles(self) -> None:
        """Crea los controles que el controlador actualizará después."""
        # --- Formulario de registro ---
        self.campo_nombre = ft.TextField(
            label="Nombre",
            hint_text="Nombre del paciente",
            expand=True,
        )
        self.campo_edad = ft.TextField(
            label="Edad",
            value="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=90,
        )
        self.campo_motivo = ft.TextField(
            label="Motivo / síntoma",
            hint_text="Ej. dolor de cabeza",
            expand=True,
        )
        self.desplegable_area = ft.Dropdown(
            label="Área",
            value="urgencias",
            width=150,
            options=[
                ft.dropdown.Option(area, area.capitalize()) for area in AREAS
            ],
        )
        self.desplegable_severidad = ft.Dropdown(
            label="Severidad",
            value=3,
            width=130,
            options=[
                ft.dropdown.Option(sev, SEVERIDAD_TEXTO[sev])
                for sev in SEVERIDAD_TEXTO
            ],
        )
        self.boton_registrar = ft.FilledButton(
            content="Registrar paciente",
            icon=ft.Icons.PERSON_ADD,
            on_click=self._al_registrar,
        )

        # --- Acciones ---
        self.boton_atender_urgencia = ft.FilledButton(
            content="Atender urgencia",
            icon=ft.Icons.EMERGENCY,
            on_click=self._al_atender_urgencia,
        )
        self.boton_atender_consulta = ft.FilledButton(
            content="Atender consulta",
            icon=ft.Icons.FACT_CHECK,
            on_click=self._al_atender_consulta,
        )
        self.boton_deshacer = ft.OutlinedButton(
            content="Deshacer última atención",
            icon=ft.Icons.UNDO,
            on_click=self._al_deshacer,
        )

        # --- Listados de las tres estructuras ---
        self.lista_urgencias = ft.ListView(spacing=4, expand=True)
        self.lista_consulta = ft.ListView(spacing=4, expand=True)
        self.lista_historial = ft.ListView(spacing=4, expand=True)

        # --- Mensaje de estado ---
        self.texto_mensaje = ft.Text("", size=13, color=AZUL)
    # ------------------------------------------------------------------
    # Construcción de la pantalla
    # ------------------------------------------------------------------
    def construir(self) -> None:
        """Ensambla y agrega la interfaz a la página."""
        self.pagina.title = "Sistema Hospitalario"
        self.pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.pagina.bgcolor = FONDO
        self.pagina.padding = 24
        self.pagina.scroll = ft.ScrollMode.AUTO

        encabezado = ft.Column(
            [
                ft.Text(
                    "Sistema Hospitalario",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=TEXTO,
                ),
                ft.Text(
                    "ED1 · Estructuras de Datos I — Urgencias (cola de "
                    "prioridad), Consulta externa (cola) e Historial (pila).",
                    size=13,
                    color=GRIS,
                ),
            ],
            spacing=4,
        )

        panel_formulario = ft.Container(
            bgcolor=BLANCO,
            border_radius=14,
            padding=16,
            content=ft.Column(
                [
                    ft.Text(
                        "Registrar paciente",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=TEXTO,
                    ),
                    ft.Row(
                        [self.campo_nombre, self.campo_edad, self.campo_motivo],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    ft.Row(
                        [
                            self.desplegable_area,
                            self.desplegable_severidad,
                            self.boton_registrar,
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=10,
            ),
        )

        fila_acciones = ft.Row(
            [
                self.boton_atender_urgencia,
                self.boton_atender_consulta,
                self.boton_deshacer,
                ft.Container(content=self.texto_mensaje, expand=True),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        panel_urgencias = self._crear_panel(
            "Urgencias",
            "Cola de prioridad · mayor severidad primero",
            ROJO,
            self.lista_urgencias,
        )
        panel_consulta = self._crear_panel(
            "Consulta externa",
            "Cola FIFO · orden de llegada",
            VERDE,
            self.lista_consulta,
        )
        panel_historial = self._crear_panel(
            "Historial",
            "Pila LIFO · lo último atendido arriba",
            NARANJA,
            self.lista_historial,
        )

        fila_paneles = ft.Row(
            [panel_urgencias, panel_consulta, panel_historial],
            spacing=12,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        self.pagina.add(
            ft.Column(
                [
                    encabezado,
                    panel_formulario,
                    fila_acciones,
                    fila_paneles,
                ],
                spacing=16,
                expand=True,
            )
        )

    def _crear_panel(
        self,
        titulo: str,
        subtitulo: str,
        color: str,
        lista: ft.ListView,
    ) -> ft.Container:
        """Crea un contenedor con título, subtítulo y su listado.

        Args:
            titulo: Título del panel.
            subtitulo: Descripción corta de la estructura.
            color: Color de acento del panel.
            lista: ListView que mostrará los elementos.

        Returns:
            El contenedor del panel.
        """
        return ft.Container(
            bgcolor=BLANCO,
            border_radius=14,
            padding=14,
            expand=True,
            border=ft.Border(top=ft.BorderSide(3, color)),
            content=ft.Column(
                [
                    ft.Text(
                        titulo,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=color,
                    ),
                    ft.Text(subtitulo, size=11, color=GRIS),
                    ft.Divider(height=1, color=GRIS_LINEA),
                    lista,
                ],
                spacing=6,
                expand=True,
            ),
        )
    # ------------------------------------------------------------------
    # Sincronización con el controlador
    # ------------------------------------------------------------------
    def asignar_controlador(self, controlador: Any) -> None:
        """Conecta esta vista con su controlador."""
        self.controlador = controlador

    def actualizar_estado(
        self,
        urgencias: list,
        consulta: list,
        historial: list,
    ) -> None:
        """Refresca los tres listados con el estado actual del modelo.

        Args:
            urgencias: Pacientes de la cola de prioridad (mayor a menor).
            consulta: Pacientes de la cola FIFO.
            historial: Pacientes atendidos (lo más reciente primero).
        """
        self.lista_urgencias.controls = (
            [self._crear_fila_paciente(p, "urgencias") for p in urgencias]
            or [self._crear_vacio("Sin pacientes en espera")]
        )
        self.lista_consulta.controls = (
            [self._crear_fila_paciente(p, "consulta") for p in consulta]
            or [self._crear_vacio("Sin pacientes en espera")]
        )
        self.lista_historial.controls = (
            [self._crear_fila_paciente(p, "historial") for p in historial]
            or [self._crear_vacio("Sin atenciones registradas")]
        )
        self.pagina.update()

    def limpiar_formulario(self) -> None:
        """Vuelve el formulario a sus valores iniciales."""
        self.campo_nombre.value = ""
        self.campo_edad.value = "0"
        self.campo_motivo.value = ""
        self.desplegable_area.value = "urgencias"
        self.desplegable_severidad.value = 3

    def mostrar_mensaje(self, mensaje: str) -> None:
        """Muestra un mensaje de estado al usuario.

        Args:
            mensaje: Texto informativo o de aviso.
        """
        self.texto_mensaje.value = mensaje
        self.pagina.update()
    # ------------------------------------------------------------------
    # Dibujo de filas
    # ------------------------------------------------------------------
    def _crear_fila_paciente(
        self, paciente: Paciente, area: str
    ) -> ft.Container:
        """Dibuja una fila con la información del paciente.

        Args:
            paciente: Paciente a dibujar.
            area: Contexto de la fila (``"urgencias"``, ``"consulta"`` o
                ``"historial"``).

        Returns:
            El contenedor de la fila.
        """
        if area == "urgencias":
            titulo = ft.Text(
                paciente.nombre,
                size=14,
                weight=ft.FontWeight.BOLD,
                color=TEXTO,
            )
            detalle = ft.Text(
                f"{paciente.edad} años · {paciente.motivo}",
                size=12,
                color=GRIS,
            )
            derecha = self._crear_etiqueta_severidad(paciente.severidad)
        elif area == "consulta":
            titulo = ft.Text(
                paciente.nombre,
                size=14,
                weight=ft.FontWeight.BOLD,
                color=TEXTO,
            )
            detalle = ft.Text(
                f"{paciente.edad} años · {paciente.motivo}",
                size=12,
                color=GRIS,
            )
            derecha = ft.Text("en espera", size=11, color=VERDE)
        else:  # historial
            titulo = ft.Text(paciente.nombre, size=14, color=TEXTO)
            detalle = ft.Text(
                f"atendido en {paciente.area} · {paciente.hora_llegada}",
                size=12,
                color=GRIS,
            )
            derecha = ft.Icon(ft.Icons.CHECK_CIRCLE, color=VERDE, size=16)

        return ft.Container(
            bgcolor=FONDO,
            border_radius=8,
            padding=ft.Padding.symmetric(horizontal=10, vertical=8),
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [titulo, detalle], spacing=2, tight=True
                        ),
                        expand=True,
                    ),
                    derecha,
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def _crear_etiqueta_severidad(self, severidad: int) -> ft.Container:
        """Crea una etiqueta de color según la severidad.

        Args:
            severidad: Gravedad del paciente (1–5).

        Returns:
            Contenedor con la etiqueta ``severidad/5``.
        """
        colores = {1: VERDE, 2: AZUL, 3: NARANJA, 4: ROJO, 5: "#B71C1C"}
        color = colores.get(severidad, GRIS)
        return ft.Container(
            bgcolor=color,
            border_radius=10,
            padding=ft.Padding.symmetric(horizontal=8, vertical=3),
            content=ft.Text(
                f"{severidad}/5",
                size=11,
                color=BLANCO,
                weight=ft.FontWeight.BOLD,
            ),
        )

    def _crear_vacio(self, texto: str) -> ft.Container:
        """Crea un contenedor con un texto de "vacío".

        Args:
            texto: Mensaje a mostrar cuando no hay elementos.

        Returns:
            Contenedor con el texto centrado.
        """
        return ft.Container(
            alignment=ft.Alignment.CENTER,
            padding=ft.Padding.symmetric(vertical=14),
            content=ft.Text(texto, size=12, italic=True, color=GRIS),
        )

    # ------------------------------------------------------------------
    # Manejadores de eventos (avisar al controlador)
    # ------------------------------------------------------------------
    def _al_registrar(self, evento: Any) -> None:
        """Registra un paciente con los datos del formulario."""
        if self.controlador is not None:
            self.controlador.registrar_paciente(
                nombre=self.campo_nombre.value,
                edad=self.campo_edad.value,
                motivo=self.campo_motivo.value,
                area=self.desplegable_area.value,
                severidad=self.desplegable_severidad.value,
            )

    def _al_atender_urgencia(self, evento: Any) -> None:
        """Atiende al paciente más grave de urgencias."""
        if self.controlador is not None:
            self.controlador.atender_urgencia()

    def _al_atender_consulta(self, evento: Any) -> None:
        """Atiende al primer paciente de consulta externa."""
        if self.controlador is not None:
            self.controlador.atender_consulta()

    def _al_deshacer(self, evento: Any) -> None:
        """Deshace la última atención registrada."""
        if self.controlador is not None:
            self.controlador.deshacer_ultima_atencion()



