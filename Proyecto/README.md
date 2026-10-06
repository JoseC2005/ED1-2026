# 📦 Simulador de Centro Logístico de Distribución y Rutas de Despacho

**Primer avance** — Proyecto de Estructuras de Datos I (INF-220)

Aplicación multiplataforma construida con **Flet** y arquitectura **MVC** que
simula la operación de un centro logístico de distribución.

## Requisitos

- Python 3.10 o superior
- [Flet](https://flet.dev) 1.0 o superior

```bash
pip install flet
```

## Ejecutar

```bash
python main.py
```

## Estructura del proyecto (MVC)

```
Proyecto/
├── main.py                     # Punto de entrada (Flet)
├── README.md
├── modelo/                     # Lógica de datos (sin UI)
│   ├── __init__.py
│   ├── estructuras/            # Estructuras de datos implementadas manualmente
│   │   ├── __init__.py
│   │   ├── nodo.py             # Nodo base
│   │   ├── pila.py             # Pila (LIFO) — Undo/Redo
│   │   ├── cola.py             # Cola (FIFO) — Despacho
│   │   └── lista_doble.py      # Lista doblemente enlazada — Historial
│   └── dominio/
│       ├── __init__.py
│       └── paquete.py           # Entidad Paquete
├── vista/                      # Interfaz gráfica (Flet)
│   ├── __init__.py
│   └── vista_principal.py
├── controlador/                # Conecta vista y modelo
│   ├── __init__.py
│   └── controlador_principal.py
├── datos/                      # Persistencia (pendiente)
└── tests/                      # Pruebas (pendiente)
```

## Estado del avance

- [x] Estructura MVC
- [x] Pila (LIFO) y Cola (FIFO) con nodos manuales
- [x] Lista doblemente enlazada
- [x] Entidad Paquete
- [x] UI base con Flet
- [ ] Cola de prioridad
- [ ] Lista circular (rutas)
- [ ] Undo/Redo con doble pila
- [ ] Persistencia JSON
- [ ] Rutas y vehículos

## Autor

- **Estudiante:** Jose Carlos Justiniano Montaño
- **Curso:** INF-220 Estructuras de Datos I
