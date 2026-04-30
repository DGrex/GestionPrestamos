from navigation import exit_program
from models.empleado_crud import EmpleadoCRUD, Empleado
from services.storage import JSONStorageError

crud = EmpleadoCRUD()


def show_menu(title, options):
    while True:
        print("\n========================================")
        print(title)
        print("========================================")
        for i, opt in enumerate(options, start=1):
            print(f"{i}. {opt['label']}")
        try:
            option = int(input("Ingrese una Opción: "))
            if 1 <= option <= len(options):
                action = options[option - 1]["action"]
                if action == "break":
                    break
                elif action == "exit":
                    exit_program()
                elif callable(action):
                    action()
            else:
                print("\nOpción Incorrecta")
        except ValueError:
            print("\nDebe ingresar un número válido.")


def optionMenu():
    show_menu(
        "Sistema de Gestión de Préstamos",
        [
            {"label": "Empleados", "action": employeeMenu},
            {"label": "Préstamos", "action": loan_menu},
            {"label": "Pagos", "action": payment_menu},
            {"label": "Consultas", "action": query_menu},
            {"label": "Estadísticas", "action": statistics_menu},
            {"label": "Salir", "action": "exit"},
        ],
    )


def employeeMenu():
    show_menu(
        "Menú Empleado",
        [
            {"label": "Nuevo Empleado", "action": new_employee},
            {"label": "Actualizar Empleado", "action": update_employee},
            {"label": "Eliminar Empleado", "action": delete_employee},
            {"label": "Atrás", "action": "break"},
            {"label": "Salir", "action": "exit"},
        ],
    )


def loan_menu():
    show_menu(
        "Menú Préstamo",
        [
            {"label": "Nuevo Préstamo", "action": lambda: print("Crear préstamo...")},
            {"label": "Atrás", "action": "break"},
            {"label": "Salir", "action": "exit"},
        ],
    )


def payment_menu():
    show_menu(
        "Menú Pago",
        [
            {"label": "Nuevo Pago", "action": lambda: print("Registrar pago...")},
            {"label": "Atrás", "action": "break"},
            {"label": "Salir", "action": "exit"},
        ],
    )


def query_menu():
    show_menu(
        "Menú Consultas",
        [
            {
                "label": "Consultar Empleado",
                "action": lambda: print("Consulta empleado..."),
            },
            {
                "label": "Consultar Préstamo",
                "action": lambda: print("Consulta préstamo..."),
            },
            {"label": "Consultar Pago", "action": lambda: print("Consulta pago...")},
            {"label": "Atrás", "action": "break"},
            {"label": "Salir", "action": "exit"},
        ],
    )


def statistics_menu():
    show_menu(
        "Menú Estadísticas",
        [
            {
                "label": "Ver estadísticas",
                "action": lambda: print("Mostrando estadísticas..."),
            },
            {"label": "Atrás", "action": "break"},
            {"label": "Salir", "action": "exit"},
        ],
    )


def new_employee():
    nombre = input("Ingrese nombre: ")
    cedula = input("Ingrese cédula: ")
    sueldo = input("Ingrese sueldo: ")
    try:
        id_nuevo = crud.create({"nombre": nombre, "cedula": cedula, "sueldo": sueldo})
        print(f"Empleado creado con ID: {id_nuevo}")
    except ValueError as e:
        print("Errores encontrados:")
        print(e)
    except JSONStorageError as e:
        print("Error de almacenamiento:")
        print(e)


def update_employee():
    id_emp = int(input("Ingrese ID del empleado a actualizar: "))
    empleado_data = crud.read(id_emp)

    if not empleado_data:
        print("Empleado no encontrado.")
        return

    empleado = Empleado(
        empleado_data["nombre"], empleado_data["cedula"], empleado_data["sueldo"]
    )

    opciones = {
        "1": ("Nombre", empleado.get_nombre, empleado.set_nombre),
        "2": ("Cédula", empleado.get_cedula, empleado.set_cedula),
        "3": ("Sueldo", empleado.get_sueldo, empleado.set_sueldo),
    }

    while True:
        print("\n--- Datos actuales del empleado ---")
        for key, (label, getter, _) in opciones.items():
            print(f"{key}. {label}: {getter()}")
        print("4. Guardar cambios")
        print("5. Cancelar")

        opcion = input("Seleccione opción: ")

        if opcion in opciones:
            label, _, setter = opciones[opcion]
            nuevo_valor = input(f"Ingrese nuevo {label}: ")
            try:
                setter(nuevo_valor)
            except ValueError as e:
                print("Error de validación:", e)
        elif opcion == "4":
            crud.update(id_emp, empleado.to_dict())
            print("Cambios guardados correctamente.")
            break
        elif opcion == "5":
            print("Actualización cancelada.")
            break
        else:
            print("Opción inválida.")


def delete_employee():
    id_emp = int(input("Ingrese ID del empleado a eliminar: "))
    empleado_data = crud.read(id_emp)

    if not empleado_data:
        print("Empleado no encontrado.")
        return

    empleado = Empleado(
        empleado_data["nombre"], empleado_data["cedula"], empleado_data["sueldo"]
    )

    data = {
        "Nombre": empleado.get_nombre,
        "Cédula": empleado.get_cedula,
        "Sueldo": empleado.get_sueldo,
    }

    while True:
        print("\n--- Datos actuales del empleado ---")
        for label, getter in data.items():
            print(f"{label}: {getter()}")
        print("\n4. Eliminar")
        print("5. Cancelar")

        opcion = input("Seleccione opción: ")

        if opcion == "4":
            crud.delete(id_emp)
            print("Empleado eliminado correctamente.")
            break
        elif opcion == "5":
            print("Eliminación cancelada.")
            break
        else:
            print("Opción inválida.")
