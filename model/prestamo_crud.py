from interface.crud_base import CRUDAbstract
from services.storage import JSONStorage
from models.prestamo import Prestamo


class PrestamoCRUD(CRUDAbstract):
    def __init__(self):
        self.__storage = JSONStorage("data/prestamos.json")

    def all(self):
        return self.__storage.load()

    def create(self, data):
        prestamo = Prestamo(
            data["empleado_id"],
            data["fecha_prestamo"],
            data["monto"],
            data["numero_cuotas"],
        )
        return self.__storage.append(prestamo.to_dict())

    def read(self, id):
        prestamos = self.__storage.load()
        return next((p for p in prestamos if p["id"] == id), None)

    def update(self, id, data):
        return self.__storage.update(id, data)

    def delete(self, id):
        return self.__storage.delete(id)
