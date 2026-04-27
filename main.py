import ttkbootstrap as ttk

from controlador.biblioteca_controlador import BibliotecaControlador
from vista.app import BibliotecaApp


def main():
    root = ttk.Window(themename="superhero")
    controlador = BibliotecaControlador()
    BibliotecaApp(root, controlador)
    root.mainloop()


if __name__ == "__main__":
    main()
