# 🏥 Sistema Hospitalario

Sistema de gestión hospitalaria de escritorio con **arquitectura MVC** y
**Flet**, basado en tres estructuras de datos del curso de Estructuras de
Datos I.

## Estructuras de datos usadas

| Estructura | Uso en el hospital | Política |
|---|---|---|
| `ColaPrioridad` | **Urgencias** | Mayor severidad (1–5) se atiende primero |
| `Cola` | **Consulta externa** | FIFO (orden de llegada) |
| `Pila` | **Historial** | LIFO (lo último atendido queda arriba) |

## Requisitos

- Python 3.10 o superior
- [Flet](https://flet.dev) 1.0 o superior

## Ejecutar

```bash
cd ProyectoHospital
python main.py
```

> Si el proyecto tiene su propio entorno virtual:
>
> ```powershell
> .\venv\Scripts\Activate.ps1
> python main.py
> ```

## Qué hace

- **Registrar paciente**: eliges el área (`Urgencias` o `Consulta`) y, en el
  caso de urgencias, la severidad (1–5). El paciente se encola en la
  estructura correcta.
- **Atender urgencia**: desencola y atiende al paciente más grave de la cola
  de prioridad; se apila en el historial.
- **Atender consulta**: desencola y atiende al primer paciente de la cola
  FIFO; se apila en el historial.
- **Deshacer última atención**: desapila al último paciente atendido y lo
  devuelve a su área (demuestra LIFO).

## Estructura (MVC)

```
ProyectoHospital/
├── main.py                          # Punto de entrada (Flet)
├── modelo/                          # Lógica de datos (sin UI)
│   ├── dominio/
│   │   └── paciente.py              # Entidad Paciente
│   └── estructuras/
│       ├── nodo.py                  # Nodo doble (anterior + siguiente)
│       ├── cola.py                  # Cola FIFO (consulta externa)
│       ├── pila.py                  # Pila LIFO (historial)
│       └── cola_prioridad.py        # Cola de prioridad (urgencias)
├── vista/
│   └── vista_principal.py           # Interfaz Flet (1 pantalla)
└── controlador/
    └── controlador_principal.py     # Conecta vista y modelo
```

## Complejidades

| Operación | Método | Complejidad |
|---|---|---|
| Encolar urgencia (por prioridad) | `encolar(dato, prioridad)` | O(n) |
| Atender urgencia | `desencolar()` | O(1) |
| Encolar consulta | `encolar(dato)` | O(1) |
| Atender consulta | `desencolar()` | O(1) |
| Apilar atención | `apilar(dato)` | O(1) |
| Deshacer atención | `desapilar()` | O(1) |

## Estado

- [x] Estructura MVC
- [x] Cola de prioridad (urgencias)
- [x] Cola FIFO (consulta externa)
- [x] Pila LIFO (historial + deshacer)
- [x] Entidad Paciente
- [x] Interfaz Flet
- [ ] Persistencia JSON (`a_dict`/`desde_dict` ya listos)
