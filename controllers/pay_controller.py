from core import (
    CrudInterface,
    JsonManager,
    # JsonManagerError,
    LogMixin,
    ValidationMixin,
    ConfirmAction,
    ConsoleUtils,
)
from controllers import EmployeeController, LoanController
from models import Pay, Loan
from datetime import datetime
from colorama import Fore


class PayController(CrudInterface, ValidationMixin, LogMixin, ConfirmAction):
    DATA_FILE = "data/Pay.json"

    def __init__(self):
        self.__storage = JsonManager(PayController.DATA_FILE)

    def all(self):
        return self.__storage.load()

    def create(self):
        employee_controller = EmployeeController()
        loan_controller = LoanController()
        # pago_crud = PagoCRUD()

        identification = input("Ingrese la cédula del empleado: ")

        employee_data = employee_controller.read_by_cedula(identification)
        if not employee_data:
            print("Empleado no encontrado.")
            return

        # Mostrar datos del empleado
        print("\n--- Datos del empleado ---")
        print(f"Nombre: {employee_data['nombre']}")
        print(f"Cédula: {employee_data['cedula']}")
        print(f"Sueldo: {employee_data['sueldo']}")

        # Buscar préstamo pendiente
        loans = loan_controller.all()
        loan_data = next(
            (
                l
                for l in loans
                if l["empleado_id"] == employee_data["id"]
                and l["estado"] == "pendiente"
            ),
            None,
        )
        if not loan_data:
            print("\nEste empleado no tiene préstamos pendientes.")
            return

        # Mostrar datos del préstamo
        print("\n--- Datos del préstamo ---")
        print(f"ID Préstamo: {loan_data['id']}")
        print(f"Fecha: {loan_data['fecha_prestamo']}")
        print(f"Monto: {loan_data['monto']}")
        print(f"Saldo: {loan_data['saldo']}")
        print(f"Cuota: {loan_data['cuota']}")
        # Pedir valor del pago

        value_pay = self.validate_amount(input("Ingrese valor del pago: "), "Pago")
        pay_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Usar el método de la clase Prestamo
        loan = Loan(
            loan_data["empleado_id"],
            loan_data["fecha_prestamo"],
            loan_data["monto"],
            loan_data["numero_cuotas"],
            loan_data["cuota"],
            loan_data["saldo"],
            loan_data["estado"],
        )

        try:
            loan.register_payment(value_pay)
        except ValueError as e:
            self.log_error(f"{e}")
            return

        if not self.confirm_action("Guardar"):
            return self.log_warn("Accion Cancelada")
        # Guardar cambios en préstamo
        loan_controller.update(loan_data["id"], loan.to_dict())
        # Guardar registro del pago
        pay = Pay(loan_data["id"], value_pay, pay_date)

        self.__storage.append(pay.to_dict())

        self.log_success("\nPago registrado correctamente.")
        self.log_info(f"Saldo restante: {loan.to_dict()['saldo']}")
        self.log_info(f"Estado del préstamo: {loan.to_dict()['estado']}")

    def read(self):
        ConsoleUtils.print_header("=== PAGOS ===")
        if not self.all():
            ConsoleUtils.print_error("No hay pagos registrados")
            return
        for pay_data in self.all():
            pay = Pay.from_dict(pay_data)
            ConsoleUtils.print_colored(pay.display_pay, Fore.MAGENTA)

    def update(self, id, data):
        raise NotImplementedError("Los pagos no se pueden actualizar.")

    def delete(self, id):
        raise NotImplementedError("Los pagos no se pueden eliminar.")
