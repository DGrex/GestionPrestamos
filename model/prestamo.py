from mixins.validation_mixin import ValidationMixin


class Prestamo(ValidationMixin):
    def __init__(
        self, empleado_id, fecha_prestamo, monto, numero_cuotas, estado="pendiente"
    ):
        errores = []

        try:
            self.__empleado_id = int(empleado_id)
        except ValueError:
            errores.append("Empleado ID inválido.")

        try:
            self.__monto = self.validar_monto(monto)
        except ValueError as e:
            errores.append(str(e))

        try:
            self.__numero_cuotas = self.validar_numero_cuotas(numero_cuotas)
        except ValueError as e:
            errores.append(str(e))

        if errores:
            raise ValueError("\n".join(errores))

        self.__fecha_prestamo = fecha_prestamo
        self.__cuota = round(self.__monto / self.__numero_cuotas, 2)
        self.__saldo = self.__monto  # regla: saldo inicial = monto
        self.__estado = estado

    # Getters
    def get_empleado_id(self):
        return self.__empleado_id

    def get_monto(self):
        return self.__monto

    def get_numero_cuotas(self):
        return self.__numero_cuotas

    def get_cuota(self):
        return self.__cuota

    def get_saldo(self):
        return self.__saldo

    def get_fecha_prestamo(self):
        return self.__fecha_prestamo

    def get_estado(self):
        return self.__estado

    def set_saldo(self, saldo):
        self.__saldo = saldo

    def set_estado(self, estado):
        if not (estado == "pagado" or estado == "pendiente"):
            raise ValueError("Estado desconocido")
        self.__estado = estado

    # Método registrar pago
    def registrar_pago(self, valor_pago):
        valor_pago= self.validar_monto(valor_pago, "Pago")
        
        if valor_pago <= 0:
            raise ValueError("El pago debe ser mayor a 0.")
        if valor_pago > self.__saldo:
            raise ValueError("El pago no puede ser mayor al saldo pendiente.")
        
        self.__saldo -= valor_pago

        if self.__saldo == 0:
            self.__estado = "pagado"

    def to_dict(self):
        return {
            "empleado_id": self.__empleado_id,
            "fecha_prestamo": self.__fecha_prestamo,
            "monto": self.__monto,
            "numero_cuotas": self.__numero_cuotas,
            "cuota": self.__cuota,
            "saldo": self.__saldo,
            "estado": self.__estado,
        }
