from modelos.tarea import Tarea
from servicios.gestor_json import GestorJSON

class TareaServicio:
    def __init__(self, usuario_actual):
        self.usuario = usuario_actual
        self.db = GestorJSON()

    def listar_tareas(self):
        return self.db.obtener_tareas(self.usuario)

    def agregar_tarea(self, descripcion):
        if not descripcion.strip():
            return False
        # Generar ID simple basado en tiempo
        import time
        nueva = Tarea(int(time.time()), descripcion, False, self.usuario)
        self.db.guardar_tarea(nueva)
        return True

    def toggle_completada(self, id_tarea):
        tareas = self.listar_tareas()
        for t in tareas:
            if t.id == id_tarea:
                t.completada = not t.completada
                self.db.actualizar_tarea(t)
                return t.completada
        return False

    def borrar_tarea(self, id_tarea):
        self.db.eliminar_tarea(id_tarea)