import json
import os
from modelos.tarea import Tarea

class GestorJSON:
    def __init__(self, archivo="data.json"):
        self.archivo = archivo
        self.datos = self._cargar_datos()
        self._inicializar_si_vacio()

    def _cargar_datos(self):
        if not os.path.exists(self.archivo):
            return {"usuarios": [], "tareas": []}
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"usuarios": [], "tareas": []}

    def _inicializar_si_vacio(self):
        # Usuario por defecto si no existe ninguno
        if not self.datos["usuarios"]:
            self.datos["usuarios"].append({"usuario": "admin", "password": "1234"})
            self._guardar_datos()

    def _guardar_datos(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, indent=4)

    def validar_usuario(self, usuario, password):
        for u in self.datos["usuarios"]:
            if u["usuario"] == usuario and u["password"] == password:
                return True
        return False

    def obtener_tareas(self, usuario):
        # Filtramos tareas solo de este usuario
        return [Tarea.from_dict(t) for t in self.datos["tareas"] if t["usuario"] == usuario]

    def guardar_tarea(self, tarea_obj):
        self.datos["tareas"].append(tarea_obj.to_dict())
        self._guardar_datos()

    def actualizar_tarea(self, tarea_actualizada):
        for i, t in enumerate(self.datos["tareas"]):
            if t["id"] == tarea_actualizada.id:
                self.datos["tareas"][i] = tarea_actualizada.to_dict()
                self._guardar_datos()
                return

    def eliminar_tarea(self, id_tarea):
        self.datos["tareas"] = [t for t in self.datos["tareas"] if t["id"] != id_tarea]
        self._guardar_datos()