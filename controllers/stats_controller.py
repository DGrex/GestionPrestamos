import os
from functools import reduce
from colorama import Fore, Style

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
        self._employee_stats()
        self._loan_stats()
        self._pay_stats()
        self._combined_stats()

    def _employee_stats(self):
        ConsoleUtils.print_colored("-- Empleados --", Fore.GREEN, Style.BRIGHT)

        if not self.employees:
            ConsoleUtils.print_error("  Sin empleados registrados")
            return

        total = len(self.employees)

        # Average salary
        avg_salary = (
            reduce(lambda acc, e: acc + e["sueldo"], self.employees, 0) / total
            if total > 0
            else 0
        )

        # Highest salary employee
        highest_salary_emp = reduce(
            lambda a, b: a if a["sueldo"] >= b["sueldo"] else b, self.employees
        )

        # Lowest salary employee
        lowest_salary_emp = reduce(
            lambda a, b: a if a["sueldo"] <= b["sueldo"] else b, self.employees
        )

        # Employees with salary above average
        above_avg = list(filter(lambda e: e["sueldo"] > avg_salary, self.employees))

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

        if not self.loans:
            print("  Sin préstamos registrados")
            return

        total = len(self.loans)

        # Total amount loaned
        total_amount = reduce(lambda acc, l: acc + l["monto"], self.loans, 0)

        # Average loan amount
        avg_amount = total_amount / total if total > 0 else 0

        # Pending loans
        pending = list(filter(lambda l: l["estado"] == "pendiente", self.loans))

        # Paid loans
        paid = list(filter(lambda l: l["estado"] == "pagado", self.loans))

        # Highest loan
        highest_loan = reduce(
            lambda a, b: a if a["monto"] >= b["monto"] else b, self.loans
        )

        # Loans by employee
        loans_by_emp = {}
        for l in self.loans:
            emp_id = l["empleado_id"]
            loans_by_emp[emp_id] = loans_by_emp.get(emp_id, 0) + 1

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

        if not self.pays:
            print("  Sin pagos registrados")
            return

        total = len(self.pays)

        # Total amount paid
        total_paid = reduce(lambda acc, p: acc + p["valor_pago"], self.pays, 0)

        # Average payment
        avg_payment = total_paid / total if total > 0 else 0

        # Highest payment
        highest_pay = reduce(
            lambda a, b: a if a["valor_pago"] >= b["valor_pago"] else b, self.pays
        )

        # Payments by loan
        pays_by_loan = {}
        for p in self.pays:
            loan_id = p["prestamo_id"]
            pays_by_loan[loan_id] = pays_by_loan.get(loan_id, 0) + 1

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

        # Total employees with loans
        emp_with_loans = set(l["empleado_id"] for l in self.loans)
        print(
            f"  Empleados con préstamos: {Fore.YELLOW}{len(emp_with_loans)}{Style.RESET_ALL}"
        )

        # Average loans per employee
        avg_loans_per_emp = (
            len(self.loans) / len(self.employees) if self.employees else 0
        )
        print(
            f"  Promedio de préstamos por empleado: {Fore.YELLOW}{avg_loans_per_emp:.2f}{Style.RESET_ALL}"
        )

        # Total balance remaining
        total_balance = reduce(lambda acc, l: acc + l["saldo"], self.loans, 0)
        print(
            f"  Saldo total pendiente: {Fore.YELLOW}{total_balance:.2f}{Style.RESET_ALL}"
        )

        # Loans with payments
        loans_with_pays = set(p["prestamo_id"] for p in self.pays)
        print(
            f"  Préstamos con pagos: {Fore.YELLOW}{len(loans_with_pays)}{Style.RESET_ALL}"
        )

        # Average payments per loan
        avg_pays_per_loan = len(self.pays) / len(self.loans) if self.loans else 0
        print(
            f"  Promedio de pagos por préstamo: {Fore.YELLOW}{avg_pays_per_loan:.2f}{Style.RESET_ALL}"
        )
