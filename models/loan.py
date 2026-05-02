class Loan:
    def __init__(self, employee_id:int, loan_date, amount:float, installment_number:int, quota:int, balance:float, status:str ="pendiente", id_loan:int=0):
        self.__id_loan = id_loan
        self.__employee_id = employee_id
        self.__amount = amount
        self.__installment_number = installment_number
        self.__loan_date = loan_date
        self.__quota = quota
        self.__balance = balance
        self.__status = status  # "pendiente" o "pagado"

    # Employee ID
    @property
    def employee_id(self):
        return self.__employee_id

    @employee_id.setter
    def employee_id(self, value):
        self.__employee_id = value

    # Amount
    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        if value <= 0:
            raise ValueError("El monto debe ser positivo.")
        self.__amount = value
        self.__quota = round(self.__amount / self.__installment_number, 2)

    # Installment number
    @property
    def installment_number(self):
        return self.__installment_number

    @installment_number.setter
    def installment_number(self, value):
        if value <= 0:
            raise ValueError("El número de cuotas debe ser mayor a 0.")
        self.__installment_number = value
        self.__quota = round(self.__amount / self.__installment_number, 2)

    # Quota
    @property
    def quota(self):
        return self.__quota

    # Balance
    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("El saldo no puede ser negativo.")
        self.__balance = value

    # Loan date
    @property
    def loan_date(self):
        return self.__loan_date

    @loan_date.setter
    def loan_date(self, value):
        self.__loan_date = value

    # Status
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in ("pagado", "pendiente"):
            raise ValueError("Estado desconocido.")
        self.__status = value
    
    @property
    def display_loan(self):
        return f"ID {self.__id_loan} - ID Empleado: {self.__employee_id} - Monto: {self.__amount} - Por pagar: {self.__balance} - Estado: {self.__status}"

    # Register payment
    def register_payment(self, payment_value):
        if payment_value <= 0:
            raise ValueError("El pago debe ser mayor a 0.")
        if payment_value > self.__balance:
            raise ValueError("El pago no puede ser mayor al saldo pendiente.")

        self.__balance -= payment_value

        if self.__balance == 0:
            self.__status = "pagado"

    def to_dict(self):
        return {
            "empleado_id": self.__employee_id,
            "fecha_prestamo": self.__loan_date,
            "monto": self.__amount,
            "numero_cuotas": self.__installment_number,
            "cuota": self.__quota,
            "saldo": self.__balance,
            "estado": self.__status,
        }
    
    @staticmethod
    def from_dict(data):
        return Loan(               
        id_loan = data["id"],
        employee_id = data["empleado_id"],
        amount = data["monto"],
        installment_number = data["numero_cuotas"],
        loan_date = data["fecha_prestamo"],
        quota = data["cuota"],
        balance = data["saldo"],
        status = data["estado"]  
        ) 
