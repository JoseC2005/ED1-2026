"""
Vista (interfaz grafica) para gestionar una ListaSimple con Tkinter.

"""

import tkinter as tk
from tkinter import ttk, messagebox


class VistaPrincipal(tk.Tk):
    """Ventana principal para interactuar con la ListaSimple."""

    def __init__(self):
        super().__init__()
        self.title("Lista Enlazada Simple")
        self.geometry("520x520")
        self.resizable(False, False)

        self._controlador = None
        self._construir_widgets()

    def asignar_controlador(self, controlador):
        """Conecta esta vista con su controlador."""
        self._controlador = controlador

    def _construir_widgets(self):
        contenedor = ttk.Frame(self, padding=15)
        contenedor.pack(fill="both", expand=True)

        # --- Entrada de valor ---
        marco_entrada = ttk.Frame(contenedor)
        marco_entrada.pack(fill="x", pady=(0, 10))

        ttk.Label(marco_entrada, text="Valor:").pack(side="left")
        self.entrada_valor = ttk.Entry(marco_entrada)
        self.entrada_valor.pack(side="left", fill="x", expand=True, padx=5)
        self.entrada_valor.bind(
            "<Return>", lambda evento: self._on_insertar_final())

        # --- Botones de accion ---
        marco_botones = ttk.Frame(contenedor)
        marco_botones.pack(fill="x", pady=(0, 10))

        ttk.Button(
            marco_botones, text="Insertar al inicio",
            command=self._on_insertar_inicio
        ).pack(side="left", expand=True, fill="x", padx=2)

        ttk.Button(
            marco_botones, text="Insertar al final",
            command=self._on_insertar_final
        ).pack(side="left", expand=True, fill="x", padx=2)

        marco_botones2 = ttk.Frame(contenedor)
        marco_botones2.pack(fill="x", pady=(0, 10))

        ttk.Button(
            marco_botones2, text="Buscar",
            command=self._on_buscar
        ).pack(side="left", expand=True, fill="x", padx=2)

        ttk.Button(
            marco_botones2, text="Eliminar",
            command=self._on_eliminar
        ).pack(side="left", expand=True, fill="x", padx=2)

        marco_botones3 = ttk.Frame(contenedor)
        marco_botones3.pack(fill="x", pady=(0, 10))

        ttk.Button(
            marco_botones3, text="Eliminar (Fisicamente)",
            command=self._on_eliminar_fisicamente
        ).pack(side="left", expand=True, fill="x", padx=2)

        # --- Visualizacion de la lista (como un tren) ---
        marco_lista = ttk.LabelFrame(
            contenedor, text="Lista enlazada", padding=10)
        marco_lista.pack(fill="both", expand=True, pady=(0, 10))

        # Lienzo donde se dibujan los vagones conectados en horizontal.
        self.lienzo = tk.Canvas(marco_lista, height=200, bg="white")
        self.lienzo.pack(fill="both", expand=True)

        self._PALETA = [
            "#e74c3c",  # rojo
            "#e67e22",  # naranja
            "#f1c40f",  # amarillo
            "#2ecc71",  # verde
            "#3498db",  # azul
            "#9b59b6",  # morado
            "#1abc9c",  # turquesa
            "#e84393",  # rosa
        ]

        # --- Mensajes de estado ---
        self.etiqueta_estado = ttk.Label(
            contenedor, foreground="#2b6cb0")
        self.etiqueta_estado.pack(fill="x")

    # --- Manejadores de eventos: delegan al controlador ---

    def _on_insertar_inicio(self):
        if self._controlador:
            self._controlador.insertar_al_inicio(self.entrada_valor.get())

    def _on_insertar_final(self):
        if self._controlador:
            self._controlador.insertar_al_final(self.entrada_valor.get())

    def _on_buscar(self):
        if self._controlador:
            self._controlador.buscar(self.entrada_valor.get())

    def _on_eliminar(self):
        if self._controlador:
            self._controlador.eliminar(self.entrada_valor.get())

    def _on_eliminar_fisicamente(self):
        if self._controlador:
            self._controlador.eliminar_fisicamente()

    # --- Metodos que el controlador usa para actualizar la vista ---

    def limpiar_entrada(self):
        self.entrada_valor.delete(0, tk.END)

    def mostrar_mensaje_info(self, mensaje):
        self.etiqueta_estado.config(text=mensaje, foreground="#2b6cb0")

    def mostrar_mensaje_error(self, mensaje):
        self.etiqueta_estado.config(text=mensaje, foreground="#c53030")

    def mostrar_dialogo_info(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)

    def actualizar_lista(self, valores, nodo_apartado=None):
        """
        Cada nodo se muestra como un bloque,
        conectados por flechas. La lista refleja SIEMPRE su estado real:
        al eliminar un nodo, los bloques se acomodan y el eliminado se
        dibuja aparte

        Args:
            valores: iterable con los valores en orden (cabeza a cola).
            nodo_apartado: valor del nodo desenlazado que aun existe en
                memoria, o None si no hay ninguno.
        """
        self.lienzo.delete("all")

        d = 46  # tamano del bloque (lado)
        x = 20
        y = 25

        n = len(valores)
        if n == 0 and nodo_apartado is None:
            self.lienzo.create_text(
                250, 30, anchor="n",
                font=("Segoe UI", 11, "italic"), fill="#999999")
            return

        # Tren principal (nodos reales de la lista).
        for i, valor in enumerate(valores):
            color = self._PALETA[i % len(self._PALETA)]
            self._dibujar_bloque(x, y, d, str(valor), color, "black")
            if i < len(valores) - 1:
                # Flecha hacia el siguiente nodo (conexion por el centro).
                self.lienzo.create_line(x + d, y + d // 2,
                                        x + d + 22, y + d // 2,
                                        arrow=tk.LAST, width=2,
                                        fill="black")
            x += d + 22

        # Nodo desenlazado que aun existe en memoria: se dibuja aparte,
        # debajo, en gris, sin conexiones.
        if nodo_apartado is not None:
            ay = y + d + 50  # debajo de la fila del tren
            # Rotulo que explica que aun esta en memoria.
            self.lienzo.create_text(
                20, ay, anchor="w",
                text="Nodo eliminado de la lista (aun en memoria):",
                font=("Segoe UI", 9, "italic"), fill="#555555")
            # Bloque gris con el valor, sin flecha de conexion.
            self._dibujar_bloque(20, ay + 18, d, str(nodo_apartado),
                                 "#95a5a6", "#7f8c8d")
            # Pequena leyenda para indicar que enfatiza el "GC".
            self.lienzo.create_text(
                20 + d + 12, ay + 18 + d // 2, anchor="w",
                text="pulsa 'Eliminar (Fisicamente)'\npara liberarlo de memoria",
                font=("Segoe UI", 8), fill="#7f8c8d")


    def _dibujar_bloque(self, x, y, d, texto, relleno, borde):
        """Dibuja un bloque con su valor dentro.

        Args:
            x, y: esquina superior izquierda del bloque.
            d: tamano del lado del bloque (cuadrado).
            texto: valor a mostrar dentro del bloque.
            relleno: color de fondo del bloque.
            borde: color del borde del bloque.
        """
        self.lienzo.create_rectangle(
            x, y, x + d, y + d,
            fill=relleno, outline=borde, width=2)
        self.lienzo.create_text(
            x + d // 2, y + d // 2, text=texto,
            font=("Segoe UI", 12, "bold"), fill="white")
