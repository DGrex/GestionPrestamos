def confirmar_accion(accion: str) -> bool:
    """
    Pregunta al usuario si desea confirmar la acción (eliminar/actualizar).
    Retorna True si confirma (s), False si cancela (n).
    """
    while True:
        respuesta = input(f"¿Está seguro de {accion}? (s/n): ").strip().lower()
        if respuesta == "s":
            return True
        elif respuesta == "n":
            return False
        else:
            print("Respuesta inválida. Por favor ingrese 's' para sí o 'n' para no.")

