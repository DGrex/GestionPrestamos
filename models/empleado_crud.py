from interface.crud_base import CRUDAbstract
from services.storage import JSONStorage
from models.empleado import Empleado


class EmpleadoCRUD(CRUDAbstract):
    def __init__(self):
        self.__storage = JSONStorage("data/empleados.json")

    def create(self, data):
        empleado = Empleado(data["nombre"], data["cedula"], data["sueldo"])
        return self.__storage.append(empleado.to_dict())

    def read(self, id):
        empleados = self.__storage.load()
        return next((e for e in empleados if e["id"] == id), None)

    def update(self, id, data):
        return self.__storage.update(id, data)

    def delete(self, id):
        return self.__storage.delete(id)
