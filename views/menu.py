from controllers import EmployeeController , LoanController , PayController
from core import LogMixin
import sys

log_mixin = LogMixin()

class Menu:
    
    

    def __init__(self):
        self.employee_controller = EmployeeController()
        self.loan_controller = LoanController()
        self.pay_controller = PayController()

    def show_menu(self, title, options):
        while True:
            print("\n========================================")
            print(title)
            print("========================================")
            for i, opt in enumerate(options, start=1):
                print(f"{i}. {opt['label']}")
            try:
                option = int(input("Ingrese una Opción: "))
                if 1 <= option <= len(options):
                    action = options[option - 1]["action"]
                    if action == "break":
                        break
                    elif action == "exit":
                        log_mixin.log_info("Cerrando el sistema...")
                        sys.exit()
                    elif callable(action):
                        action()
                else:
                    log_mixin.log_error("Opción Incorrecta")
            except ValueError:
                log_mixin.log_error("Debe ingresar un número válido.")
        
    def optionMenu(self):
        self.show_menu(
            "Sistema de Gestión de Préstamos",
            [
                {"label": "Empleados", "action": self.employeeMenu},
                {"label": "Préstamos", "action": self.loan_menu},
                {"label": "Pagos", "action": self.payment_menu},
                {"label": "Consultas", "action": lambda: None},
                {"label": "Estadísticas", "action": lambda: None},
                {"label": "Salir", "action": "exit"},
            ],
        )

    def employeeMenu(self):
        self.show_menu(
            "Menú Empleado",
            [
                {"label": "Nuevo Empleado", "action":  lambda: safe_action(self.employee_controller.create)},
                {"label": "Actualizar Empleado", "action": lambda: safe_action(self.employee_controller.update)},
                {"label": "Eliminar Empleado", "action": lambda: safe_action(self.employee_controller.delete)},
                {"label": "Atrás", "action": "break"},
                {"label": "Salir", "action": "exit"},
            ],
        )

    def loan_menu(self):
        self.show_menu(
            "Menú Préstamo",
            [
                {"label": "Nuevo Préstamo", "action": lambda: safe_action(self.loan_controller.create)},
                {"label": "Atrás", "action": "break"},
                {"label": "Salir", "action": "exit"},
            ],
        )

    def payment_menu(self):
        self.show_menu(
            "Menú Pago",
            [
                {"label": "Nuevo Pago", "action": lambda: safe_action(self.pay_controller.create)},
                {"label": "Atrás", "action": "break"},
                {"label": "Salir", "action": "exit"},
            ],
        )
        
def safe_action(action, *args, **kwargs):
    try:
        return action(*args, **kwargs)
    except ValueError as e:        
        log_mixin.log_error(e)
        return None



