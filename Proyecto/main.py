"""Punto de entrada del Simulador de Centro Logístico (arquitectura MVC).

Ejecutar con:
    python main.py
"""

import flet as ft

from controlador.controlador_principal import ControladorPrincipal


def main(page: ft.Page) -> None:
    """Configura la página e inicializa el controlador principal."""
    ControladorPrincipal(page).iniciar()


if __name__ == "__main__":
    ft.run(main)
