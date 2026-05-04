from core.colors import Fore, Style

from core import JsonManager, JsonManagerError, ConsoleUtils
from models import Employee, Loan, Pay


class StatsController:
    EMPLOYEES_FILE = "data/Employee.json"
    LOANS_FILE = "data/Loan.json"
    PAYS_FILE = "data/Pay.json"

    def __init__(self):
        # Inicializa listas vacías; los datos se cargan en show()
        self.employees = []
        self.loans = []
        self.pays = []

    def reload_data(self):
        """Recarga los datos desde los archivos JSON para sincronizar con actualizaciones."""
        try:
            self.employees = JsonManager(StatsController.EMPLOYEES_FILE).load()
        except JsonManagerError as e:
            ConsoleUtils.print_error(str(e))
            self.employees = []

        try:
            self.loans = JsonManager(StatsController.LOANS_FILE).load()
        except JsonManagerError as e:
            ConsoleUtils.print_error(str(e))
            self.loans = []

        try:
            self.pays = JsonManager(StatsController.PAYS_FILE).load()
        except JsonManagerError as e:
            ConsoleUtils.print_error(str(e))
            self.pays = []

    def show(self):
        # Recarga los datos para reflejar cualquier actualización
        self.reload_data()
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
        """Valida y normaliza los registros de empleados antes de calcular las estadísticas."""
        valid = []
        for item in self.employees:
            if not isinstance(item, dict):
                continue
            try:
                nombre = item.get("nombre")
                sueldo = item.get("sueldo")
                if nombre is None or sueldo is None:
                    continue
                valid.append(
                    {
                        "nombre": str(nombre),
                        "sueldo": float(sueldo),
                    }
                )
            except (TypeError, ValueError):
                # Ignora registros con tipos inválidos.
                continue
        return valid

    def _safe_loan_records(self):
        """Valida y normaliza los registros de préstamos antes de calcular las estadísticas."""
        valid = []
        for item in self.loans:
            if not isinstance(item, dict):
                continue
            try:
                id_val = item.get("id")
                empleado_id = item.get("empleado_id")
                monto = item.get("monto")
                estado = item.get("estado")
                saldo = item.get("saldo")
                if (
                    id_val is None
                    or empleado_id is None
                    or monto is None
                    or estado is None
                    or saldo is None
                ):
                    continue
                valid.append(
                    {
                        "id": int(id_val),
                        "empleado_id": int(empleado_id),
                        "monto": float(monto),
                        "estado": str(estado),
                        "saldo": float(saldo),
                    }
                )
            except (TypeError, ValueError):
                # Ignora registros corruptos o con datos inválidos.
                continue
        return valid

    def _safe_pay_records(self):
        """Valida y normaliza los registros de pagos antes de calcular las estadísticas."""
        valid = []
        for item in self.pays:
            if not isinstance(item, dict):
                continue
            try:
                id_val = item.get("id")
                prestamo_id = item.get("prestamo_id")
                valor_pago = item.get("valor_pago")
                if id_val is None or prestamo_id is None or valor_pago is None:
                    continue
                valid.append(
                    {
                        "id": int(id_val),
                        "prestamo_id": int(prestamo_id),
                        "valor_pago": float(valor_pago),
                    }
                )
            except (TypeError, ValueError):
                # Ignora registros inválidos que podrían romper el informe.
                continue
        return valid

    def _employee_stats(self):
        # Imprime el encabezado para la sección de empleados
        ConsoleUtils.print_colored("-- Empleados --", Fore.GREEN, Style.BRIGHT)

        # Obtiene los registros válidos de empleados
        employees = self._safe_employee_records()
        if not employees:
            ConsoleUtils.print_error("  Sin empleados registrados o datos inválidos")
            return

        # Calcula métricas básicas
        total = len(employees)  # Número total de empleados
        avg_salary = sum(e["sueldo"] for e in employees) / total  # Salario promedio
        highest_salary_emp = max(
            employees, key=lambda e: e["sueldo"]
        )  # Empleado con mayor salario
        lowest_salary_emp = min(
            employees, key=lambda e: e["sueldo"]
        )  # Empleado con menor salario
        above_avg = [
            e for e in employees if e["sueldo"] > avg_salary
        ]  # Empleados por encima del promedio

        # Imprime los resultados
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
        # Imprime el encabezado para la sección de préstamos
        print(Fore.BLUE + Style.BRIGHT + "\n-- Préstamos --" + Style.RESET_ALL)

        # Obtiene los registros válidos de préstamos
        loans = self._safe_loan_records()
        if not loans:
            print("  Sin préstamos registrados o datos inválidos")
            return

        # Calcula métricas de préstamos
        total = len(loans)  # Número total de préstamos
        total_amount = sum(l["monto"] for l in loans)  # Monto total prestado
        avg_amount = (
            total_amount / total if total > 0 else 0
        )  # Monto promedio por préstamo
        pending = [
            l for l in loans if l["estado"] == "pendiente"
        ]  # Préstamos pendientes
        paid = [l for l in loans if l["estado"] == "pagado"]  # Préstamos pagados
        highest_loan = max(loans, key=lambda l: l["monto"])  # Préstamo de mayor monto
        loans_by_emp = {}  # Diccionario para contar préstamos por empleado
        for l in loans:
            loans_by_emp[l["empleado_id"]] = loans_by_emp.get(l["empleado_id"], 0) + 1

        # Imprime los resultados
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
        # Imprime el encabezado para la sección de pagos
        print(Fore.MAGENTA + Style.BRIGHT + "\n-- Pagos --" + Style.RESET_ALL)

        # Obtiene los registros válidos de pagos
        pays = self._safe_pay_records()
        if not pays:
            print("  Sin pagos registrados o datos inválidos")
            return

        # Calcula métricas de pagos
        total = len(pays)  # Número total de pagos
        total_paid = sum(p["valor_pago"] for p in pays)  # Monto total pagado
        avg_payment = total_paid / total if total > 0 else 0  # Pago promedio
        highest_pay = max(pays, key=lambda p: p["valor_pago"])  # Pago de mayor monto
        pays_by_loan = {}  # Diccionario para contar pagos por préstamo
        for p in pays:
            pays_by_loan[p["prestamo_id"]] = pays_by_loan.get(p["prestamo_id"], 0) + 1

        # Imprime los resultados
        print(f"  Total pagos: {Fore.YELLOW}{total}{Style.RESET_ALL}")
        print(f"  Monto total pagado: {Fore.YELLOW}{total_paid:.2f}{Style.RESET_ALL}")
        print(f"  Pago promedio: {Fore.YELLOW}{avg_payment:.2f}{Style.RESET_ALL}")
        print(
            f"  Pago de mayor monto: {Fore.YELLOW}ID {highest_pay['id']} ({highest_pay['valor_pago']:.2f}){Style.RESET_ALL}"
        )
        print(f"  Pagos por préstamo: {Fore.YELLOW}{pays_by_loan}{Style.RESET_ALL}")

    def _combined_stats(self):
        # Imprime el encabezado para la sección combinada
        print(
            Fore.RED
            + Style.BRIGHT
            + "\n-- Estadísticas Combinadas --"
            + Style.RESET_ALL
        )

        # Obtiene registros válidos de todas las entidades
        employees = self._safe_employee_records()
        loans = self._safe_loan_records()
        pays = self._safe_pay_records()

        # Calcula métricas combinadas
        emp_with_loans = set(
            l["empleado_id"] for l in loans
        )  # Empleados únicos con préstamos
        avg_loans_per_emp = (
            len(loans) / len(employees) if employees else 0
        )  # Promedio de préstamos por empleado
        total_balance = sum(l["saldo"] for l in loans)  # Saldo total pendiente
        loans_with_pays = set(
            p["prestamo_id"] for p in pays
        )  # Préstamos únicos con pagos
        avg_pays_per_loan = (
            len(pays) / len(loans) if loans else 0
        )  # Promedio de pagos por préstamo

        # Imprime los resultados
        print(
            f"  Empleados con préstamos: {Fore.YELLOW}{len(emp_with_loans)}{Style.RESET_ALL}"
        )
        print(
            f"  Promedio de préstamos por empleado: {Fore.YELLOW}{avg_loans_per_emp:.2f}{Style.RESET_ALL}"
        )
        print(
            f"  Saldo total pendiente: {Fore.YELLOW}{total_balance:.2f}{Style.RESET_ALL}"
        )
        print(
            f"  Préstamos con pagos: {Fore.YELLOW}{len(loans_with_pays)}{Style.RESET_ALL}"
        )
        print(
            f"  Promedio de pagos por préstamo: {Fore.YELLOW}{avg_pays_per_loan:.2f}{Style.RESET_ALL}"
        )
