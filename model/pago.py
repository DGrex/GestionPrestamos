from datetime import datetime
from mixins.validation_mixin import ValidationMixin

class Pago(ValidationMixin):
    def __init__(self, prestamo_id, valor_pago):
        errores = []

        try:
            self.__valor_pago = self.validar_monto(valor_pago, "Valor del pago")
        except ValueError as e:
            errores.append(str(e))

        self.__prestamo_id = prestamo_id
        self.__fecha_pago = datetime.now().strftime("%Y-%m-%d")

        if errores:
            raise ValueError("\n".join(errores))

    def to_dict(self):
        return {
            "prestamo_id": self.__prestamo_id,
            "fecha_pago": self.__fecha_pago,
            "valor_pago": self.__valor_pago
        }
