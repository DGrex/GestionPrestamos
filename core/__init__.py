# Paquete de infraestructura transversal: persistencia, interfaces, mixins y decoradores.
from .decorators import ask_continue
from .interfaces import CrudInterface
from .json_manager import JsonManager, JsonManagerError
from .mixins import ValidationMixin, LogMixin, ConfirmAction
from .console_utils import ConsoleUtils

__all__ = [
    "ask_continue",
    "CrudInterface",
    "JsonManagerError",
    "JsonManager",
    "ValidationMixin",
    "LogMixin",
    "ConfirmAction",
    "ConsoleUtils",
]
