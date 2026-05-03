from .mixins import LogMixin
logMixin = LogMixin()
# Decoradores transversales reutilizables por la capa de vistas y controladores.

# Confirmación previa a la ejecución de la función decorada.
def confirm_action(message="¿Está seguro de que desea continuar? (s/n): "):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                respuesta = input(message).strip().lower()
                if respuesta == "s":
                    return func(*args, **kwargs)
                if respuesta == "n":
                    logMixin.log_info("Acción cancelada por el usuario.")
                    return None
                logMixin.log_error("Respuesta inválida. Use 's' para sí o 'n' para no.")

        return wrapper

    return decorator
