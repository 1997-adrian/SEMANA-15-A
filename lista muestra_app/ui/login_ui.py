import tkinter as tk
from tkinter import messagebox
from servicios.gestor_json import GestorJSON

class LoginUI:
    def __init__(self, root, callback_exito):
        self.root = root
        self.callback_exito = callback_exito
        self.db = GestorJSON()
        
        self.root.title("Iniciar Sesión - To-Do App")
        self.root.geometry("300x250")
        self.root.resizable(False, False)
        
        # Estilos
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True)
        
        tk.Label(self.frame, text="Bienvenido", font=("Arial", 16, "bold")).pack(pady=10)
        
        tk.Label(self.frame, text="Usuario:").pack(anchor="w")
        self.entry_user = tk.Entry(self.frame)
        self.entry_user.pack(fill="x", pady=5)
        self.entry_user.insert(0, "admin") # Default para pruebas
        
        tk.Label(self.frame, text="Contraseña:").pack(anchor="w")
        self.entry_pass = tk.Entry(self.frame, show="*")
        self.entry_pass.pack(fill="x", pady=5)
        self.entry_pass.insert(0, "1234") # Default para pruebas
        
        self.btn_login = tk.Button(self.frame, text="Ingresar", command=self.validar, bg="#007ACC", fg="white")
        self.btn_login.pack(fill="x", pady=20)
        
        # Bind Enter en login
        self.root.bind("<Return>", lambda e: self.validar())

    def validar(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        if self.db.validar_usuario(user, pwd):
            self.callback_exito(user)
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.\n(Prueba: admin / 1234)")