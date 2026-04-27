import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, END, LEFT, RIGHT, X, Y


class BibliotecaApp:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Biblioteca Musical Personal")
        self.root.geometry("1366x768")

        self.titulo_var = tk.StringVar()
        self.artista_var = tk.StringVar()
        self.duracion_var = tk.StringVar()
        self.enlace_var = tk.StringVar()
        self.busqueda_var = tk.StringVar()
        self.playlist_var = tk.StringVar()

        self._crear_interfaz()
        self._cargar_biblioteca()

    def _crear_interfaz(self):
        contenedor = ttk.Frame(self.root, padding=16)
        contenedor.pack(fill=BOTH, expand=True)

        panel_izquierdo = ttk.Frame(contenedor)
        panel_izquierdo.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 8))

        panel_derecho = ttk.Frame(contenedor)
        panel_derecho.pack(side=RIGHT, fill=BOTH, expand=True, padx=(8, 0))

        self._crear_formulario(panel_izquierdo)
        self._crear_tabla_biblioteca(panel_izquierdo)
        self._crear_panel_playlist(panel_derecho)

    def _crear_formulario(self, parent):
        card = ttk.Labelframe(parent, text="Gestionar canciones", padding=14)
        card.pack(fill=X, pady=(0, 12))

        ttk.Label(card, text="Titulo").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(card, textvariable=self.titulo_var, width=28).grid(
            row=0, column=1, sticky="ew", padx=8, pady=4
        )

        ttk.Label(card, text="Artista").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(card, textvariable=self.artista_var, width=28).grid(
            row=1, column=1, sticky="ew", padx=8, pady=4
        )

        ttk.Label(card, text="Duracion").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(card, textvariable=self.duracion_var, width=28).grid(
            row=2, column=1, sticky="ew", padx=8, pady=4
        )

        ttk.Label(card, text="Link").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(card, textvariable=self.enlace_var, width=28).grid(
            row=3, column=1, sticky="ew", padx=8, pady=4
        )

        ttk.Button(card, text="Agregar cancion", command=self.agregar_cancion).grid(
            row=4, column=0, pady=(10, 0), sticky="ew"
        )
        ttk.Button(card, text="Eliminar por titulo", command=self.eliminar_cancion, bootstyle="danger").grid(
            row=4, column=1, padx=8, pady=(10, 0), sticky="ew"
        )

        ttk.Separator(card).grid(row=5, column=0, columnspan=2, sticky="ew", pady=12)

        ttk.Label(card, text="Buscar").grid(row=6, column=0, sticky="w", pady=4)
        ttk.Entry(card, textvariable=self.busqueda_var, width=28).grid(
            row=6, column=1, sticky="ew", padx=8, pady=4
        )
        ttk.Button(card, text="Buscar cancion", command=self.buscar_cancion, bootstyle="info").grid(
            row=7, column=0, sticky="ew", pady=(10, 0)
        )
        ttk.Button(card, text="Mostrar todo", command=self._cargar_biblioteca, bootstyle="secondary").grid(
            row=7, column=1, padx=8, pady=(10, 0), sticky="ew"
        )

        card.columnconfigure(1, weight=1)

    def _crear_tabla_biblioteca(self, parent):
        frame = ttk.Labelframe(parent, text="Biblioteca principal", padding=14)
        frame.pack(fill=BOTH, expand=True)

        columnas = ("titulo", "artista", "duracion", "enlace")
        self.tabla_biblioteca = ttk.Treeview(frame, columns=columnas, show="headings", height=14)

        self.tabla_biblioteca.heading("titulo", text="Titulo")
        self.tabla_biblioteca.heading("artista", text="Artista")
        self.tabla_biblioteca.heading("duracion", text="Duracion")
        self.tabla_biblioteca.heading("enlace", text="Link")

        self.tabla_biblioteca.column("titulo", width=220)
        self.tabla_biblioteca.column("artista", width=180)
        self.tabla_biblioteca.column("duracion", width=90, anchor="center")
        self.tabla_biblioteca.column("enlace", width=280)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tabla_biblioteca.yview)
        self.tabla_biblioteca.configure(yscrollcommand=scrollbar.set)

        self.tabla_biblioteca.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

    def _crear_panel_playlist(self, parent):
        card = ttk.Labelframe(parent, text="Playlists", padding=14)
        card.pack(fill=BOTH, expand=True)

        ttk.Label(card, text="Nombre de playlist").pack(anchor="w")
        ttk.Entry(card, textvariable=self.playlist_var).pack(fill=X, pady=(4, 10))

        ttk.Button(
            card,
            text="Crear playlist con canciones seleccionadas",
            command=self.crear_playlist,
            bootstyle="success",
        ).pack(fill=X, pady=(0, 12))

        ttk.Button(
            card,
            text="Agregar seleccionadas a playlist",
            command=self.agregar_a_playlist,
            bootstyle="primary",
        ).pack(fill=X, pady=(0, 12))

        ttk.Label(card, text="Playlists creadas").pack(anchor="w")
        self.lista_playlists = tk.Listbox(card, height=8)
        self.lista_playlists.pack(fill=X, pady=(4, 10))
        self.lista_playlists.bind("<<ListboxSelect>>", self.mostrar_playlist)

        ttk.Label(card, text="Canciones de la playlist").pack(anchor="w")
        columnas = ("titulo", "artista", "duracion")
        self.tabla_playlist = ttk.Treeview(card, columns=columnas, show="headings", height=12)
        self.tabla_playlist.heading("titulo", text="Titulo")
        self.tabla_playlist.heading("artista", text="Artista")
        self.tabla_playlist.heading("duracion", text="Duracion")
        self.tabla_playlist.column("titulo", width=200)
        self.tabla_playlist.column("artista", width=160)
        self.tabla_playlist.column("duracion", width=90, anchor="center")
        self.tabla_playlist.pack(fill=BOTH, expand=True)

    def agregar_cancion(self):
        titulo = self.titulo_var.get().strip()
        artista = self.artista_var.get().strip()
        duracion = self.duracion_var.get().strip()
        enlace = self.enlace_var.get().strip()

        if not titulo or not artista or not duracion:
            messagebox.showwarning("Campos incompletos", "Completa titulo, artista y duracion.")
            return

        self.controlador.agregar_cancion(titulo, artista, duracion, enlace)
        self._limpiar_formulario()
        self._cargar_biblioteca()

    def buscar_cancion(self):
        resultados = self.controlador.buscar_canciones(self.busqueda_var.get())
        self._llenar_tabla(self.tabla_biblioteca, resultados, incluir_enlace=True)

    def eliminar_cancion(self):
        titulo = self.titulo_var.get().strip()
        if not titulo:
            messagebox.showwarning("Dato faltante", "Escribe el titulo de la cancion a eliminar.")
            return

        eliminado = self.controlador.eliminar_cancion(titulo)
        if eliminado:
            self._limpiar_formulario()
            self._cargar_biblioteca()
            self._actualizar_playlists()
        else:
            messagebox.showinfo("No encontrada", "No existe una cancion con ese titulo.")

    def crear_playlist(self):
        seleccion = self.tabla_biblioteca.selection()
        nombre = self.playlist_var.get().strip()

        if not nombre:
            messagebox.showwarning("Dato faltante", "Escribe un nombre para la playlist.")
            return

        if not seleccion:
            messagebox.showwarning("Sin seleccion", "Selecciona una o varias canciones de la biblioteca.")
            return

        titulos = [self.tabla_biblioteca.item(item_id, "values")[0] for item_id in seleccion]

        self.controlador.crear_playlist(nombre, titulos)
        self.playlist_var.set("")
        self._actualizar_playlists()
        self._seleccionar_playlist(nombre)
        self.mostrar_playlist()

    def agregar_a_playlist(self):
        seleccion_playlist = self.lista_playlists.curselection()
        seleccion_canciones = self.tabla_biblioteca.selection()

        if not seleccion_playlist:
            messagebox.showwarning("Dato faltante", "Selecciona una playlist.")
            return

        if not seleccion_canciones:
            messagebox.showwarning("Sin seleccion", "Selecciona una o varias canciones.")
            return

        nombre = self.lista_playlists.get(seleccion_playlist[0])
        titulos = [self.tabla_biblioteca.item(item_id, "values")[0] for item_id in seleccion_canciones]

        agregado = self.controlador.agregar_a_playlist(nombre, titulos)
        if not agregado:
            messagebox.showinfo("Error", "No se pudo agregar a la playlist.")
            return

        self._seleccionar_playlist(nombre)
        self.mostrar_playlist()

    def mostrar_playlist(self, _event=None):
        seleccion = self.lista_playlists.curselection()
        if not seleccion:
            return

        nombre = self.lista_playlists.get(seleccion[0])
        canciones = self.controlador.obtener_playlist(nombre)
        self._llenar_tabla(self.tabla_playlist, canciones, incluir_enlace=False)

    def _cargar_biblioteca(self):
        canciones = self.controlador.obtener_biblioteca()
        self._llenar_tabla(self.tabla_biblioteca, canciones, incluir_enlace=True)
        self._actualizar_playlists()

    def _actualizar_playlists(self):
        nuevos = self.controlador.obtener_nombres_playlists()
        self.lista_playlists.delete(0, END)
        for nombre in nuevos:
            self.lista_playlists.insert(END, nombre)

    def _llenar_tabla(self, tabla, canciones, incluir_enlace):
        for item in tabla.get_children():
            tabla.delete(item)

        for cancion in canciones:
            valores = [
                cancion["titulo"],
                cancion["artista"],
                cancion["duracion"],
            ]
            if incluir_enlace:
                valores.append(cancion.get("enlace", ""))
            tabla.insert("", END, values=valores)

    def _limpiar_formulario(self):
        self.titulo_var.set("")
        self.artista_var.set("")
        self.duracion_var.set("")
        self.enlace_var.set("")

    def _seleccionar_playlist(self, nombre):
        nombres = self.lista_playlists.get(0, END)
        for i, actual in enumerate(nombres):
            if actual == nombre:
                self.lista_playlists.selection_clear(0, END)
                self.lista_playlists.selection_set(i)
                break
