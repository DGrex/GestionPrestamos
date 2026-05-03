# Paquete de infraestructura transversal: persistencia, interfaces, mixins y decoradores.
from .decorators import  confirm_action
from .interfaces import CrudInterface
from .json_manager import JsonManager, JsonManagerError
from .mixins import ValidationMixin, LogMixin
from .console_utils import ConsoleUtils

__all__ = [    
    "confirm_action",
    "CrudInterface",
    "JsonManagerError",
    "JsonManager",
    "ValidationMixin",
    "LogMixin",
    "ConsoleUtils",
]
