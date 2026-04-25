from navigation import exit_program

# from decorators import decorator_menu


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
            {"label": "Préstamos", "action": loanMenu},
            {"label": "Pagos", "action": paymentMenu},
            {"label": "Consultas", "action": queryMenu},
            {"label": "Estadísticas", "action": statisticsMenu},
            {"label": "Salir", "action": "exit"},
        ],
    )


def employeeMenu():
    show_menu(
        "Menú Empleado",
        [
            {"label": "Nuevo Empleado", "action": lambda: print("Crear empleado...")},
            {"label": "Actualizar Empleado", "action": lambda: print("Actualizar...")},
            {"label": "Eliminar Empleado", "action": lambda: print("Eliminar...")},
            {"label": "Atrás", "action": "break"},
            {"label": "Salir", "action": "exit"},
        ],
    )


def loanMenu():
    show_menu(
        "Menú Préstamo",
        [
            {"label": "Nuevo Préstamo", "action": lambda: print("Crear préstamo...")},
            {"label": "Atrás", "action": "break"},
            {"label": "Salir", "action": "exit"},
        ],
    )


def paymentMenu():
    show_menu(
        "Menú Pago",
        [
            {"label": "Nuevo Pago", "action": lambda: print("Registrar pago...")},
            {"label": "Atrás", "action": "break"},
            {"label": "Salir", "action": "exit"},
        ],
    )


def queryMenu():
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


def statisticsMenu():
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
