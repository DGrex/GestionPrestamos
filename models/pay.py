class Pay:
    def __init__(self, loan_id, payment_value, payment_date):
        self.__loan_id = loan_id
        self.__payment_value = payment_value
        self.__payment_date = payment_date

    # Loan ID
    @property
    def loan_id(self):
        return self.__loan_id

    @loan_id.setter
    def loan_id(self, value):
        self.__loan_id = value

    # Payment value
    @property
    def payment_value(self):
        return self.__payment_value

    @payment_value.setter
    def payment_value(self, value):
        if value <= 0:
            raise ValueError("Error: el valor del pago debe ser mayor a 0.")
        self.__payment_value = value

    # Payment date
    @property
    def payment_date(self):
        return self.__payment_date

    @payment_date.setter
    def payment_date(self, value):
        self.__payment_date = value

    # Diccionario con claves en español
    def to_dict(self):
        return {
            "prestamo_id": self.__loan_id,
            "valor_pago": self.__payment_value,
            "fecha_pago": self.__payment_date,
        }
