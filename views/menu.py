from controllers import (
    EmployeeController,
    LoanController,
    PayController,
    StatsController,
)
from core import LogMixin, ConsoleUtils
from colorama import Fore
import sys

log_mixin = LogMixin()


class Menu:

    def __init__(self):
        self.employee_controller = EmployeeController()
        self.loan_controller = LoanController()
        self.pay_controller = PayController()
        self.stats_controller = StatsController()

    def show_menu(self, title, options):
        while True:
            ConsoleUtils.clear_screen()
            ConsoleUtils.gotoxy(1, 1)  # Position at top-left
            ConsoleUtils.print_header("=" * 40)
            ConsoleUtils.print_header(title)
            ConsoleUtils.print_header("=" * 40)
            for i, opt in enumerate(options, start=1):
                ConsoleUtils.print_colored(f"{i}. {opt['label']}", Fore.GREEN)
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
                        input("\nPresione Enter para continuar...")
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
                {"label": "Estadísticas", "action": self.stats_controller.show},
                {"label": "Salir", "action": "exit"},
            ],
        )

    def employeeMenu(self):
        self.show_menu(
            "Menú Empleado",
            [
                {
                    "label": "Listar Empleados",
                    "action": lambda: safe_action(self.employee_controller.read),
                },
                {
                    "label": "Nuevo Empleado",
                    "action": lambda: safe_action(self.employee_controller.create),
                },
                {
                    "label": "Actualizar Empleado",
                    "action": lambda: safe_action(self.employee_controller.update),
                },
                {
                    "label": "Eliminar Empleado",
                    "action": lambda: safe_action(self.employee_controller.delete),
                },
                {"label": "Atrás", "action": "break"},
                {"label": "Salir", "action": "exit"},
            ],
        )

    def loan_menu(self):
        self.show_menu(
            "Menú Préstamo",
            [
                {
                    "label": "Listar Préstamos",
                    "action": lambda: safe_action(self.loan_controller.read),
                },
                {
                    "label": "Nuevo Préstamo",
                    "action": lambda: safe_action(self.loan_controller.create),
                },
                {"label": "Atrás", "action": "break"},
                {"label": "Salir", "action": "exit"},
            ],
        )

    def payment_menu(self):
        self.show_menu(
            "Menú Pago",
            [
                {
                    "label": "Listar Pagos",
                    "action": lambda: safe_action(self.pay_controller.read),
                },
                {
                    "label": "Nuevo Pago",
                    "action": lambda: safe_action(self.pay_controller.create),
                },
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
