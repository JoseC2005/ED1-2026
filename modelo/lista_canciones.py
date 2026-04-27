from .nodo import NodoCancion


class ListaCanciones:
    def __init__(self, nombre="Biblioteca"):
        self.nombre = nombre
        self.cabeza = None

    def agregar_cancion(self, titulo, artista, duracion, enlace=""):
        cancion = {
            "titulo": titulo.strip(),
            "artista": artista.strip(),
            "duracion": duracion.strip(),
            "enlace": enlace.strip(),
        }
        nuevo_nodo = NodoCancion(cancion)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            return

        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo_nodo

    def buscar_canciones(self, texto):
        texto = texto.strip().lower()
        resultados = []
        actual = self.cabeza

        while actual:
            datos = actual.datos
            if texto in datos["titulo"].lower() or texto in datos["artista"].lower():
                resultados.append(datos)
            actual = actual.siguiente

        return resultados

    def eliminar_cancion(self, titulo):
        titulo = titulo.strip().lower()
        actual = self.cabeza
        anterior = None

        while actual:
            if actual.datos["titulo"].lower() == titulo:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente

        return False

    def obtener_todas(self):
        canciones = []
        actual = self.cabeza

        while actual:
            canciones.append(actual.datos)
            actual = actual.siguiente

        return canciones

    def obtener_por_titulo(self, titulo):
        titulo = titulo.strip().lower()
        actual = self.cabeza

        while actual:
            if actual.datos["titulo"].lower() == titulo:
                return actual.datos
            actual = actual.siguiente

        return None
