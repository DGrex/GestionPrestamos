from controllers.employee_controller import EmployeeController
from core.mixins import LogMixin
import sys

class Menu:

    def __init__(self):
        self.employee_controller = EmployeeController()

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
                        sys.exit()
                    elif callable(action):
                        action()
                else:
                    print("\nOpción Incorrecta")
            except ValueError:
                print("\nDebe ingresar un número válido.")
        
    def optionMenu(self):
        self.show_menu(
            "Sistema de Gestión de Préstamos",
            [
                {"label": "Empleados", "action": self.employeeMenu},
                {"label": "Préstamos", "action": lambda: None},
                {"label": "Pagos", "action": lambda: None},
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

def safe_action(action, *args, **kwargs):
    try:
        return action(*args, **kwargs)
    except ValueError as e:
        log_mixin = LogMixin()  
        log_mixin.log_error(e)
        return None



