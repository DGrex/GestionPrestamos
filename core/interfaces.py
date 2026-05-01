from abc import ABC, abstractmethod


class CrudInterface(ABC):
    """
    Clase abstracta que define la interfaz CRUD.
    Obliga a implementar los métodos básicos en cualquier clase que herede.
    """

    @abstractmethod
    def create(self, data):
        """Crear un nuevo registro"""
        pass

    @abstractmethod
    def read(self, id):
        """Leer un registro por ID"""
        pass

    @abstractmethod
    def update(self, id, data):
        """Actualizar un registro existente"""
        pass

    @abstractmethod
    def delete(self, id):
        """Eliminar un registro por ID"""
        pass
