class Tarea:
    def __init__(self, id_tarea, descripcion, completada=False, usuario=""):
        self.id = id_tarea
        self.descripcion = descripcion
        self.completada = completada
        self.usuario = usuario

    def to_dict(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "completada": self.completada,
            "usuario": self.usuario
        }

    @staticmethod
    def from_dict(data):
        return Tarea(
            id_tarea=data["id"],
            descripcion=data["descripcion"],
            completada=data["completada"],
            usuario=data.get("usuario", "")
        )