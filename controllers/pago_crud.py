from interface.crud_base import CRUDAbstract
from services.storage import JSONStorage
from models.pay import Pago

class PagoCRUD(CRUDAbstract):
    def __init__(self):
        self.__storage = JSONStorage("data/pagos.json")

    def create(self, data):
        pago = Pago(data["prestamo_id"], data["valor_pago"])
        return self.__storage.append(pago.to_dict())

    def all(self):
        return self.__storage.load()

    def read(self, id):
        pagos = self.__storage.load()
        return next((p for p in pagos if p["id"] == id), None)

    def update(self, id, data):
        raise NotImplementedError("Los pagos no se pueden actualizar.")

    def delete(self, id):
        raise NotImplementedError("Los pagos no se pueden eliminar.")
