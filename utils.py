def confirmar_accion(accion: str) -> bool:
    """
    Pregunta al usuario si desea confirmar la acción (eliminar/actualizar).
    Retorna True si confirma (s), False si cancela (n).
    """
    while True:
        respuesta = input(f"¿Está seguro de {accion}? \n 1. Si \n 2. No \n Ingrese una Opción: ")
        if respuesta == "1":
            return True
        elif respuesta == "2":
            return False
        else:
            print("Respuesta inválida")

