# Paquete de modelos de dominio.
# Reexporta las entidades para permitir imports limpios: `from models import ...`.
from .employee_controller import EmployeeController

__all__ = ["EmployeeController"]
