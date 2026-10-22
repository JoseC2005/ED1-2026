"""Controlador principal del Sistema Hospitalario.

Conecta la vista (Flet) con el modelo (estructuras y dominio) siguiendo el
patrón MVC. Gestiona tres estructuras de datos:

- ``ColaPrioridad``: sala de urgencias (mayor severidad = se atiende antes).
- ``Cola``: consulta externa (orden de llegada, FIFO).
- ``Pila``: historial de pacientes atendidos (lo último atendido, arriba).
"""

from __future__ import annotations

import flet as ft

from modelo.dominio.paciente import Paciente
from modelo.estructuras.cola import Cola
from modelo.estructuras.cola_prioridad import ColaPrioridad
from modelo.estructuras.pila import Pila
from vista.vista_principal import VistaPrincipal


def _a_entero(valor, por_defecto: int = 0) -> int:
    """Convierte un valor a entero de forma segura.

    Args:
        valor: Valor a convertir (puede ser texto o número).
        por_defecto: Valor a retornar si la conversión falla.

    Returns:
        El valor convertido a entero o ``por_defecto``.
    """
    try:
        return int(valor)
    except (TypeError, ValueError):
        return por_defecto


class ControladorPrincipal:
    """Coordina urgencias, consulta externa, historial y la vista.

    Responsabilidades:

    - Registrar pacientes en la estructura correcta según su área.
    - Atender pacientes (urgencias por prioridad, consulta por orden).
    - Guardar el historial de atendidos en una pila y permitir "deshacer".
    """

    def __init__(self, page: ft.Page) -> None:
        """Inicializa el controlador con su vista y sus estructuras.

        Args:
            page: Página de Flet donde se renderizará la interfaz.
        """
        self.vista = VistaPrincipal(page)

        self.urgencias = ColaPrioridad()
        self.consulta = Cola()
        self.historial = Pila()

    # ------------------------------------------------------------------
    # Arranque
    # ------------------------------------------------------------------
    def iniciar(self) -> None:
        """Conecta la vista, dibuja la interfaz y muestra el estado."""
        self.vista.asignar_controlador(self)
        self.vista.construir()
        self.actualizar_vista()

    # ------------------------------------------------------------------
    # Acciones del usuario
    # ------------------------------------------------------------------
    def registrar_paciente(
        self,
        nombre: str,
        edad,
        motivo: str,
        area: str,
        severidad,
    ) -> None:
        """Crea un paciente y lo encola en su área correspondiente.

        Args:
            nombre: Nombre completo del paciente.
            edad: Edad en años.
            motivo: Motivo de consulta o síntoma.
            area: ``"urgencias"`` o ``"consulta"``.
            severidad: Gravedad (1–5), solo usada en urgencias.
        """
        nombre = (nombre or "").strip()
        if not nombre:
            self.vista.mostrar_mensaje("Escribe el nombre del paciente.")
            return

        paciente = Paciente(
            nombre=nombre,
            edad=_a_entero(edad),
            motivo=(motivo or "").strip(),
            area=area,
            severidad=_a_entero(severidad, 1),
        )

        if paciente.es_urgencia:
            self.urgencias.encolar(paciente, paciente.severidad)
        else:
            self.consulta.encolar(paciente)

        self.vista.limpiar_formulario()
        self.vista.mostrar_mensaje(
            f"{paciente.nombre} registrado en {paciente.area} "
            f"({paciente.identificador})."
        )
        self.actualizar_vista()

    def atender_urgencia(self) -> None:
        """Atiende al paciente más grave de urgencias (mayor severidad)."""
        if self.urgencias.esta_vacia():
            self.vista.mostrar_mensaje("No hay pacientes en urgencias.")
            return
        paciente = self.urgencias.desencolar()
        self.historial.apilar(paciente)
        self.vista.mostrar_mensaje(
            f"Atendido en urgencias: {paciente.nombre} "
            f"(severidad {paciente.severidad}/5)."
        )
        self.actualizar_vista()

    def atender_consulta(self) -> None:
        """Atiende al primer paciente de la cola de consulta externa (FIFO)."""
        if self.consulta.esta_vacia():
            self.vista.mostrar_mensaje("No hay pacientes en consulta externa.")
            return
        paciente = self.consulta.desencolar()
        self.historial.apilar(paciente)
        self.vista.mostrar_mensaje(
            f"Atendido en consulta: {paciente.nombre}."
        )
        self.actualizar_vista()

    def deshacer_ultima_atencion(self) -> None:
        """Devuelve al último paciente atendido a su área (LIFO)."""
        if self.historial.esta_vacia():
            self.vista.mostrar_mensaje("No hay atenciones para deshacer.")
            return
        paciente = self.historial.desapilar()
        if paciente.es_urgencia:
            self.urgencias.encolar(paciente, paciente.severidad)
        else:
            self.consulta.encolar(paciente)
        self.vista.mostrar_mensaje(
            f"Deshecha la atención de {paciente.nombre} "
            f"(vuelve a {paciente.area})."
        )
        self.actualizar_vista()

    # ------------------------------------------------------------------
    # Sincronización con la vista
    # ------------------------------------------------------------------
    def actualizar_vista(self) -> None:
        """Refresca la vista con el estado actual de las tres estructuras."""
        self.vista.actualizar_estado(
            urgencias=self.urgencias.a_lista(),
            consulta=self.consulta.a_lista(),
            historial=self.historial.a_lista(),
        )
