from mixins.validation_mixin import ValidationMixin


class Employee(ValidationMixin):

    def __init__(self, name: str, identification: str, salary: float):

        self.__name = name
        self.__identification = identification
        self.__salary = salary

    # Encapsulamiento con getters/setters
    @property
    def get_nombre(self):
        return self.__nombre

    @property
    def get_cedula(self):
        return self.__cedula

    @property
    def get_sueldo(self):
        return self.__sueldo

    def set_nombre(self, new_name):
        self.__nombre = new_name

    def set_cedula(self, new_identification):
        self.__cedula = new_identification

    def set_sueldo(self, nuevo_sueldo):
        self.__sueldo = nuevo_sueldo

    # Método para exportar a dict (para JSON)
    def to_dict(self):
        return {
            "nombre": self.__nombre,
            "cedula": self.__cedula,
            "sueldo": self.__sueldo,
        }

    # Método estático: factoría que reconstruye un Customer desde un dict (JSON). 
    @staticmethod
    def from_dict(data):
        return Employee(
            name=data["name"],            
            identification=data["identification"],
            salary=data["salary"]
        ) 
