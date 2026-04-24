from navigation import functionExit


def optionMenu():
    while True:
        print("\n========================================")
        print("Sistema de Gestión de Préstamos")
        print("========================================")
        print("1. Empleados")
        print("2. Préstamos")
        print("3. Pagos")
        print("4. Consultas")
        print("5. Estadísticas")
        print("6. Salir")
        option = int(input("Ingrese una Opción: "))

        match option:
            case 1:
                employeeMenu()
            case 2:
                loanMenu()
            case 3:
                paymentMenu()
            case 4:
                queryMenu()
            case 5:
                pass
            case 6:
                functionExit()
            case _:
                print("\nOpción Incorrecta")


def employeeMenu():
    while True:
        print("\n========================================")
        print("Menu Empleado")
        print("========================================")
        print("1. Nuevo Empleado")
        print("2. Actualizar Empleado")
        print("3. Eliminar Empleado")
        print("4. Atrás")
        print("5. Salir")
        option = int(input("Ingrese una Opción: "))
        match option:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                break
            case 5:
                functionExit()


def loanMenu():
    while True:
        print("\n========================================")
        print("Menu Préstamo")
        print("========================================")
        print("1. Nuevo Préstamo")
        print("2. Atrás")
        print("3. Salir")
        option = int(input("Ingrese una Opción: "))
        match option:
            case 1:
                pass
            case 2:
                break
            case 3:
                functionExit()


def paymentMenu():
    while True:
        print("\n========================================")
        print("Menu Pago")
        print("========================================")
        print("1. Nuevo Pago")
        print("2. Atrás")
        print("3. Salir")
        option = int(input("Ingrese una Opción: "))
        match option:
            case 1:
                pass
            case 2:
                break
            case 3:
                functionExit()


def queryMenu():
    while True:
        print("\n========================================")
        print("Menu Consultas")
        print("========================================")
        print("1. Consultar Empleado")
        print("2. Consultar Préstamo")
        print("3. Consultar Pago")
        print("4. Atrás")
        print("5. Salir")
        option = int(input("Ingrese una Opción: "))
        match option:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                break
            case 5:
                functionExit()
