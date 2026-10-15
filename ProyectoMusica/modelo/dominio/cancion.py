"""Entidad Canción del dominio musical."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from itertools import count


@dataclass
class Cancion:
    """Representa una canción en la cola del reproductor.

    Attributes:
        titulo: Nombre de la canción.
        artista: Intérprete de la canción.
        duracion: Duración en formato texto (ej. "3:45").
        favorita: Indica si la canción está marcada como favorita.
        identificador: Código único y autoincremental (CAN-001...).
        hora_registro: Hora local en la que se agregó la canción.
    """

    titulo: str
    artista: str = "Desconocido"
    duracion: str = "?:??"
    favorita: bool = False
    identificador: str = field(init=False, default="")
    hora_registro: str = field(
        init=False, default_factory=lambda: datetime.now().strftime("%H:%M:%S")
    )

    # Contador de clase para identificadores únicos (CAN-001, CAN-002...)
    _contador = count(1)

    def __post_init__(self) -> None:
        """Asigna el identificador único después de inicializar."""
        self.identificador = f"CAN-{next(self._contador):03d}"

    def a_dict(self) -> dict:
        """Convierte la canción a diccionario (para persistencia JSON).

        Returns:
            Diccionario con los campos de la canción.
        """
        return {
            "identificador": self.identificador,
            "titulo": self.titulo,
            "artista": self.artista,
            "duracion": self.duracion,
            "favorita": self.favorita,
            "hora_registro": self.hora_registro,
        }

    @classmethod
    def desde_dict(cls, datos: dict) -> "Cancion":
        """Reconstruye una canción desde su representación en diccionario.

        Args:
            datos: Diccionario con los campos de la canción.

        Returns:
            Una nueva instancia de :class:`Cancion`.
        """
        cancion = cls(
            titulo=datos["titulo"],
            artista=datos.get("artista", "Desconocido"),
            duracion=datos.get("duracion", "?:??"),
            favorita=bool(datos.get("favorita", False)),
        )
        cancion.identificador = datos["identificador"]
        cancion.hora_registro = datos.get("hora_registro", "")
        return cancion

    def __str__(self) -> str:
        """Retorna una representación legible de la canción."""
        estrella = " ★" if self.favorita else ""
        return (
            f"[{self.identificador}] {self.titulo} - {self.artista} "
            f"({self.duracion}){estrella}"
        )