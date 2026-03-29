import tkinter as tk
from ui.login_ui import LoginUI
from ui.app_tkinter import AppTkinter

def iniciar_app(usuario):
    # Cuando el login es exitoso, se destruye la ventana de login
    # y se crea la ventana principal
    root = tk.Tk()
    app = AppTkinter(root, usuario)
    root.mainloop()

if __name__ == "__main__":
    root_login = tk.Tk()
    # Pasamos la función que se ejecutará al loguearse correctamente
    login = LoginUI(root_login, iniciar_app)
    root_login.mainloop()