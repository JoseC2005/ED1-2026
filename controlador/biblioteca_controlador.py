from modelo.lista_canciones import ListaCanciones


class BibliotecaControlador:
    def __init__(self):
        self.biblioteca = ListaCanciones("Biblioteca Principal")
        self.playlists = {}
        self.cargar_ejemplos()

    def cargar_ejemplos(self):
        ejemplos = [
            ("Viva La Vida", "Coldplay", "4:02", "https://www.youtube.com/watch?v=dvgZkm1xWPE"),
            ("Bohemian Rhapsody", "Queen", "5:55", "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"),
            ("Blinding Lights", "The Weeknd", "3:20", "https://www.youtube.com/watch?v=4NRXx6U8ABQ"),
        ]

        for titulo, artista, duracion, enlace in ejemplos:
            self.biblioteca.agregar_cancion(titulo, artista, duracion, enlace)

    def agregar_cancion(self, titulo, artista, duracion, enlace=""):
        self.biblioteca.agregar_cancion(titulo, artista, duracion, enlace)

    def buscar_canciones(self, texto):
        if texto.strip() == "":
            return self.biblioteca.obtener_todas()
        return self.biblioteca.buscar_canciones(texto)

    def eliminar_cancion(self, titulo):
        eliminado = self.biblioteca.eliminar_cancion(titulo)
        if eliminado:
            for playlist in self.playlists.values():
                playlist.eliminar_cancion(titulo)
        return eliminado

    def crear_playlist(self, nombre, titulos):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("La playlist necesita un nombre.")

        playlist = ListaCanciones(nombre)
        for titulo in titulos:
            self._agregar_titulo_a_lista(playlist, titulo)

        self.playlists[nombre] = playlist

    def agregar_a_playlist(self, nombre, titulos):
        playlist = self.playlists.get(nombre)
        if playlist is None:
            return False

        for titulo in titulos:
            self._agregar_titulo_a_lista(playlist, titulo)

        return True

    def obtener_biblioteca(self):
        return self.biblioteca.obtener_todas()

    def obtener_nombres_playlists(self):
        return list(self.playlists.keys())

    def obtener_playlist(self, nombre):
        playlist = self.playlists.get(nombre)
        if playlist is None:
            return []
        return playlist.obtener_todas()

    def _agregar_titulo_a_lista(self, lista, titulo):
        cancion = self.biblioteca.obtener_por_titulo(titulo)
        if cancion is None:
            return

        if lista.obtener_por_titulo(titulo) is not None:
            return

        lista.agregar_cancion(
            cancion["titulo"],
            cancion["artista"],
            cancion["duracion"],
            cancion.get("enlace", ""),
        )
