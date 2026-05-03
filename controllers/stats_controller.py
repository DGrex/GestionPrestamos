from core.colors import Fore, Style

from core import JsonManager, JsonManagerError, ConsoleUtils
from models import Employee, Loan, Pay


class StatsController:
    EMPLOYEES_FILE = "data/Employee.json"
    LOANS_FILE = "data/Loan.json"
    PAYS_FILE = "data/Pay.json"

    def __init__(self):
        self.employees = []
        self.loans = []
        self.pays = []

        try:
            self.employees = JsonManager(StatsController.EMPLOYEES_FILE).load()
        except JsonManagerError as e:
            ConsoleUtils.print_error(str(e))

        try:
            self.loans = JsonManager(StatsController.LOANS_FILE).load()
        except JsonManagerError as e:
            ConsoleUtils.print_error(str(e))

        try:
            self.pays = JsonManager(StatsController.PAYS_FILE).load()
        except JsonManagerError as e:
            ConsoleUtils.print_error(str(e))

    def show(self):
        ConsoleUtils.print_header("=== CONSULTA GENERAL / ESTADÍSTICAS ===")
        for step in (
            self._employee_stats,
            self._loan_stats,
            self._pay_stats,
            self._combined_stats,
        ):
            try:
                step()
            except Exception as e:
                ConsoleUtils.print_error(f"Error en estadísticas: {e}")

    def _safe_employee_records(self):
        valid = []
        for item in self.employees:
            if not isinstance(item, dict):
                continue
            try:
                valid.append(
                    {
                        "nombre": str(item["nombre"]),
                        "sueldo": float(item["sueldo"]),
                    }
                )
            except (KeyError, TypeError, ValueError):
                continue
        return valid

    def _safe_loan_records(self):
        valid = []
        for item in self.loans:
            if not isinstance(item, dict):
                continue
            try:
                valid.append(
                    {
                        "id": int(item["id"]),
                        "empleado_id": int(item["empleado_id"]),
                        "monto": float(item["monto"]),
                        "estado": str(item["estado"]),
                        "saldo": float(item["saldo"]),
                    }
                )
            except (KeyError, TypeError, ValueError):
                continue
        return valid

    def _safe_pay_records(self):
        valid = []
        for item in self.pays:
            if not isinstance(item, dict):
                continue
            try:
                valid.append(
                    {
                        "id": int(item["id"]),
                        "prestamo_id": int(item["prestamo_id"]),
                        "valor_pago": float(item["valor_pago"]),
                    }
                )
            except (KeyError, TypeError, ValueError):
                continue
        return valid

    def _employee_stats(self):
        ConsoleUtils.print_colored("-- Empleados --", Fore.GREEN, Style.BRIGHT)

        employees = self._safe_employee_records()
        if not employees:
            ConsoleUtils.print_error("  Sin empleados registrados o datos inválidos")
            return

        total = len(employees)
        avg_salary = sum(e["sueldo"] for e in employees) / total
        highest_salary_emp = max(employees, key=lambda e: e["sueldo"])
        lowest_salary_emp = min(employees, key=lambda e: e["sueldo"])
        above_avg = [e for e in employees if e["sueldo"] > avg_salary]

        print(f"  Total empleados: {Fore.YELLOW}{total}{Style.RESET_ALL}")
        print(f"  Salario promedio: {Fore.YELLOW}{avg_salary:.2f}{Style.RESET_ALL}")
        print(
            f"  Empleado con mayor salario: {Fore.YELLOW}{highest_salary_emp['nombre']} ({highest_salary_emp['sueldo']:.2f}){Style.RESET_ALL}"
        )
        print(
            f"  Empleado con menor salario: {Fore.YELLOW}{lowest_salary_emp['nombre']} ({lowest_salary_emp['sueldo']:.2f}){Style.RESET_ALL}"
        )
        print(
            f"  Empleados con salario por encima del promedio: {Fore.YELLOW}{len(above_avg)}{Style.RESET_ALL}"
        )

    def _loan_stats(self):
        print(Fore.BLUE + Style.BRIGHT + "\n-- Préstamos --" + Style.RESET_ALL)

        loans = self._safe_loan_records()
        if not loans:
            print("  Sin préstamos registrados o datos inválidos")
            return

        total = len(loans)
        total_amount = sum(l["monto"] for l in loans)
        avg_amount = total_amount / total if total > 0 else 0
        pending = [l for l in loans if l["estado"] == "pendiente"]
        paid = [l for l in loans if l["estado"] == "pagado"]
        highest_loan = max(loans, key=lambda l: l["monto"])
        loans_by_emp = {}
        for l in loans:
            loans_by_emp[l["empleado_id"]] = loans_by_emp.get(l["empleado_id"], 0) + 1

        print(f"  Total préstamos: {Fore.YELLOW}{total}{Style.RESET_ALL}")
        print(
            f"  Monto total prestado: {Fore.YELLOW}{total_amount:.2f}{Style.RESET_ALL}"
        )
        print(
            f"  Monto promedio por préstamo: {Fore.YELLOW}{avg_amount:.2f}{Style.RESET_ALL}"
        )
        print(f"  Préstamos pendientes: {Fore.YELLOW}{len(pending)}{Style.RESET_ALL}")
        print(f"  Préstamos pagados: {Fore.YELLOW}{len(paid)}{Style.RESET_ALL}")
        print(
            f"  Préstamo de mayor monto: {Fore.YELLOW}ID {highest_loan['id']} ({highest_loan['monto']:.2f}){Style.RESET_ALL}"
        )
        print(f"  Préstamos por empleado: {Fore.YELLOW}{loans_by_emp}{Style.RESET_ALL}")

    def _pay_stats(self):
        print(Fore.MAGENTA + Style.BRIGHT + "\n-- Pagos --" + Style.RESET_ALL)

        pays = self._safe_pay_records()
        if not pays:
            print("  Sin pagos registrados o datos inválidos")
            return

        total = len(pays)
        total_paid = sum(p["valor_pago"] for p in pays)
        avg_payment = total_paid / total if total > 0 else 0
        highest_pay = max(pays, key=lambda p: p["valor_pago"])
        pays_by_loan = {}
        for p in pays:
            pays_by_loan[p["prestamo_id"]] = pays_by_loan.get(p["prestamo_id"], 0) + 1

        print(f"  Total pagos: {Fore.YELLOW}{total}{Style.RESET_ALL}")
        print(f"  Monto total pagado: {Fore.YELLOW}{total_paid:.2f}{Style.RESET_ALL}")
        print(f"  Pago promedio: {Fore.YELLOW}{avg_payment:.2f}{Style.RESET_ALL}")
        print(
            f"  Pago de mayor monto: {Fore.YELLOW}ID {highest_pay['id']} ({highest_pay['valor_pago']:.2f}){Style.RESET_ALL}"
        )
        print(f"  Pagos por préstamo: {Fore.YELLOW}{pays_by_loan}{Style.RESET_ALL}")

    def _combined_stats(self):
        print(
            Fore.RED
            + Style.BRIGHT
            + "\n-- Estadísticas Combinadas --"
            + Style.RESET_ALL
        )

        employees = self._safe_employee_records()
        loans = self._safe_loan_records()
        pays = self._safe_pay_records()

        emp_with_loans = set(l["empleado_id"] for l in loans)
        print(
            f"  Empleados con préstamos: {Fore.YELLOW}{len(emp_with_loans)}{Style.RESET_ALL}"
        )

        avg_loans_per_emp = len(loans) / len(employees) if employees else 0
        print(
            f"  Promedio de préstamos por empleado: {Fore.YELLOW}{avg_loans_per_emp:.2f}{Style.RESET_ALL}"
        )

        total_balance = sum(l["saldo"] for l in loans)
        print(
            f"  Saldo total pendiente: {Fore.YELLOW}{total_balance:.2f}{Style.RESET_ALL}"
        )

        loans_with_pays = set(p["prestamo_id"] for p in pays)
        print(
            f"  Préstamos con pagos: {Fore.YELLOW}{len(loans_with_pays)}{Style.RESET_ALL}"
        )

        avg_pays_per_loan = len(pays) / len(loans) if loans else 0
        print(
            f"  Promedio de pagos por préstamo: {Fore.YELLOW}{avg_pays_per_loan:.2f}{Style.RESET_ALL}"
        )
