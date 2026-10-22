"""Entidad Paciente del dominio hospitalario."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from itertools import count


@dataclass
class Paciente:
    """Representa un paciente registrado en el hospital.

    Attributes:
        nombre: Nombre completo del paciente.
        edad: Edad del paciente en años.
        motivo: Motivo de consulta o síntoma principal.
        area: Área de atención (``"urgencias"`` o ``"consulta"``).
        severidad: Gravedad de 1 a 5 (5 = crítico). Solo se usa en urgencias.
        identificador: Código único autoincremental (PAC-001...).
        hora_llegada: Hora local en la que se registró al paciente.
    """

    nombre: str
    edad: int = 0
    motivo: str = ""
    area: str = "consulta"
    severidad: int = 1
    identificador: str = field(init=False, default="")
    hora_llegada: str = field(
        init=False, default_factory=lambda: datetime.now().strftime("%H:%M:%S")
    )

    # Contador de clase para identificadores únicos (PAC-001, PAC-002...).
    _contador = count(1)

    def __post_init__(self) -> None:
        """Asigna el identificador único y normaliza edad y severidad."""
        self.identificador = f"PAC-{next(self._contador):03d}"
        self.edad = max(0, int(self.edad))
        self.severidad = max(1, min(int(self.severidad), 5))

    @property
    def es_urgencia(self) -> bool:
        """Indica si el paciente pertenece al área de urgencias."""
        return self.area == "urgencias"

    def a_dict(self) -> dict:
        """Convierte el paciente a diccionario (para persistencia JSON).

        Returns:
            Diccionario con los campos del paciente.
        """
        return {
            "identificador": self.identificador,
            "nombre": self.nombre,
            "edad": self.edad,
            "motivo": self.motivo,
            "area": self.area,
            "severidad": self.severidad,
            "hora_llegada": self.hora_llegada,
        }

    @classmethod
    def desde_dict(cls, datos: dict) -> "Paciente":
        """Reconstruye un paciente desde su representación en diccionario.

        Args:
            datos: Diccionario con los campos del paciente.

        Returns:
            Una nueva instancia de :class:`Paciente`.
        """
        paciente = cls(
            nombre=datos["nombre"],
            edad=datos.get("edad", 0),
            motivo=datos.get("motivo", ""),
            area=datos.get("area", "consulta"),
            severidad=datos.get("severidad", 1),
        )
        paciente.identificador = datos.get(
            "identificador", paciente.identificador
        )
        paciente.hora_llegada = datos.get("hora_llegada", "")
        return paciente

    def __str__(self) -> str:
        """Retorna una representación legible del paciente."""
        if self.es_urgencia:
            return (
                f"{self.nombre} ({self.edad} años) · severidad {self.severidad}/5"
                f" · {self.motivo}"
            )
        return f"{self.nombre} ({self.edad} años) · {self.motivo}"
