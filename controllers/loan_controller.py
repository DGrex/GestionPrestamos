from core import (
    CrudInterface,
    JsonManager,
    JsonManagerError,
    LogMixin,
    ValidationMixin,
    ConsoleUtils,
    confirm_action,
)
from core.colors import Fore
from models import Loan
from controllers import EmployeeController
from datetime import datetime


class LoanController(CrudInterface, ValidationMixin, LogMixin):
    DATA_FILE = "data/Loan.json"

    def __init__(self):
        self.__storage = JsonManager(LoanController.DATA_FILE)

    def all(self):
        try:
            return self.__storage.load()
        except JsonManagerError as e:
            ConsoleUtils.print_error(str(e))
            return []

    def create(self):
        employee_controller = EmployeeController()
        # prestamo_crud = PrestamoCRUD()

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

        loans = self.all() or []

        for l in loans:
            if l.get("empleado_id") == id_employee and l.get("estado") != "pagado":
                self.log_info(
                    "\nEste empleado ya tiene un préstamo pendiente. No puede solicitar otro."
                )
                return

        # Pedir datos del préstamo
        loan_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        amount = self.validate_amount(input("Ingrese monto del préstamo: "))
        installment_number = self.validate_number_quotas(
            input("Ingrese número de cuotas: ")
        )
        quota = amount / installment_number
        balance = amount

        # Crear préstamo
        try:
            return self._save_loan(
                id_employee, loan_date, amount, installment_number, quota, balance
            )
        except ValueError as e:
            self.log_error(e)

    @confirm_action("¿Guardar préstamo? (s/n): ")
    def _save_loan(
        self, id_employee, loan_date, amount, installment_number, quota, balance
    ):
        loan = Loan(id_employee, loan_date, amount, installment_number, quota, balance)
        id_prestamo = self.__storage.append(loan.to_dict())
        self.log_success(f"Préstamo creado correctamente con ID: {id_prestamo}")
        return id_prestamo

    def read(self):
        ConsoleUtils.print_header("=== PRÉSTAMOS ===")
        if not self.all():
            ConsoleUtils.print_error("No hay préstamos registrados")
            return
        for loan_data in self.all():
            loan = Loan.from_dict(loan_data)
            ConsoleUtils.print_colored(loan.display_loan, Fore.BLUE)

    def update(self, id, data):
        return self.__storage.update(id, data)

    def delete(self, id):
        return self.__storage.delete(id)
