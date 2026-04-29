from mixins.validation_mixin import ValidationMixin


class Empleado(ValidationMixin):

    def __init__(self, nombre, cedula, sueldo):
        errores = []

        try:
            self.__nombre = self.validar_nombre(nombre)
        except ValueError as e:
            errores.append(str(e))

        try:
            self.__cedula = self.validar_cedula_ecuatoriana(cedula)
        except ValueError as e:
            errores.append(str(e))

        try:
            self.__sueldo = self.validar_sueldo(sueldo)
        except ValueError as e:
            errores.append(str(e))

        # Si hubo errores, lanzar excepción con todos juntos
        if errores:
            raise ValueError("\n".join(errores))

    # Encapsulamiento con getters/setters
    def get_nombre(self):
        return self.__nombre

    def get_cedula(self):
        return self.__cedula

    def get_sueldo(self):
        return self.__sueldo

    def set_nombre(self, nuevo_nombre):
        self.__nombre = self.validar_nombre(nuevo_nombre)

    def set_cedula(self, nueva_cedula):
        self.__cedula = self.validar_cedula_ecuatoriana(nueva_cedula)

    def set_sueldo(self, nuevo_sueldo):
        self.__sueldo = self.validar_sueldo(nuevo_sueldo)

    # Método para exportar a dict (para JSON)
    def to_dict(self):
        return {
            "nombre": self.__nombre,
            "cedula": self.__cedula,
            "sueldo": self.__sueldo,
        }
