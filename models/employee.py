class Employee():

    def __init__(self, name: str, identification: str, salary: float):

        self.__name = name
        self.__identification = identification
        self.__salary = salary

    # Nombre
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    # Cédula
    @property
    def identification(self):
        return self.__identification

    @identification.setter
    def identification(self, new_identification):
        self.__identification = new_identification

    # Sueldo
    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, new_salary):
        self.__salary = new_salary

    # Método para exportar a dict (para JSON)
    def to_dict(self):
        return {
            "nombre": self.__name,
            "cedula": self.__identification,
            "sueldo": self.__salary,
        }

    # Método estático: factoría que reconstruye un Customer desde un dict (JSON). 
    @staticmethod
    def from_dict(data):
        return Employee(
            name=data["name"],            
            identification=data["identification"],
            salary=data["salary"]
        ) 
