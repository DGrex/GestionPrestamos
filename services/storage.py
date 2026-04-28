import json
import os

class JSONStorage:
    """
    Clase base para manipular archivos JSON con IDs automáticos y únicos.
    """

    def __init__(self, filename):
        self.__filename = filename
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w") as f:
                json.dump([], f)

    def __generate_id(self, data):
        """Generar un ID único basado en los registros existentes"""
        if not data:
            return 1
        # Busca el máximo ID y suma 1
        max_id = max(item["id"] for item in data)
        return max_id + 1

    def load(self):
        """Cargar datos desde el archivo JSON"""
        with open(self.__filename, "r") as f:
            return json.load(f)

    def save(self, data):
        """Guardar datos en el archivo JSON"""
        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)

    def append(self, record):
        """Agregar un nuevo registro con ID automático"""
        data = self.load()
        record["id"] = self.__generate_id(data)
        data.append(record)
        self.save(data)
        return record["id"]

    def update(self, id, new_record):
        """Actualizar un registro existente por ID"""
        data = self.load()
        for item in data:
            if item["id"] == id:
                item.update(new_record)
                self.save(data)
                return True
        return False

    def delete(self, id):
        """Eliminar un registro por ID"""
        data = self.load()
        new_data = [item for item in data if item["id"] != id]
        if len(new_data) != len(data):
            self.save(new_data)
            return True
        return False

    def clear(self):
        """Vaciar el archivo JSON"""
        self.save([])
