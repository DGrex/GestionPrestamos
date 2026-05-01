from interface.crud_base import CRUDAbstract
from services.storage import JSONStorage
from models.employee import Empleado


class EmpleadoCRUD(CRUDAbstract):
    def __init__(self):
        self.__storage = JSONStorage("data/empleados.json")

    def create(self, data):
        empleados = self.__storage.load()
        # Validar unicidad de cédula
        if any(e["cedula"] == data["cedula"] for e in empleados):
            raise ValueError("Ya existe un empleado con esa cédula")

        empleado = Empleado(data["nombre"], data["cedula"], data["sueldo"])
        return self.__storage.append(empleado.to_dict())

    def read(self, id):
        empleados = self.__storage.load()
        return next((e for e in empleados if e["id"] == id), None)

    def read_by_cedula(self, cedula):
        empleados = self.__storage.load()
        return next((e for e in empleados if e["cedula"] == cedula), None)

    def update(self, id, data):
        return self.__storage.update(id, data)

    def delete(self, id):
        return self.__storage.delete(id)
