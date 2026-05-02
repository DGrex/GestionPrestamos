# Paquete de modelos de dominio.
# Reexporta las entidades para permitir imports limpios: `from models import ...`.
from .employee_controller import EmployeeController
from .loan_controller import LoanController
from .pay_controller import PayController

__all__ = ["EmployeeController", "LoanController", "PayController"]
