from datetime import datetime
from navigation import exit_program

from models.empleado_crud import EmpleadoCRUD, Empleado
from models.prestamo_crud import PrestamoCRUD, Prestamo
from models.pago_crud import PagoCRUD
from services.storage import JSONStorageError

from utils import confirmar_accion

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
            {"label": "Nuevo Préstamo", "action": new_loan},
            {"label": "Atrás", "action": "break"},
            {"label": "Salir", "action": "exit"},
        ],
    )


def payment_menu():
    show_menu(
        "Menú Pago",
        [
            {"label": "Nuevo Pago", "action": loan_payment},
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
        if confirmar_accion("Guardar"):
            id_nuevo = crud.create(
                {"nombre": nombre, "cedula": cedula, "sueldo": sueldo}
            )
            print(f"Empleado creado con ID: {id_nuevo}")

    except ValueError as e:
        print("Errores encontrados:")
        print(e)
    except JSONStorageError as e:
        print("Error de almacenamiento:")
        print(e)


def update_employee():
    id_emp = input("Ingrese cedula del empleado a actualizar: ")
    empleado_data = crud.read_by_cedula(id_emp)
    id_emp = empleado_data["id"]
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
            if confirmar_accion("Actualizar"):
                crud.update(id_emp, empleado.to_dict())
                print("Cambios guardados correctamente.")
                break
        elif opcion == "5":
            print("Actualización cancelada.")
            break
        else:
            print("Opción inválida.")


def delete_employee():
    id_emp = input("Ingrese cedula del empleado a eliminar: ")
    empleado_data = crud.read_by_cedula(id_emp)
    id_emp = empleado_data["id"]
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
            if confirmar_accion("Eliminar"):
                crud.delete(id_emp)
                print("Empleado eliminado correctamente.")
                break
        elif opcion == "5":
            print("Eliminación cancelada.")
            break
        else:
            print("Opción inválida.")


def new_loan():
    empleado_crud = EmpleadoCRUD()
    prestamo_crud = PrestamoCRUD()

    id_emp = input("Ingrese cedula del empleado: ")
    empleado_data = empleado_crud.read_by_cedula(id_emp)
    id_emp = empleado_data["id"]

    if not empleado_data:
        print("Empleado no encontrado.")
        return

    # Mostrar datos del empleado
    print("\n--- Datos del empleado ---")
    print(f"Nombre: {empleado_data['nombre']}")
    print(f"Cédula: {empleado_data['cedula']}")
    print(f"Sueldo: {empleado_data['sueldo']}")

    prestamos = prestamo_crud.all()
    for p in prestamos:
        if p["empleado_id"] == id_emp and p["estado"] != "pagado":
            print(
                "\nEste empleado ya tiene un préstamo pendiente. No puede solicitar otro."
            )
            return

    # Pedir datos del préstamo
    fecha_prestamo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    monto = input("Ingrese monto del préstamo: ")
    numero_cuotas = input("Ingrese número de cuotas: ")
    # Crear préstamo
    try:
        if confirmar_accion("Guardar"):
            id_prestamo = prestamo_crud.create(
                {
                    "empleado_id": id_emp,
                    "fecha_prestamo": fecha_prestamo,
                    "monto": monto,
                    "numero_cuotas": numero_cuotas,
                }
            )
            print(f"\nPréstamo creado correctamente con ID: {id_prestamo}")
    except ValueError as e:
        print("Error al crear préstamo:")
        print(e)


def loan_payment():
    empleado_crud = EmpleadoCRUD()
    prestamo_crud = PrestamoCRUD()
    pago_crud = PagoCRUD()

    cedula = input("Ingrese la cédula del empleado: ")

    empleado_data = empleado_crud.read_by_cedula(cedula)
    if not empleado_data:
        print("Empleado no encontrado.")
        return

    # Mostrar datos del empleado
    print("\n--- Datos del empleado ---")
    print(f"Nombre: {empleado_data['nombre']}")
    print(f"Cédula: {empleado_data['cedula']}")
    print(f"Sueldo: {empleado_data['sueldo']}")

    # Buscar préstamo pendiente
    prestamos = prestamo_crud.all()
    prestamo_data = next(
        (
            p
            for p in prestamos
            if p["empleado_id"] == empleado_data["id"] and p["estado"] == "pendiente"
        ),
        None,
    )

    if not prestamo_data:
        print("\nEste empleado no tiene préstamos pendientes.")
        return

    # Mostrar datos del préstamo
    print("\n--- Datos del préstamo ---")
    print(f"ID Préstamo: {prestamo_data['id']}")
    print(f"Fecha: {prestamo_data['fecha_prestamo']}")
    print(f"Monto: {prestamo_data['monto']}")
    print(f"Saldo: {prestamo_data['saldo']}")
    print(f"Cuota: {prestamo_data['cuota']}")

    # Pedir valor del pago

    valor_pago = input("Ingrese valor del pago: ")

    # Usar el método de la clase Prestamo
    prestamo_obj = Prestamo(
        prestamo_data["empleado_id"],
        prestamo_data["fecha_prestamo"],
        prestamo_data["monto"],
        prestamo_data["numero_cuotas"],
    )
    # sincronizar saldo y estado actuales

    # prestamo_obj._Prestamo__saldo = prestamo_data["saldo"]
    # prestamo_obj._Prestamo__estado = prestamo_data["estado"]

    prestamo_obj.set_saldo(prestamo_data["saldo"])
    prestamo_obj.set_estado(prestamo_data["estado"])

    try:
        prestamo_obj.registrar_pago(valor_pago)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Guardar cambios en préstamo
    prestamo_crud.update(prestamo_data["id"], prestamo_obj.to_dict())

    # Guardar registro del pago
    pago_crud.create({"prestamo_id": prestamo_data["id"], "valor_pago": valor_pago})

    print("\nPago registrado correctamente.")
    print(f"Saldo restante: {prestamo_obj.to_dict()['saldo']}")
    print(f"Estado del préstamo: {prestamo_obj.to_dict()['estado']}")
