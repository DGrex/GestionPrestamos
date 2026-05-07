import re
from core.colors import Fore


class ValidationMixin:

    @staticmethod
    def validate_identification(cedula: str):
        cedula = cedula.strip()
        """
        Validar cédula ecuatoriana:
        - Debe tener 10 dígitos
        - Los dos primeros dígitos corresponden a la provincia (01-24)
        - El último dígito es un dígito verificador (algoritmo módulo 10)
        """
        if not cedula.isdigit() or len(cedula) != 10:
            raise ValueError(
                "Error: la cédula debe tener exactamente 10 dígitos numéricos."
            )

        provincia = int(cedula[0:2])
        if provincia < 1 or provincia > 24:
            raise ValueError(
                "Error: los dos primeros dígitos no corresponden a una provincia válida."
            )

        # Algoritmo de validación (módulo 10)
        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        suma = 0
        for i in range(9):
            valor = int(cedula[i]) * coeficientes[i]
            if valor >= 10:
                valor -= 9
            suma += valor

        digito_verificador = 10 - (suma % 10)
        if digito_verificador == 10:
            digito_verificador = 0

        if digito_verificador != int(cedula[9]):
            raise ValueError(
                "Error: la cédula no es válida (dígito verificador incorrecto)."
            )

        return cedula

    @staticmethod
    def validate_salary(valor, limite_max=1_000_000):
        if isinstance(valor, str):
            if "," in valor:
                raise ValueError("Error: use '.' como separador decimal, no ','.")
            try:
                valor = float(valor)
            except ValueError:
                raise ValueError("Error: el sueldo debe ser un número válido.")

        if valor <= 0:
            raise ValueError("Error: el sueldo debe ser positivo.")

        if valor > limite_max:
            raise ValueError(f"Error: el sueldo no puede superar {limite_max}.")

        # Aquí redondeamos siempre a dos decimales
        return round(valor, 2)

    @staticmethod
    def validate_name(nombre, max_length=50):
        """
        Validar nombre:
        - Mínimo 3 caracteres
        - Máximo max_length caracteres
        - Solo letras y espacios
        - Sin números ni caracteres especiales
        - Retorna nombre capitalizado
        """
        # Quitar espacios al inicio y final
        nombre = nombre.strip()

        # Validar longitud mínima
        if len(nombre) < 3:
            raise ValueError("Error: el nombre debe tener al menos 3 caracteres.")

        # Validar longitud máxima
        if len(nombre) > max_length:
            raise ValueError(
                f"Error: el nombre no puede superar {max_length} caracteres."
            )

        # Validar solo letras y espacios (regex)
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", nombre):
            raise ValueError("Error: el nombre solo puede contener letras y espacios.")

        # Capitalizar cada palabra
        nombre = " ".join([palabra.capitalize() for palabra in nombre.split()])

        return nombre

    @staticmethod
    def validate_amount(monto, field_name="Monto"):
        try:
            monto = float(monto)
        except ValueError:
            raise ValueError(f"Error: {field_name} debe ser un número válido.")

        if monto <= 0:
            raise ValueError(f"Error: {field_name} debe ser positivo.")

        # Redondear a 2 decimales
        return round(monto, 2)

        # --- Validación de número de cuotas ---

    @staticmethod
    def validate_number_quotas(numero_cuotas, field_name="Número de cuotas"):
        try:
            numero_cuotas = int(numero_cuotas)
        except ValueError:
            raise ValueError(f"Error: {field_name} debe ser un número entero.")

        if numero_cuotas <= 0:
            raise ValueError(f"Error: {field_name} debe ser mayor a 0.")

        return numero_cuotas


# Mixin de registro: imprime mensajes informativos por consola.
class LogMixin:
    # Métodos de logging con distintos prefijos

    def log_info(self, message):
        from .console_utils import ConsoleUtils

        ConsoleUtils.print_info(f"[INFO]: {message}")

    def log_warn(self, message):
        from .console_utils import ConsoleUtils

        ConsoleUtils.print_colored(f"[WARN]: {message}", Fore.YELLOW)

    def log_error(self, message):
        from .console_utils import ConsoleUtils

        ConsoleUtils.print_error(f"[ERROR]: {message}")

    def log_debug(self, message):
        from .console_utils import ConsoleUtils

        ConsoleUtils.print_colored(f"[DEBUG]: {message}", Fore.BLUE)

    def log_success(self, message):
        from .console_utils import ConsoleUtils

        ConsoleUtils.print_success(f"[SUCCESS]: {message}")

    def log_trace(self, message):
        from .console_utils import ConsoleUtils

        ConsoleUtils.print_colored(f"[TRACE]: {message}", Fore.MAGENTA)

    # Método genérico si quieres pasar el prefijo manualmente
    def log(self, message, prefix="[LOG]"):
        from .console_utils import ConsoleUtils

        ConsoleUtils.print_colored(f"{prefix}: {message}")
