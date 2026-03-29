import tkinter as tk
from tkinter import ttk, messagebox
from servicios.tarea_servicio import TareaServicio

class AppTkinter:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.servicio = TareaServicio(usuario)
        
        self.root.title(f"Lista de Tareas - {usuario}")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        self._configurar_estilos()
        self._crear_widgets()
        self._cargar_tareas()
        
        # Bindings de Eventos
        self.entry_tarea.bind("<Return>", self._on_enter_presionado)
        self.tree.bind("<Double-1>", self._on_doble_clic)

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        # Configurar tag para tareas completadas
        self.tree = None # Se define en widgets

    def _crear_widgets(self):
        # Frame Superior (Input)
        frame_top = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        frame_top.pack(fill="x", padx=20)
        
        tk.Label(frame_top, text="Nueva Tarea:", bg="#f0f0f0", font=("Arial", 10)).pack(side="left")
        self.entry_tarea = tk.Entry(frame_top, font=("Arial", 10))
        self.entry_tarea.pack(side="left", fill="x", expand=True, padx=10)
        
        btn_add = tk.Button(frame_top, text="Añadir", command=self._agregar_tarea, bg="#28a745", fg="white")
        btn_add.pack(side="left")
        
        # Frame Central (Lista)
        frame_mid = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        frame_mid.pack(fill="both", expand=True, padx=20)
        
        columns = ("id", "descripcion", "estado")
        self.tree = ttk.Treeview(frame_mid, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("estado", text="Estado")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("descripcion", width=400)
        self.tree.column("estado", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_mid, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar colores visuales
        self.tree.tag_configure("completada", foreground="gray", font=("Arial", 10, "overstrike"))
        self.tree.tag_configure("pendiente", foreground="black", font=("Arial", 10))

        # Frame Inferior (Acciones)
        frame_bot = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        frame_bot.pack(fill="x", padx=20)
        
        btn_done = tk.Button(frame_bot, text="Marcar/Desmarcar", command=self._toggle_estado)
        btn_done.pack(side="left", padx=5)
        
        btn_del = tk.Button(frame_bot, text="Eliminar", command=self._eliminar_tarea, bg="#dc3545", fg="white")
        btn_del.pack(side="left", padx=5)

    def _cargar_tareas(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        tareas = self.servicio.listar_tareas()
        for t in tareas:
            estado_txt = "[Hecho]" if t.completada else "[Pendiente]"
            tag = "completada" if t.completada else "pendiente"
            self.tree.insert("", "end", iid=t.id, values=(t.id, t.descripcion, estado_txt), tags=(tag,))

    # --- Lógica de Eventos ---

    def _on_enter_presionado(self, event):
        self._agregar_tarea()

    def _on_doble_clic(self, event):
        # Identificar el item seleccionado
        item = self.tree.selection()
        if item:
            self._toggle_estado()

    def _agregar_tarea(self):
        desc = self.entry_tarea.get()
        if self.servicio.agregar_tarea(desc):
            self.entry_tarea.delete(0, tk.END)
            self._cargar_tareas()
        else:
            messagebox.showwarning("Atención", "La descripción no puede estar vacía")

    def _toggle_estado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        id_tarea = int(seleccion[0])
        self.servicio.toggle_completada(id_tarea)
        self._cargar_tareas()

    def _eliminar_tarea(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una tarea para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta tarea?"):
            id_tarea = int(seleccion[0])
            self.servicio.borrar_tarea(id_tarea)
            self._cargar_tareas()