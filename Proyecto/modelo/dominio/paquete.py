"""Entidad Paquete del dominio logístico."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from itertools import count


@dataclass
class Paquete:
    """Representa un paquete en tránsito dentro del centro logístico.

    Attributes:
        destino: Ciudad o dirección de destino del paquete.
        peso_kg: Peso del paquete en kilogramos.
        urgente: Indica si el paquete debe despacharse con prioridad.
        identificador: Código único y autoincremental del paquete.
        hora_registro: Hora local en la que se registró el paquete.
    """

    destino: str
    peso_kg: float = 0.0
    urgente: bool = False
    identificador: str = field(init=False, default="")
    hora_registro: str = field(
        init=False, default_factory=lambda: datetime.now().strftime("%H:%M:%S")
    )

    # Contador de clase para identificadores únicos (PKG-001, PKG-002...)
    _contador = count(1)

    def __post_init__(self) -> None:
        """Asigna el identificador único después de inicializar."""
        self.identificador = f"PKG-{next(self._contador):03d}"

    def a_dict(self) -> dict:
        """Convierte el paquete a diccionario (para persistencia JSON).

        Returns:
            Diccionario con los campos del paquete.
        """
        return {
            "identificador": self.identificador,
            "destino": self.destino,
            "peso_kg": self.peso_kg,
            "urgente": self.urgente,
            "hora_registro": self.hora_registro,
        }

    @classmethod
    def desde_dict(cls, datos: dict) -> "Paquete":
        """Reconstruye un paquete desde su representación en diccionario.

        Args:
            datos: Diccionario con los campos del paquete.

        Returns:
            Una nueva instancia de :class:`Paquete`.
        """
        paquete = cls(
            destino=datos["destino"],
            peso_kg=float(datos.get("peso_kg", 0.0)),
            urgente=bool(datos.get("urgente", False)),
        )
        paquete.identificador = datos["identificador"]
        paquete.hora_registro = datos.get("hora_registro", "")
        return paquete

    def __str__(self) -> str:
        """Retorna una representación legible del paquete."""
        tipo = "URGENTE" if self.urgente else "estándar"
        return (
            f"[{self.identificador}] → {self.destino} "
            f"({self.peso_kg} kg, {tipo}) - {self.hora_registro}"
        )
