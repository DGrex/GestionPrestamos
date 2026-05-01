from core import (
    CrudInterface,
    JsonManager,
    # JsonManagerError,
    LogMixin,
    ValidationMixin,
    ConfirmAction,
)
from models import Loan
from controllers import EmployeeController
from datetime import datetime

class LoanController( CrudInterface, ValidationMixin, LogMixin, ConfirmAction):
    DATA_FILE = "data/Loan.json"
    def __init__(self):
        self.__storage = JsonManager(LoanController.DATA_FILE)

    def all(self):
        return self.__storage.load()

    def create(self):
        employee_controller = EmployeeController()
        #prestamo_crud = PrestamoCRUD()

        identification = input("\nIngrese cedula del empleado: ")
        employee_data = employee_controller.read_by_cedula(identification)    
        if not employee_data:
            self.log_warn("Empleado no encontrado.")
            return
        
        id_employee = employee_data["id"]

        # Mostrar datos del empleado
        print("\n--- Datos del empleado ---")
        print(f"Nombre: {employee_data['nombre']}")
        print(f"Cédula: {employee_data['cedula']}")
        print(f"Sueldo: {employee_data['sueldo']}")

        loans = self.__storage.load() or []

        for l in loans:
            if l.get("empleado_id") == id_employee and l.get("estado") != "pagado":
                self.log_info("\nEste empleado ya tiene un préstamo pendiente. No puede solicitar otro.")
                return

        # Pedir datos del préstamo
        loan_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        amount = self.validate_amount(input("Ingrese monto del préstamo: "))
        installment_number = self.validate_number_quotas(input("Ingrese número de cuotas: ")) 
        quota = amount/installment_number
        balance = amount
        
        # Crear préstamo
        try:
            if self.confirm_action("Guardar"):
                loan = Loan(id_employee,loan_date,amount,installment_number,quota,balance)
                id_prestamo = self.__storage.append(loan.to_dict())
                self.log_success(f"Préstamo creado correctamente con ID: {id_prestamo}")
        except ValueError as e:            
            self.log_error(e)    

    def read(self, id):
        prestamos = self.__storage.load()
        return next((p for p in prestamos if p["id"] == id), None)

    def update(self, id, data):
        return self.__storage.update(id, data)

    def delete(self, id):
        return self.__storage.delete(id)
