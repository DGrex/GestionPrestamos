class Empleado:

    def __init__(self, nombre, cedula, sueldo):
        self.__nombre = nombre
        self.__cedula = cedula
        self.__sueldo = sueldo

    # Encapsulamiento con getters/setters
    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_cedula(self):
        return self.__cedula

    def get_sueldo(self):
        return self.__sueldo

    def set_sueldo(self, nuevo_sueldo):
        if nuevo_sueldo > 0:
            self.__sueldo = nuevo_sueldo

    # Método para exportar a dict (para JSON)
    def to_dict(self):
        return {
            "nombre": self.__nombre,
            "cedula": self.__cedula,
            "sueldo": self.__sueldo
        }
