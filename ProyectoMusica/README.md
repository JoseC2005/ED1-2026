# 🎵 Reproductor de Música

**Proyecto hermano del Centro Logístico** — mismo estilo MVC y Flet, pero más
sencillo y con temática musical.

## Requisitos

- Python 3.10 o superior
- [Flet](https://flet.dev) 1.0 o superior (`pip install flet`)

## Ejecutar

```bash
python main.py
```

## Qué hace

- **Agregar a la cola**: registra canciones (título, artista, duración,
  favorita) en una **cola FIFO** — la que llegó primero suena primero.
- **Reproducir siguiente**: desencola la primera canción y la muestra en la
  barra «Sonando». La que venía sonando pasa a la **pila** de historial
  (lo último reproducido queda arriba de todo).
- Las **favoritas** se marcan con ★ dorada en las listas.

## Estructura (MVC)

```
ProyectoMusica/
├── main.py                     # Punto de entrada (Flet)
├── modelo/                     # Lógica de datos (sin UI)
│   ├── estructuras/
│   │   ├── nodo.py             # Nodo simple (dato + siguiente)
│   │   ├── cola.py             # Cola (FIFO) — cola de reproducción
│   │   └── pila.py             # Pila (LIFO) — historial
│   └── dominio/
│       └── cancion.py          # Entidad Canción
├── vista/                      # Interfaz gráfica (Flet, tema oscuro)
│   └── vista_principal.py
└── controlador/                # Conecta vista y modelo
    └── controlador_principal.py
```

## Diferencias con el proyecto del centro logístico

| Centro Logístico | Reproductor (este) |
|---|---|
| Entidad `Paquete` | Entidad `Cancion` |
| Cola de despacho (FIFO) | Cola de reproducción (FIFO) |
| Lista doble para historial | **Pila** para historial (¡ahora sí se usa!) |
| Nodo con `anterior` y `siguiente` | Nodo simple con `solo siguiente` |
| Validación de destino + peso | Solo título obligatorio |

## Estado

- [x] Estructura MVC
- [x] Cola (FIFO) con nodos manuales
- [x] Pila (LIFO) con nodos manuales
- [x] Entidad Canción
- [x] UI oscura con Flet
- [ ] Persistencia JSON (`a_dict`/`desde_dict` ya listos)
- [ ] Lista circular (modo repetir)
- [ ] Pruebas unitarias
