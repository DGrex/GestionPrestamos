# Paquete de modelos de dominio.
# Reexporta las entidades para permitir imports limpios: `from models import ...`.
from .employee import Employee
from .loan import Loan
from .pay import Pay

__all__ = ["Employee", "Loan", "Pay"]
